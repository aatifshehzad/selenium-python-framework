from selenium.webdriver.common.by import By

from pageobjects.checkoutpage import CheckoutPage
from utils.utils import Utils


class HomePage:

    def __init__(self, driver):
        self.driver = driver

    tup_shop = (By.LINK_TEXT, "Shop")
    tup_card = (By.CSS_SELECTOR, ".card-title a")
    tup_add_button = (By.CSS_SELECTOR, ".card-footer button")
    tup_name = (By.CSS_SELECTOR, "[name='name']")
    tup_email = (By.NAME, "email")
    tup_checkbox = (By.ID, "exampleCheck1")
    tuple_gender = (By.ID, 'exampleFormControlSelect1')
    tuple_submit = (By.XPATH, "//input[@class='btn btn-success']")
    tuple_alert = (By.CSS_SELECTOR, "div.alert.alert-success.alert-dismissible")

    obj_utils = Utils()

    def get_shop_item(self):
        self.driver.find_element(*HomePage.tup_shop).click()
        obj_checkoutpage = CheckoutPage(self.driver)
        return obj_checkoutpage

    def get_card_titles(self):
        return self.driver.find_elements(*HomePage.tup_card)

    def get_add_button(self):
        return self.driver.find_elements(*HomePage.tup_add_button)

    def get_name(self):
        return self.driver.find_element(*HomePage.tup_name)

    def get_email(self):
        return self.driver.find_element(*HomePage.tup_email)

    def get_checkbox(self):
        return self.driver.find_element(*HomePage.tup_checkbox)

    def get_gender(self, str_option):
        self.obj_utils.select_by_visible_text(self.driver, HomePage.tuple_gender, str_option)

    def get_submit(self):
        return self.driver.find_element(*HomePage.tuple_submit)

    def get_alert(self):
        return self.driver.find_element(*HomePage.tuple_alert)
