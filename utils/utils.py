from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class Utils:

    def wait_for_presence_of_element(self, pdriver, ptup_locator):
        return WebDriverWait(pdriver, 10).until(
            expected_conditions.presence_of_element_located(ptup_locator))

    def select_by_visible_text(self, pdriver, ptup_locator, str_option):
        Select(pdriver.find_element(*ptup_locator)).select_by_visible_text(str_option)