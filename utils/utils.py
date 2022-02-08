from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from utils.logger import Logger


class Utils:
    obj_logger = Logger().get_logger()

    def wait_for_presence_of_element(self, pdriver, ptup_locator):
        try:
            return WebDriverWait(pdriver, 10).until(
                expected_conditions.presence_of_element_located(ptup_locator))
        except Exception as e:
            self.obj_logger.error("Following Exception Occurred : " + str(e))
            raise Exception(e)

    def select_by_visible_text(self, pdriver, ptup_locator, str_option):
        try:
            Select(pdriver.find_element(*ptup_locator)).select_by_visible_text(str_option)
        except Exception as e:
            self.obj_logger.error("Following Exception Occurred : " + str(e))
            raise Exception(e)
