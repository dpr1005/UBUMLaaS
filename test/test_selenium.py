# Generated by Selenium IDE
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



class TestDefaultSuite():
    def setup_method(self, method):
        """Setup test suite.
        """
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.wait = 0.5

    def teardown_method(self, method):
        """Shut down current test.
        """
        self.driver.quit()

    def login(self, usermail):
        """Login on with usermail test account.
        
        Arguments:
            usermail {string} -- mail from test account.
        """
        self.driver.get("http://localhost:5000/")
        self.driver.set_window_size(1536, 824)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys(usermail)
        self.driver.find_element(By.ID, "password").send_keys("thisIsATest1!")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

    def logout(self):
        """Logout and check we have loged out.
        """
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        assert self.driver.find_element(By.LINK_TEXT, "Login").text == "Login"

    def test_1Register(self):
        """Test to correct register in the page.

            Steps:
                1. Click register.
                2. Complete form.
                3. Submit form.
                4. Check for alert with "User registered"
        """
        self.driver.get("http://localhost:5000/")
        self.driver.set_window_size(1536, 824)
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("ubumlaas@gmail.com")
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("ubumlaas")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("thisIsATest1!")
        self.driver.find_element(By.ID, "confirm_password").click()
        self.driver.find_element(By.ID, "confirm_password").send_keys("thisIsATest1!")
        self.driver.find_element(By.ID, "submit").click()
        WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".alert")))
        assert self.driver.find_element(By.CSS_SELECTOR, ".alert").text == "User registered.\n×"

    def test_21LoginIncorrect(self):
        """Incorrect login.

            Steps:
                1. Click on login.
                2. Complete form with false information.
                3. Submit form.
                4. Check alert "Wrong username or password".
        """
        self.driver.get("http://localhost:5000/")
        self.driver.set_window_size(1536, 824)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("ubumlaas@gmail.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("ThisIsNotMyPassword")
        self.driver.find_element(By.ID, "submit").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".alert").text == "Wrong username or password\n×"

    def test_22LoginAndLogoutCorrect(self):
        """Correct login and logout.

            Steps:
                1. Login correctly.
                2. Check if login ok.
                3. Logout (and check logout).
        """
        self.login("ubumlaas@gmail.com")
        assert self.driver.find_element(By.LINK_TEXT, "My launched experiments").text == "My launched experiments"
        self.logout()

    def test_31DatasetLoad(self):
        """Dataset load correct, for 4 datasets already uploaded.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select and check all datasets uploaded for the user.
                4. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".jumbotron > .text-center").text == "Configure experiment"
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, "#dataset_parameters_0 > div > table > thead > tr > th:nth-child(3)").text == "Cl.thickness"
        self.driver.execute_script("$('#data_0').val('iris.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, "#dataset_parameters_0 > div > table > thead > tr > th:nth-child(2)").text == "sepal length (cm)"
        self.driver.execute_script("$('#data_0').val('music.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, "#dataset_parameters_0 > div > table > thead > tr > th:nth-child(2)").text == "amazed-suprised"
        self.driver.execute_script("$('#data_0').val('weatherHistory.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, "#dataset_parameters_0 > div > table > thead > tr > th:nth-child(2)").text == "Temperature (C)"
        self.logout()  

    def test_321DatasetUseNormal(self):
        """Click on use in dataset variable.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on use switch.
                5. Check if this variable has changed on reduced mode.
                6. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.execute_script("$('#col0_use_label_0').click();")
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        WebDriverWait(self.driver, 30000).until(expected_conditions.visibility_of_element_located((By.ID, "0_opt_0")))
        element = self.driver.find_element(By.ID, "0_opt_0")
        assert "list-group-item-secondary" in element.get_attribute('class').split(" ")
        self.logout()

    def test_322DatasetUseReduced(self):
        """Click on use in dataset variable.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on Reduce.
                5. Change one use variable state to no use. 
                6. Click on Normal.
                7. Check if switch of selected variable has changed.
                8. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        self.driver.execute_script('$("#sel_0 option[value=\'Id\']").prop("selected",true)')
        self.driver.execute_script('$("#nuse_0").click()')
        self.driver.find_element(By.ID, "normal_tab_link").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col0_use_0:checked")
        assert len(elements) == 0
        self.logout()

    def test_331DatasetNotUseNormal(self):
        """Click on no use in dataset variable.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on use switch.
                5. Click on use switch on the same varible, to change from no use to use.
                6. Check if this variable has not changed on reduced mode.
                7. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.execute_script("$('#col0_use_label_0').click();")
        self.driver.execute_script("$('#col0_use_label_0').click();")
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        element = self.driver.find_element(By.ID, "0_opt_0")
        assert "list-group-item-primary" in element.get_attribute('class').split(" ")
        self.logout()

    def test_332DatasetNotUseReduced(self):
        """Click on no usem, then on use in dataset variable on reduced mode.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on Reduced.
                5. Change variable to no use then to use again.
                6. Click on Normal.
                7. Check if variable switch use is checked.
                8. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        self.driver.execute_script('$("#sel_0 option[value=\'Id\']").prop("selected",true)')
        self.driver.execute_script('$("#nuse_0").click()')
        self.driver.execute_script('$("#sel_0 option[value=\'Id\']").prop("selected",true)')
        self.driver.execute_script('$("#use_0").click()')
        self.driver.find_element(By.ID, "normal_tab_link_0").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col0_use_0:checked")
        assert len(elements) > 0
        self.logout()

    def test_341DatasetNoTargetNormal(self):
        """Click on target in dataset variable.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on target variable, to change to not target.
                5. Check target is un checked and use is unchecked.
                6. Click on Reduced.
                7. Check if variable is on no use mode.
                8. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.execute_script("$('#col10_target_label_0').click();")
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_use_0:checked")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_target_0:checked")
        assert len(elements) == 0
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        element = self.driver.find_element(By.ID, "10_opt_0")
        assert "list-group-item-secondary" in element.get_attribute('class').split(" ")
        self.logout()

    def test_342DatasetNoTargetReduced(self):
        """Click on no use on dataset variable on reduced mode.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on Reduced.
                5. Change target variable to no use.
                6. Check no use variable.
                6. Click on Normal.
                7. Check if variable switch use is not checked.
                8. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        self.driver.execute_script('$("#sel_0 option[value=\'Class\']").prop("selected",true)')
        self.driver.execute_script('$("#nuse_0").click()')
        element = self.driver.find_element(By.ID, "10_opt_0")
        assert "list-group-item-secondary" in element.get_attribute('class').split(" ")
        self.driver.find_element(By.ID, "normal_tab_link_0").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_use_0:checked")
        assert len(elements) == 0
        self.logout()

    def test_351DatasetNoTargetUseNormal(self):
        """Click on use in dataset target variable.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click use switch of target variable.
                5. Check target is unchecked and use checked.
                6. Click on Reduced.
                7. Check if variable is on use mode.
                8. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.execute_script("$('#col10_use_label_0').click();")
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_use_0:checked")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_target_0:checked")
        assert len(elements) == 0
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        element = self.driver.find_element(By.ID, "10_opt_0")
        assert "list-group-item-primary" in element.get_attribute('class').split(" ")
        self.logout()

    def test_352DatasetNoTargetUseReduced(self):
        """Click on use in dataset target variable on reduced mode.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on Reduced.
                5. Change target variable to use.
                6. Click on Normal.
                7. Check if variable switch use is checked and target unchecked.
                8. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        self.driver.execute_script('$("#sel_0 option[value=\'Class\']").prop("selected",true)')
        self.driver.execute_script('$("#use_0").click()')
        element = self.driver.find_element(By.ID, "10_opt_0")
        assert "list-group-item-primary" in element.get_attribute('class').split(" ")
        self.driver.find_element(By.ID, "normal_tab_link_0").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_use_0:checked")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_target_0:checked")
        assert len(elements) == 0
        self.logout()

    def test_361DatasetChangeTargetNormal(self):
        """Change target variable.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click target switch on use variable.
                5. Check old target variable is now in no use mode and new target on target mode.
                6. Click on Reduced.
                7. Check if variable old target is on no use mode and new target on target mode.
                8. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.execute_script("$('#col9_target_label_0').click();")
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_use_0:checked")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_target_0:checked")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col9_use_0:checked")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col9_target_0:checked")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        element = self.driver.find_element(By.ID, "10_opt_0")
        assert "list-group-item-secondary" in element.get_attribute('class').split(" ")
        element = self.driver.find_element(By.ID, "9_opt_0")
        assert "list-group-item-success" in element.get_attribute('class').split(" ")
        self.logout()

    def test_362DatasetChangeTargetReduced(self):
        """Change target variable on reduced mode.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on Reduced.
                5. Change variable to target mode.
                6. Check if variable is on target mode and old target on no use mode.
                6. Click on Normal.
                7. Check old target variable is now in no use mode and new target on target mode.
                8. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        self.driver.execute_script("$('#sel_0 option[value=\"Mitoses\"]').prop('selected',true);")
        self.driver.execute_script("$('#target_0').click();")
        element = self.driver.find_element(By.ID, "10_opt_0")
        assert "list-group-item-secondary" in element.get_attribute('class').split(" ")
        element = self.driver.find_element(By.ID, "9_opt_0")
        assert "list-group-item-success" in element.get_attribute('class').split(" ")
        self.driver.find_element(By.ID, "normal_tab_link_0").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_use_0:checked")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col10_target_0:checked")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col9_use_0:checked")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col9_target_0:checked")
        assert len(elements) > 0
        self.logout()

    def test_37DatasetNoMultiLabelTarget(self):
        """Change target variable on reduced mode.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset.
                4. Click on Reduced.
                5. Select multiple variables and try to set them to target mode.
                6. Check alert You can't select more than 1 target in no multilabel algorithms.
                7. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#data_0').val('breastCancer.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        self.driver.execute_script("$('#sel_0 option[value=\"Cell.shape\"]').prop('selected',true);")
        self.driver.execute_script("$('#sel_0 option[value=\"Marg.adhesion\"]').prop('selected',true);")
        self.driver.execute_script("$('#sel_0 option[value=\"Epith.c.size\"]').prop('selected',true);")
        self.driver.execute_script("$('#sel_0 option[value=\"Bare.nuclei\"]').prop('selected',true);")
        self.driver.execute_script('$("#target_0").click()')
        time.sleep(self.wait*2)
        assert self.driver.find_element(By.CSS_SELECTOR, "#alert_modal_body > p:nth-child(1)").text == "You can't select more than 1 target in no multilabel algorithms."
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "alert_modal_close").click()
        time.sleep(self.wait*2)
        self.logout()

    def test_381DatasetMultiLabelTargetNormal(self):
        """Multilabel target variables.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset and cange algorithm type to MultiClassfication.
                4. Click 6 first variables target switch
                5. Check target switch checked and use switch unchecked.
                6. Click on use switch on target variable.
                7. Click on Reduced.
                8. Check 6 first variables are on target mode and old target on use mode.
                9. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#alg_typ').val(\"MultiClassification\")")
        self.driver.execute_script("$('#alg_typ').change();")
        self.driver.execute_script("$('#data_0').val('music.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        elm = list(range(6))
        for e in elm:
            self.driver.execute_script("$('#col"+str(e)+"_target_label_0').click();")
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#col"+str(e)+"_use_0:checked")
            assert len(elements) == 0
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#col"+str(e)+"_target_0:checked")
            assert len(elements) > 0
        self.driver.execute_script("$('#col76_use_label_0').click();")

        self.driver.find_element(By.ID, "reduced_tab_link_0").click()

        element = self.driver.find_element(By.ID, "76_opt_0")
        assert "list-group-item-primary" in element.get_attribute("class").split(" ")

        for e in elm:
            element = self.driver.find_element(By.ID, str(e)+"_opt_0")
            assert "list-group-item-success" in element.get_attribute("class").split(" ")
        self.logout()

    def test_382DatasetMultiLabelTargetReduced(self):
        """Multilabel target variables reduced mode.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset and cange algorithm type to MultiClassfication.
                4. Click on Reduced.
                5. Change target variable to use mode.
                6. Select first 6 variables and click target mode.
                7. Check if fist 6 variable mode is target.
                8. Click Normal.
                9. Check all first 6 target variables use switch unchecked and target switch checked.
                10. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()

        self.driver.execute_script("$('#alg_typ').val(\"MultiClassification\")")
        self.driver.execute_script("$('#alg_typ').change();")
        self.driver.execute_script("$('#data_0').val('music.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        self.driver.execute_script("$('#sel_0 option[value=\"BHSUM3\"]').prop('selected', true);")
        self.driver.execute_script("$('#use_0').click();")

        assert "list-group-item-primary" in self.driver.find_element(By.ID, "76_opt_0").get_attribute("class").split(" ")

        elm = ['amazed-suprised', 'happy-pleased', 'relaxing-clam', 'quiet-still', 'sad-lonely', 'angry-aggresive']
        for e in elm:
            self.driver.execute_script("$('#sel_0 option[value=\""+e+"\"]').prop('selected', true);")
        self.driver.execute_script("$('#target_0').click();")
        for e in range(6):
            assert "list-group-item-success" in self.driver.find_element(By.ID, str(e)+"_opt_0").get_attribute("class").split(" ")

        self.driver.find_element(By.ID, "normal_tab_link_0").click()
        for e in range(6):
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#col"+str(e)+"_use_0:checked")
            assert len(elements) == 0
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#col"+str(e)+"_target_0:checked")
            assert len(elements) > 0
        self.logout()

    def test_39DatasetFromMultiLabelToMonoLabel(self):
        """Change form multilabel to monolabel algorithm type.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select dataset and cange algorithm type to MultiClassfication.
                4. Click on Reduced.
                5. Change target variable to use mode.
                6. Select first 6 variables and click target mode.
                7. Change to Classification on algorithm type.
                8. Check 6 first variables are on use mode and last variable is on target mode.
                9. Click Normal.
                10. Check all first 6 target variables use switch checked and target switch unchecked.
                11. Check last variables target switch is checked and use switch unchecked.
                12. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()

        self.driver.execute_script("$('#alg_typ').val(\"MultiClassification\")")
        self.driver.execute_script("$('#alg_typ').change();")
        self.driver.execute_script("$('#data_0').val('music.csv');")
        self.driver.execute_script("$('#data_0').change();")
        time.sleep(self.wait)
        self.driver.find_element(By.ID, "reduced_tab_link_0").click()
        self.driver.execute_script("$('#sel_0 option[value=\"BHSUM3\"]').prop('selected', true);")
        self.driver.execute_script("$('#use_0').click();")

        elm = ['amazed-suprised', 'happy-pleased', 'relaxing-clam', 'quiet-still', 'sad-lonely', 'angry-aggresive']
        for e in elm:
            self.driver.execute_script("$('#sel_0 option[value=\""+e+"\"]').prop('selected', true);")
        self.driver.execute_script("$('#target_0').click();")

        self.driver.execute_script("$('#alg_typ').val(\"Classification\")")
        self.driver.execute_script("$('#alg_typ').change();")

        time.sleep(self.wait)
        assert "list-group-item-success" in self.driver.find_element(By.ID, "76_opt_0").get_attribute("class").split(" ")
        for e in range(6):
            assert "list-group-item-primary" in self.driver.find_element(By.ID, str(e)+"_opt_0").get_attribute("class").split(" ")

        self.driver.find_element(By.ID, "normal_tab_link_0").click()
        for e in range(6):
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#col"+str(e)+"_use_0:checked")
            assert len(elements) > 0
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#col"+str(e)+"_target_0:checked")
            assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col76_use_0:checked")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#col76_target_0:checked")
        assert len(elements) > 0
        self.logout()

    def test_4TrainTextCrossvalidation(self):
        """Check train-test/cross-validation selector.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Check train test is loaded default.
                4. Change to cross validation.
                5. Check cross validation is loaded.
                6. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "#train_test_div > .form-control-label").text == "Train/Test partition"
        time.sleep(self.wait*2)
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.ID, "random_seed_div"))
        time.sleep(self.wait*2)
        self.driver.find_element(By.CSS_SELECTOR, "#config_experiment_block > div:nth-child(3) > div > label.pure-material-radio.ml-2").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "#cross_validation_div > label").text == "Number of folds"
        self.logout()

    def test_51Algorithm(self):
        """Check algorithm base estimator generator.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select Classification on algorithm type.
                4. Select Bagging algorithm.
                5. Select Bagging on base estimator.
                6. Check title is Bagging.
                6. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#alg_typ').val(\"Classification\");")
        self.driver.execute_script("$('#alg_typ').change();")
        time.sleep(self.wait)
        self.driver.execute_script("$('#alg_name_0').val(\"sklearn.ensemble.BaggingClassifier\");")
        self.driver.execute_script("$('#alg_name_0').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, "p.font-weight-bold").text == "Decision Tree"
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.ID, "select_algorithm_block"))
        self.driver.find_element(By.CSS_SELECTOR, "#base_estimator_0_open > .material-icons").click()
        self.driver.execute_script("$('#base_estimator_0_value').val(\"sklearn.ensemble.BaggingClassifier\");")
        self.driver.execute_script("$('#base_estimator_0_value').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, "#base_estimator_0_title > .font-weight-bold").text == "Bagging"
        self.logout()

    def test_52Algorithm2(self):
        """Check algorithm config generation and destruction.

            Steps:
                1. Login.
                2. Click on New Experiment.
                3. Select Classification on algorithm type.
                4. Select Bagging algorithm.
                5. Check title is Decision Tree.
                6. Select Bagging on base estimator on next 3 base estimators and check the title is Decision Tree when Bagging config is loaded.
                7. On first base estimator change Bagging to KNN.
                8. Check destruction checking title KNN.
                9. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "New Experiment").click()
        self.driver.execute_script("$('#alg_typ').val(\"Classification\");")
        self.driver.execute_script("$('#alg_typ').change();")
        time.sleep(self.wait)
        self.driver.execute_script("$('#alg_name_0').val(\"sklearn.ensemble.BaggingClassifier\");")
        self.driver.execute_script("$('#alg_name_0').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, "p.font-weight-bold").text == "Decision Tree"
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.ID, "select_algorithm_block"))
        self.driver.find_element(By.CSS_SELECTOR, "#base_estimator_0_open > .material-icons").click()
        self.driver.execute_script("$('#base_estimator_0_value').val(\"sklearn.ensemble.BaggingClassifier\");")
        self.driver.execute_script("$('#base_estimator_0_value').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, "#base_estimator_0_title > .font-weight-bold").text == "Bagging"
        for i in range(1,3):
            self.driver.find_element(By.CSS_SELECTOR, "#level"+str(i)+"_base_estimator_0_open > .material-icons").click()
            self.driver.execute_script("$('#level"+str(i)+"_base_estimator_0_value').val(\"sklearn.ensemble.BaggingClassifier\");")
            self.driver.execute_script("$('#level"+str(i)+"_base_estimator_0_value').change();")
            time.sleep(self.wait)
            assert self.driver.find_element(By.CSS_SELECTOR, "#level"+str(i+1)+"_base_estimator_0_title > .font-weight-bold").text == "Decision Tree"
        self.driver.execute_script("$('#base_estimator_0_value').val(\"sklearn.neighbors.KNeighborsClassifier\");")
        self.driver.execute_script("$('#base_estimator_0_value').change();")
        time.sleep(self.wait)
        assert self.driver.find_element(By.CSS_SELECTOR, ".font-weight-bold").text == "KNN"
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#level2_base_estimator_0_title")
        assert len(elements) == 0
        self.logout()

    def test_61NoExperiments(self):
        """Check no experiment on user.

            Steps:
                1. Login.
                2. Click on My launched experiments.
                3. Check text "No data available in table on experiment" table.
                4. Logout.
        """
        self.login("ubumlaas@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "My launched experiments").click()
        time.sleep(self.wait)
        assert "No data available in table" in self.driver.find_element(By.CSS_SELECTOR, ".dataTables_empty").text
        self.logout()

    def test_62Experiments(self):
        """Check experiment on user2.

            Steps:
                1. Login as ubumlaas2.
                2. Click on My launched experiments
                3. Check KNN experiment.
                4. Logout.
        """
        self.login("ubumlaas2@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "My launched experiments").click()
        time.sleep(self.wait)
        assert "KNN" in self.driver.find_element(By.CSS_SELECTOR, "#exper > tbody > tr > td:nth-child(2)").text
        self.logout()

    def test_63ExperimentInfo(self):
        """Check experiment on user2.

            Steps:
                1. Login as ubumlaas2.
                2. Click on My launched experiments.
                3. Click on See.
                3. Check KNN experiment on algorithm information.
                4. Logout.
        """
        self.login("ubumlaas2@gmail.com")
        self.driver.find_element(By.LINK_TEXT, "My launched experiments").click()
        time.sleep(self.wait)
        self.driver.find_element(By.LINK_TEXT, "SEE").click()
        time.sleep(self.wait)
        assert "KNeighborsClassifier" in self.driver.find_element(By.CSS_SELECTOR, "#alg_params > div > div.col-12.row-odd > label").text
        self.logout()
