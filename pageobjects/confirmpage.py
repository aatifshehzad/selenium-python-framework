from selenium.webdriver.common.by import By

from utils.utils import Utils


class ConfirmPage:

    def __init__(self, driver):
        self.driver = driver

    tup_country = (By.ID, "country")
    tup_country_suggestion = (By.XPATH, "//li/a[.='Pakistan']")
    tup_terms = (By.XPATH, "//a[.='term & Conditions']/parent::label")
    tup_purchase = (By.CSS_SELECTOR, "input[value='Purchase']")
    tup_terms_popup = (By.XPATH, "//h1[.='Terms And Conditions']")
    tup_close_button = (By.XPATH, "//button[.='Close']")
    tup_success_message = (By.CSS_SELECTOR, 'div.alert.alert-success.alert-dismissible')
    obj_utils = Utils()

    def get_country_input(self):
        return self.driver.find_element(*ConfirmPage.tup_country)

    def get_country_suggestion(self):
        return self.obj_utils.wait_for_presence_of_element(self.driver, ConfirmPage.tup_country_suggestion)

    def get_terms_checkbox(self):
        return self.driver.find_element(*ConfirmPage.tup_terms)

    def get_purchase_button(self):
        return self.driver.find_element(*ConfirmPage.tup_purchase)

    def get_terms_popup(self):
        return self.driver.find_element(*ConfirmPage.tup_terms_popup).is_displayed()

    def get_close_button(self):
        return self.driver.find_element(*ConfirmPage.tup_close_button)

    def get_success_alert(self):
        return self.driver.find_element(*ConfirmPage.tup_success_message)



