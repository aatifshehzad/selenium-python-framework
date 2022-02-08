from pageobjects.homepage import HomePage
from utils.baseclass import BaseClass
from utils.logger import Logger


class TestOrder(BaseClass):
    obj_logger = Logger().get_logger()

    def test_place_order(self):
        try:
            obj_homepage = HomePage(self.driver)
            obj_checkoutpage = obj_homepage.get_shop_item()
            card_titles = obj_homepage.get_card_titles()
            i = -1
            for card in card_titles:
                i = i + 1
                if card.text == "Blackberry":
                    obj_homepage.get_add_button()[i].click()
            obj_checkoutpage.get_checkout_button().click()
            obj_confirmpage = obj_checkoutpage.get_checkout_success()
            obj_confirmpage.get_country_input().click()
            obj_confirmpage.get_country_input().send_keys('Pak')
            obj_confirmpage.get_country_suggestion().click()
            obj_confirmpage.get_terms_checkbox().click()
            if obj_confirmpage.get_terms_popup():
                obj_confirmpage.get_close_button().click()
            obj_confirmpage.get_purchase_button().click()
            str_success_message = obj_confirmpage.get_success_alert().text
            assert str_success_message.__contains__(
                'Success! Thank you! Your order will be delivered in next few weeks '
                ':-).')
        except Exception as e:
            self.obj_logger.error("An Exception Occurred: " + str(e))
            raise Exception(e)
