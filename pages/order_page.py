import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage


class OrderPage(BasePage):
    FIRST_NAME_INPUT = (By.XPATH, ".//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, ".//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, ".//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, ".//input[@placeholder='* Станция метро']")
    METRO_STATION_ITEM = (By.XPATH, ".//div[@class='select-search__select']/ul/li/button")
    PHONE_INPUT = (By.XPATH, ".//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, ".//button[text()='Далее']")

    DATE_INPUT = (By.XPATH, ".//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.XPATH, ".//div[@class='Dropdown-control']")
    RENTAL_PERIOD_OPTION = (By.XPATH, ".//div[@class='Dropdown-option']")
    COLOR_BLACK_CHECKBOX = (By.ID, "black")
    COLOR_GREY_CHECKBOX = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, ".//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, ".//button[@class='Button_Button__ra12g Button_Middle__1CSJM' and text()='Заказать']")

    CONFIRM_ORDER_BUTTON = (By.XPATH, ".//button[text()='Да']")
    SUCCESS_MESSAGE = (By.XPATH, ".//div[contains(@class, 'Order_ModalHeader')]")
    ORDER_NUMBER = (By.XPATH, ".//div[contains(@class, 'Order_Text')]")

    @allure.step("Заполнение первой страницы заказа")
    def fill_first_page(self, first_name, last_name, address, metro_station, phone):
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.ADDRESS_INPUT, address)
        
        self._select_metro_station(metro_station)
        self.input_text(self.PHONE_INPUT, phone)
        self.click_element(self.NEXT_BUTTON)
        time.sleep(2)

    @allure.step("Заполнение второй страницы заказа")
    def fill_second_page(self, date, rental_period, color, comment):
        self._select_date(date)
        self._select_rental_period(rental_period)
        self._select_color(color)
        
        if comment:
            self.input_text(self.COMMENT_INPUT, comment)
        
        self.click_element(self.ORDER_BUTTON)
        time.sleep(2)

    @allure.step("Подтверждение заказа")
    def confirm_order(self):
        self.click_element(self.CONFIRM_ORDER_BUTTON)
        time.sleep(3)

    @allure.step("Проверка успешного создания заказа")
    def is_order_successful(self):
        try:
            self.wait_for_element_visible(self.SUCCESS_MESSAGE, timeout=10)
            return True
        except:
            return False

    @allure.step("Получение номера заказа")
    def get_order_number(self):
        if self.is_order_successful():
            return self.find_element(self.ORDER_NUMBER).text
        return None

    def _select_metro_station(self, station_name):
        self.click_element(self.METRO_STATION_INPUT)
        time.sleep(1)
        stations = self.find_elements(self.METRO_STATION_ITEM)
        for station in stations:
            if station_name in station.text:
                station.click()
                return

    def _select_date(self, date):
        date_input = self.find_element(self.DATE_INPUT)
        date_input.click()
        date_input.send_keys(Keys.CONTROL + "a")
        date_input.send_keys(Keys.DELETE)
        date_input.send_keys(date)
        date_input.send_keys(Keys.ENTER)
        time.sleep(1)

    def _select_rental_period(self, period):
        self.click_element(self.RENTAL_PERIOD_DROPDOWN)
        time.sleep(1)
        periods = self.find_elements(self.RENTAL_PERIOD_OPTION)
        for p in periods:
            if period in p.text:
                p.click()
                return

    def _select_color(self, color):
        if color == "black":
            self.click_element(self.COLOR_BLACK_CHECKBOX)
        elif color == "grey":
            self.click_element(self.COLOR_GREY_CHECKBOX)