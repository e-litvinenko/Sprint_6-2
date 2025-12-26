import pytest
import allure
from pages.main_page import MainPage
from pages.faq_page import FaqPage


class TestFAQ:
    @allure.feature("FAQ")
    @allure.story("Проверка выпадающего списка вопросов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "question_index,expected_text",
        [
            (0, "Сутки — 400 рублей. Оплата курьеру — наличными или картой."),
            (1, "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим."),
            (2, "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30."),
            (3, "Только начиная с завтрашнего дня. Но скоро станем расторопнее."),
            (4, "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010."),
            (5, "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится."),
            (6, "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои."),
            (7, "Да, обязательно. Всем самокатов! И Москве, и Московской области.")
        ]
    )
    def test_faq_questions(self, setup, question_index, expected_text):
        with allure.step("Открытие главной страницы и принятие куки"):
            main_page = MainPage(setup)
            main_page.accept_cookies()

        with allure.step("Прокрутка к разделу FAQ"):
            main_page.scroll_to_faq()

        with allure.step(f"Клик по вопросу с индексом {question_index}"):
            faq_page = FaqPage(setup)
            faq_page.click_question_by_index(question_index)
            
            assert faq_page.is_answer_displayed_by_index(question_index), \
                f"Ответ на вопрос {question_index} не отображается"

        with allure.step("Проверка текста ответа"):
            actual_text = faq_page.get_answer_text_by_index(question_index)
            
            assert actual_text == expected_text, \
                f"Текст ответа не совпадает. Ожидалось: '{expected_text}', получено: '{actual_text}'"