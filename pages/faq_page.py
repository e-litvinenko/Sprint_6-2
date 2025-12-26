import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class FaqPage(BasePage):
    
    FAQ_QUESTION = (By.XPATH, ".//div[@class='accordion__button']")
    FAQ_ANSWER = (By.XPATH, ".//div[@class='accordion__panel']/p")
    
    @allure.step("Получение количества вопросов FAQ")
    def get_faq_count(self):
        return len(self.find_elements(self.FAQ_QUESTION))

    @allure.step("Клик по вопросу по индексу")
    def click_question_by_index(self, index):
        questions = self.find_elements(self.FAQ_QUESTION)
        if 0 <= index < len(questions):
            self.driver.execute_script("arguments[0].scrollIntoView(true);", questions[index])
            time.sleep(1)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable(questions[index]))
            self.driver.execute_script("arguments[0].click();", questions[index])
            time.sleep(1)

    @allure.step("Получение текста ответа по индексу")
    def get_answer_text_by_index(self, index):
        try:
            wait = WebDriverWait(self.driver, 10)
            answer_locator = (By.XPATH, f"(.//div[@class='accordion__panel']/p)[{index + 1}]")
            answer = wait.until(EC.visibility_of_element_located(answer_locator))
            return answer.text
        except:
            answers = self.find_elements(self.FAQ_ANSWER)
            if index < len(answers):
                return answers[index].text
            return None

    @allure.step("Проверка, что ответ отображается")
    def is_answer_displayed_by_index(self, index):
        try:
            answers = self.find_elements(self.FAQ_ANSWER)
            if index < len(answers):
                return answers[index].is_displayed()
            return False
        except:
            return False