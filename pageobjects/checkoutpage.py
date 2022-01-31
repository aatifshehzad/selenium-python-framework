from selenium.webdriver.common.by import By

from pageobjects.confirmpage import ConfirmPage


class CheckoutPage:

    def __init__(self, driver):
        self.driver = driver

    tup_checkout_button = (By.XPATH, "//a[contains(text(), 'Checkout')]")
    tup_checkout_success = (By.XPATH, "//button[@class='btn btn-success']")

    def get_checkout_button(self):
        return self.driver.find_element(*CheckoutPage.tup_checkout_button)

    def get_checkout_success(self):
        self.driver.find_element(*CheckoutPage.tup_checkout_success).click()
        obj_confirmpage = ConfirmPage(self.driver)
        return obj_confirmpage
