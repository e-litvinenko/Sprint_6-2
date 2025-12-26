import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.order_page import OrderPage


class TestOrderScooter:
    @allure.feature("Заказ самоката")
    @allure.story("Позитивный сценарий заказа через верхнюю кнопку")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "order_button_position,user_data",
        [
            (
                "top",
                {
                    "first_name": "Иван",
                    "last_name": "Иванов",
                    "address": "ул. Ленина, д. 10",
                    "metro_station": "Сокольники",
                    "phone": "+79991234567",
                    "date": "20.12.2024",
                    "rental_period": "сутки",
                    "color": "black",
                    "comment": "Позвонить за час"
                }
            ),
            (
                "bottom",
                {
                    "first_name": "Мария",
                    "last_name": "Петрова",
                    "address": "пр. Мира, д. 25",
                    "metro_station": "Красные Ворота",
                    "phone": "+79997654321",
                    "date": "25.12.2024",
                    "rental_period": "трое суток",
                    "color": "grey",
                    "comment": "Оставить у двери"
                }
            )
        ]
    )
    def test_order_scooter_positive(self, setup, order_button_position, user_data):
        with allure.step("Открытие главной страницы"):
            main_page = MainPage(setup)
            main_page.accept_cookies()

        with allure.step(f"Клик по кнопке заказа ({order_button_position})"):
            if order_button_position == "top":
                main_page.click_top_order_button()
            else:
                setup.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                main_page.click_bottom_order_button()

        with allure.step("Заполнение первой страницы заказа"):
            order_page = OrderPage(setup)
            order_page.fill_first_page(
                user_data["first_name"],
                user_data["last_name"],
                user_data["address"],
                user_data["metro_station"],
                user_data["phone"]
            )

        with allure.step("Заполнение второй страницы заказа"):
            order_page.fill_second_page(
                user_data["date"],
                user_data["rental_period"],
                user_data["color"],
                user_data["comment"]
            )

        with allure.step("Подтверждение заказа"):
            order_page.confirm_order()

        with allure.step("Проверка успешного создания заказа"):
            assert order_page.is_order_successful(), "Заказ не был успешно создан"

    @allure.feature("Навигация")
    @allure.story("Проверка перехода на главную через логотип Самоката")
    @allure.severity(allure.severity_level.NORMAL)
    def test_scooter_logo_navigation(self, setup):
        with allure.step("Открытие главной страницы"):
            main_page = MainPage(setup)
            main_page.accept_cookies()

        with allure.step("Клик по логотипу Самоката"):
            main_page.click_scooter_logo()

        with allure.step("Проверка URL главной страницы"):
            current_url = main_page.get_current_url()
            assert current_url == "https://qa-scooter.praktikum-services.ru/", \
                f"Неверный URL после клика на логотип: {current_url}"

    @allure.feature("Навигация")
    @allure.story("Проверка перехода на Дзен через логотип Яндекса")
    @allure.severity(allure.severity_level.NORMAL)
    def test_yandex_logo_navigation(self, setup):
        with allure.step("Открытие главной страницы"):
            main_page = MainPage(setup)
            main_page.accept_cookies()

        with allure.step("Сохраняем исходное окно"):
            original_window = setup.current_window_handle

        with allure.step("Клик по логотипу Яндекса"):
            main_page.click_yandex_logo()

        with allure.step("Ожидание и переключение на новое окно"):
            wait = WebDriverWait(setup, 10)
            wait.until(EC.number_of_windows_to_be(2))
            
            for window_handle in setup.window_handles:
                if window_handle != original_window:
                    setup.switch_to.window(window_handle)
                    break
            
            wait.until(lambda driver: driver.current_url != "about:blank")

        with allure.step("Проверка URL Дзена"):
            current_url = setup.current_url
            
            assert any(domain in current_url for domain in ['dzen.ru', 'zen.yandex.ru']), \
                f"Неверный URL после клика на логотип Яндекс: {current_url}"

        with allure.step("Закрытие нового окна и возврат к исходному"):
            setup.close()
            setup.switch_to.window(original_window)