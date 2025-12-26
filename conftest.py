import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service


@pytest.fixture(scope="function")
def driver():
    """
    Простейшая фикстура - используем системный Firefox
    """
    options = webdriver.FirefoxOptions()
    options.add_argument("--window-size=1920,1080")
    
    # Просто используем системный Firefox
    # Убедитесь, что Firefox установлен
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)
    
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def setup(driver):
    """
    Настройка тестового окружения
    """
    driver.get("https://qa-scooter.praktikum-services.ru/")
    driver.maximize_window()
    yield driver