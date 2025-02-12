from flask import render_template, url_for, flash, redirect, request, Blueprint, \
    abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
import variables as v
from ubumlaas.users.forms import RegistrationForm, LoginForm, PasswordForm, \
    EmailForm
from ubumlaas.models import User, get_experiments, Country, Experiment
import os
from ubumlaas.util import generate_confirmation_token, confirm_token, \
    send_email, get_ngrok_url
import pandas as pd
import time
from datetime import date
import numpy as np
import multiprocessing as mp
from ubumlaas.admin import clear_tmp_csvs, exps_type
from werkzeug.utils import secure_filename

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    """
    User login.

    Returns:
        string -- redirect new page
    """
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = LoginForm()

    if request.method == "POST":
        go_to = url_for("users.login")
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.check_password(form.password.data):
                login_user(user)
                go_to = url_for("core.index")
                v.app.logger.info("%d - User login", user.id)
            else:
                flash("Wrong username or password", "danger")
                v.app.logger.info("-1 - Login failed")
        else:
            flash("Wrong username or password", "danger")
            v.app.logger.info("-1 - Login failed")
        return redirect(go_to)

    return render_template("login.html", form=form, title="Log in")


@users.route("/register", methods=["GET", "POST"])
def register():
    """
    User registry.

    Returns:
        string -- render register or redirect log in.
    """
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        if form.email_exists(form.email):
            flash("Email already exists", "warning")
            v.app.logger.info(
                "-1 - Trying to register with an email that already exists, %s",
                form.email.data)
        elif form.username_exists(form.username):
            flash("Username already exists", "warning")
            v.app.logger.info(
                "-1 - Trying to register with an username that already exists, %s",
                form.username.data)
        else:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        desired_use=form.desired_use.data,
                        country=form.country.data,
                        activated=0,
                        user_type=1)
            v.db.session.add(user)

            default_datasets(form.username.data)
            flash("User registered.", "success")
            token = generate_confirmation_token(user.email)
            confirm_url = get_ngrok_url('users.confirm_email', token=token)
            html = render_template('confirm.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(subject, user.email, html=html)

            v.app.logger.info("%d - User registered", user.id)

            flash(
                'A confirmation email has been sent via email. Please confirm email before login.',
                'success')
            v.db.session.commit()
            return redirect(url_for("users.login"))
    return render_template("register.html", form=form, title="Register",
                           password_msg=form.password_msg)


def default_datasets(username):
    _dest = "ubumlaas/datasets/" + username + "/"
    _from = "ubumlaas/default_datasets/"
    try:
        os.makedirs(_dest)
        for d in os.listdir(_from):
            os.link(_from + d, _dest + d)
    except OSError:
        pass


@users.route("/logout")
def logout():
    """
    User log out.

    Returns:
        string -- redirect to index.
    """
    v.app.logger.info("%d - User logout", current_user.id)
    logout_user()
    return redirect(url_for("core.index"))


@users.route("/profile", methods=['POST', 'GET'])
@login_required
def profile():
    """User profile load.

    Returns:
        string -- render profile page.
    """
    os.chdir(os.environ['LIBFOLDER'])
    tmp_dir = 'ubumlaas/static/tmp/'
    cards_data = {}
    update_data_form = RegistrationForm()
    del update_data_form.password
    del update_data_form.confirm_password

    update_passwd_form = PasswordForm()

    datasets = [x for x in
                os.listdir("ubumlaas/datasets/" + current_user.username)]
    cards_data['datasets'] = len(datasets)
    experiments = get_experiments(current_user.id)
    cards_data['experiments'] = len(experiments)
    user = current_user.to_dict_all()

    country = Country.query.filter_by(alpha_2=user['country']).first()
    user['country'] = country.to_dict()['name']
    v.app.logger.info(
        "%d - User enter to profile, %d datasets and %d experiments",
        current_user.id, len(datasets), len(experiments))

    exps_type_dict, exps_type_times = exps_type(
        Experiment.query.filter(Experiment.idu == current_user.id).all())
    exps_alg_type_dict = dict(
        sorted(exps_type_dict.items(), key=lambda item: item[1], reverse=True))

    exps_alg_type = pd.DataFrame(
        list(exps_type_dict.items()), columns=['type', 'times'])
    exps_type_times = pd.DataFrame(
        list(exps_type_times.items()), columns=['type', 'seconds'])
    exps_7d_df = pd.DataFrame([[f'I-{x}', 0] for x in range(7)],
                              columns=['day', 'times'])
    today = time.localtime(time.time())[:3]

    for e in experiments:
        try:
            endtime = np.array(
                e['endtime'].strip().split('-')[0].split('/')).astype(int)[::-1]
            delta = date(*today) - date(*endtime)
            if delta.days < 7:
                exps_7d_df.at[delta.days, 'times'] += 1
        except Exception:
            exps_7d_df.at[0, 'times'] += 1

    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    exps_7d_df = exps_7d_df.sort_values(by='day', ascending=False)
    exps_7d_df.to_csv(f'ubumlaas/static/tmp/exp_{current_user.username}_7d.csv',
                      index=False)
    exps_alg_type.to_csv('ubumlaas/static/tmp/exps_alg_type_' +
                         current_user.username + '.csv', index=False)
    exps_type_times.to_csv(
        'ubumlaas/static/tmp/exps_type_' + current_user.username + '_times.csv',
        index=False)

    if request.method == 'POST' and update_data_form.update_checkbox.data:
        if update_data_form.validate_on_submit():
            try:
                v.app.logger.info("%d - User updated its information",
                                  user['id'])

                user_update = User.query.filter_by(
                    email=current_user.email).first_or_404()
                old_username = user_update.username
                user_update.username = update_data_form.username.data
                user_update.email = update_data_form.email.data
                user_update.desired_use = update_data_form.desired_use.data
                user_update.country = update_data_form.country.data
                user_update.website = update_data_form.website.data
                user_update.twitter = update_data_form.twitter.data
                user_update.github = update_data_form.github.data
                user_update.institution = update_data_form.institution.data
                user_update.linkedin = update_data_form.linkedin.data
                user_update.google_scholar = update_data_form.google_scholar.data

                os.chdir(os.path.join('ubumlaas', 'models'))
                try:
                    os.rename(src=old_username,
                              dst=user_update.username)
                except FileNotFoundError:
                    v.app.logger.info(
                        "%d - User has no models", user['id'])
                os.chdir(os.path.join('..', 'datasets'))
                os.rename(src=old_username,
                          dst=user_update.username)
                try:
                    os.chdir(os.path.join('..', 'static', 'avatars'))
                    os.rename(src=old_username + '.png',
                              dst=user_update.username + '.png')
                except FileNotFoundError:
                    v.app.logger.info(
                        "%d - User has no profile picture", user['id'])
                v.db.session.add(user_update)
                v.db.session.commit()
                user = current_user.to_dict_all()
                country = Country.query.filter_by(
                    alpha_2=user['country']).first()
                user['country'] = country.to_dict()['name']
                flash('User updated', 'success')
            except Exception as exc:
                v.app.logger.exception(exc)
                v.db.session.rollback()
                flash('Error ocurred', 'danger')
        else:
            flash('Some fields do not meet the required criteria.', 'warning')

    if request.method == 'POST' and update_passwd_form.pass_checkbox.data:
        if update_passwd_form.validate_on_submit():
            if current_user.check_password(update_passwd_form.password.data):
                flash(
                    'The new password can not be the same as the current password',
                    'danger')
            else:
                v.app.logger.info("%d - User password changed", user['id'])

                user_update = User.query.filter_by(
                    email=current_user.email).first_or_404()
                user_update.set_password(update_passwd_form.password.data)

                v.db.session.add(user_update)
                v.db.session.commit()
                flash("Password changed", "success")
        else:
            flash('Password do not meet the required criteria.', 'warning')

    os.chdir(os.environ['LIBFOLDER'])
    if not os.path.exists(f'ubumlaas/static/avatars/{current_user.id}.png'):
        user['avatar_exists'] = 'Not'
        user['avatar'] = 'static/avatars/default.png'
    else:
        user['avatar_exists'] = 'Exits'
        user['avatar'] = f'static/avatars/{current_user.id}.png'

    mp.Process(target=clear_tmp_csvs, args=(tmp_dir,)).start()
    return render_profile(user, datasets, experiments, update_data_form,
                          update_passwd_form, cards_data, exps_alg_type_dict)


@users.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for("users.login"))

    user = User.query.filter_by(email=email).first_or_404()
    if user.activated:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.activated = True
        v.db.session.add(user)
        v.db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('users.login'))


