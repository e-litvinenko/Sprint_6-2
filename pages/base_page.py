import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://qa-scooter.praktikum-services.ru/"

    def _wait_for_element(self, locator, time=10, find_multiple=False, visible=False):
        
        try:
            if find_multiple:
                if visible:
                    return WebDriverWait(self.driver, time).until(
                        EC.visibility_of_all_elements_located(locator)
                    )
                else:
                    return WebDriverWait(self.driver, time).until(
                        EC.presence_of_all_elements_located(locator)
                    )
            else:
                if visible:
                    return WebDriverWait(self.driver, time).until(
                        EC.visibility_of_element_located(locator)
                    )
                else:
                    return WebDriverWait(self.driver, time).until(
                        EC.presence_of_element_located(locator)
                    )
        except Exception:
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot_on_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    def find_element(self, locator, time=10):
        with allure.step(f"Поиск элемента: {locator}"):
            return self._wait_for_element(locator, time, find_multiple=False)

    def find_elements(self, locator, time=10):
        with allure.step(f"Поиск элементов: {locator}"):
            return self._wait_for_element(locator, time, find_multiple=True)

    def wait_for_element_visible(self, locator, timeout=10):
        with allure.step(f"Ожидание видимости элемента: {locator}"):
            return self._wait_for_element(locator, timeout, find_multiple=False, visible=True)

    def go_to_site(self):
        with allure.step(f"Переход на {self.base_url}"):
            self.driver.get(self.base_url)

    def click_element(self, locator):
        with allure.step(f"Клик по элементу: {locator}"):
            self.find_element(locator).click()

    def input_text(self, locator, text):
        with allure.step(f"Ввод текста в {locator}: {text}"):
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)

    def get_current_url(self):
        with allure.step("Получение текущего URL"):
            return self.driver.current_url