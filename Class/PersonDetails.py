from selenium import webdriver
from helper.selenium import get_elements
from helper.css_selector import CANDIDATE_PROFILE_DATA_RIGHT, CANDIDATE_PROFILE_DATA_LEFT
from helper.css_selector import CANDIDATE_EXPERIENCE


class PersonDetails:
    def __init__(self, person: dict, driver: webdriver) -> None:
        self.driver: webdriver = driver
        self.person: dict = person
        self.contact_data_left: list = []
        self.contact_data_right: list = []

    def profile_page(self) -> None:
        """Función para ir a la página de perfil del candidato"""

        url = self.person["profile_page"]
        self.driver.get(url)

        self.get_left_side_data()
        self.get_right_side_data()

    def get_left_side_data(self) -> None:
        """Función que extrae los datos de la izquierda en la página del candidato"""

        self.contact_data_left = get_elements(
            CANDIDATE_PROFILE_DATA_LEFT, self.driver)

    def get_right_side_data(self) -> None:
        """Función que extrae los datos de la derecha en la página del candidato"""

        self.contact_data_right = get_elements(
            CANDIDATE_PROFILE_DATA_RIGHT, self.driver)

    def email(self) -> str:
        """Función para extraer el correo del candidato"""

        return self.contact_data_left[0].text

    def dni(self) -> str:
        """Función para extraer el dni del candidato"""

        return self.contact_data_left[1].text

    def phone(self) -> str:
        """Función para extraer el teléfono del candidato"""

        return self.contact_data_left[2].text

    def city(self) -> str:
        """Función para extraer la ciudad donde reside el candidato"""

        return self.contact_data_left[3].text

    def expectation(self) -> str:
        """Función para extraer la expectativa económica del candidato"""

        money_10 = self.contact_data_left[10].text
        if "Mensual".lower() in money_10.lower():
            return money_10

        money_11 = self.contact_data_left[11].text
        if "Mensual".lower() in money_11.lower():
            return money_11

        money_12 = self.contact_data_left[12].text
        if "Mensual".lower() in money_12.lower():
            return money_12

    def personal_summary(self) -> str:
        """Función para extraer el resumen personal del candidato"""

        return self.contact_data_right[0].text

    def work_experience(self) -> [str]:
        """Función para extraer la experiencia del candidato"""

        w_experience_div = self.contact_data_right[2]
        lis = get_elements(CANDIDATE_EXPERIENCE, w_experience_div)

        w_experiences = []
        for el in lis:
            w_experiences.append(el.text)

        return w_experiences
