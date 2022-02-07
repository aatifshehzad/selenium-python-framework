import pytest

from pageobjects.homepage import HomePage
from utils.baseclass import BaseClass
from utils.excel_reader_utils import ExcelReader
from utils.logger import Logger


class TestHomePage(BaseClass):
    obj_excel_reader = ExcelReader()
    obj_logger = Logger().get_logger()

    @pytest.mark.usefixtures('get_data')
    def test_formsubmission(self, get_data):
        try:
            self.obj_logger.info(get_data)
            self.obj_logger.info(Logger.ROOT_PATH)
            obj_homepage = HomePage(self.driver)
            obj_homepage.get_name().send_keys(get_data["Name"])
            obj_homepage.get_email().send_keys(get_data["Email"])
            obj_homepage.get_checkbox().click()
            obj_homepage.get_gender(get_data["Gender"])
            obj_homepage.get_submit().click()
            alert_text = obj_homepage.get_alert().text
            self.obj_logger.info(alert_text)
            assert "Success" in alert_text
        except Exception as e:
            self.obj_logger.error("An Exception Occurred: " + str(e))
            raise Exception(e)

    @pytest.fixture(
        params=obj_excel_reader.get_data_in_list_of_dict("D:\\seleniumPython\\test_data\\test_data.xlsx", "Home_Page"))
    def get_data(self, request):
        return request.param