@users.route('/reset', methods=["GET", "POST"])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("Email account not exist, try with other", "warning")
            v.app.logger.info("-1 - Trying to reset password for unknown user")
            return redirect(url_for('users.reset'))
        v.app.logger.info("%d - Password reset email send", user.id)

        subject = "Password reset requested"

        token = generate_confirmation_token(user.email)

        recover_url = get_ngrok_url('users.reset_with_token', token=token)

        html = render_template(
            'recover.html',
            recover_url=recover_url)

        send_email(subject, user.email, html=html)
        flash("Reset password sended to: " + user.email, "success")
        return redirect(url_for('users.login'))
    return render_template('reset.html', form=form)


@users.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    email = confirm_token(token)
    if not email:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        v.app.logger.info("%d - User password changed", user.id)

        user.set_password(form.password.data)

        v.db.session.add(user)
        v.db.session.commit()
        flash("Password changed", "success")
        return redirect(url_for('users.login'))

    return render_template('reset_with_token.html', form=form, token=token)


def render_profile(user, datasets, experiments, update_data_form,
                   update_passwd_form, cards_data, exps_alg_type_dict):
    return render_template("profile.html",
                           title=current_user.username + " Profile",
                           user=user,
                           datasets=datasets,
                           experiments=experiments,
                           form=update_data_form,
                           pass_form=update_passwd_form,
                           ip=request.environ.get(
                               'HTTP_X_REAL_IP', request.remote_addr),
                           cards_data=cards_data,
                           exps_alg_type=exps_alg_type_dict)


@users.route('/change-picture', methods=['POST'])
def change_picture():
    os.chdir(os.environ['LIBFOLDER'])
    files = request.files.getlist('file[]')
    file = files[0]

    if file and allowed_file(file.filename):
        try:
            secure_filename(file.filename)
            file.save(os.path.join('ubumlaas', 'static', 'avatars',
                                   str(current_user.id) + '.png'))
            flash('Profile picture successfully updated', 'success')
            resp = jsonify({'message': 'Profile picture successfully updated'})
            resp.status_code = 201
            return resp
        except Exception:
            flash('An error occured', 'warning')
            resp = jsonify()
            resp.status_code = 400
            return resp
    else:
        flash('File type is not supported', 'warning')
        resp = jsonify()
        resp.status_code = 400
        return resp


def allowed_file(filename):
    allowed_extensions = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in allowed_extensions
