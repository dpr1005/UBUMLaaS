from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, NumberRange
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask import flash
from flask_login import current_user
from ubumlaas.models import User, get_algorithms
import pandas as pd
import os


class ExperimentForm(FlaskForm):
    """Experiment basic form.

    Inherit:
        FlaskForm
    """

    alg_typ = SelectField("Algorithm Type", validators=[DataRequired()],
                          choices=[("", "---"), ("Regression", "Regression"), ("Classification", "Classification")])

    alg_name = SelectField("Algorithm Name", validators=[DataRequired()],
                           choices=[])

    data = SelectField("Select Dataset", validators=[DataRequired()],
                       choices=[("", "---")])

    def alg_list(self, alg_typ):
        """Generate a list of supported algorithms by type.

        Arguments:
            alg_typ {str} -- Type of algorithm (Regression, Classification etc.)
        """
        self.alg_name.choices = [("", "---")]+[(x.alg_name, x.web_name)
                                 for x in get_algorithms(alg_typ)]

    def dataset_list(self):
        """Generate a list of uploaded dataset by current user.
        """
        if os.path.isdir("ubumlaas/datasets/"+current_user.username):
            self.data.choices = [("", "---")]+[(x, x) for x in os.listdir(
                "ubumlaas/datasets/"+current_user.username)]

    submit = SubmitField("Create")


class DatasetForm(FlaskForm):
    """Upload dataset form.

    Inherit:
        FlaskForm
    """
    dataset = FileField("Upload Dataset")

    def to_dataframe(self, filename, upload_folder):
        """Load a dataset in dataframe.

        Arguments:
            filename {str} -- name of dataset
            upload_folder {str} -- folder of current user dataset

        Returns:
            [type] -- [description]
        """
        if filename.split(".")[-1] == "csv":
            file_df = pd.read_csv(upload_folder + filename)
        elif filename.split(".")[-1] == "xls":
            file_df = pd.read_excel(upload_folder + filename)
        else:
            flash("File format not allowed")
        return file_df


class DatasetParametersForm(FlaskForm):
    """Dataset configuration with static parameters.

    Inherit:
        FlaskForm
    """

    train_partition = IntegerRangeField("Train/Test partition", default=70, validators=[NumberRange(1,100)])
