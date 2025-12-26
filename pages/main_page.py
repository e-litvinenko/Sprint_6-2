import allure
import time
from selenium.webdriver.common.by import By
from .base_page import BasePage


class MainPage(BasePage):
    
    ORDER_BUTTON_TOP = (By.XPATH, "//button[text()='Заказать']")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//button[@class='Button_Button__ra12g Button_Middle__1CSJM']")
    FAQ_SECTION = (By.XPATH, "//div[text()='Вопросы о важном']")
    SCOOTER_LOGO = (By.XPATH, "//a[@class='Header_LogoScooter__3lsAR']")
    YANDEX_LOGO = (By.XPATH, "//a[@class='Header_LogoYandex__3TSOI']")
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")

    @allure.step("Клик по верхней кнопке заказа")
    def click_top_order_button(self):
        self.click_element(self.ORDER_BUTTON_TOP)

    @allure.step("Клик по нижней кнопке заказа")
    def click_bottom_order_button(self):
        self.click_element(self.ORDER_BUTTON_BOTTOM)

    @allure.step("Прокрутка к разделу FAQ")
    def scroll_to_faq(self):
        
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    @allure.step("Клик на логотип Самоката")
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    @allure.step("Клик на логотип Яндекса")
    def click_yandex_logo(self):
        self.click_element(self.YANDEX_LOGO)

    @allure.step("Принятие куки")
    def accept_cookies(self):
        try:
            self.click_element(self.COOKIE_BUTTON)
            time.sleep(1)
        except:
            pass