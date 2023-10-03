import os
import requests
import json
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from helper.file import save_candidates
from helper.selenium import get_elements, get_candidates_webelements, go_to_page
from helper.selenium import go_to_jobposition_page, get_next_pagination_button
from Class.PersonData import PersonData
from Class.PersonDetails import PersonDetails

from selenium.webdriver.common.by import By


load_dotenv()

USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASS = os.getenv("USER_PASS")

COMPUTRABAJO_URL_LOGIN = "https://pe.computrabajo.com/login/"


class Scraper:
    """Clase que realiza el scraping de los candidatos de un anuncio de empleo en computrabajo"""

    def __init__(self) -> None:
        self.driver: webdriver = None
        self.candidates: list = []
        self.next_button: webdriver.Remote._web_element_cls = None

    def init(self) -> None:
        """Inicio del webdriver para hacer scraper"""

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

        self.login()

    def login(self) -> None:
        """Inicio de sesión"""

        self.driver.get(COMPUTRABAJO_URL_LOGIN)

        input_email, *_ = get_elements("#Email", self.driver)
        input_pass, *_ = get_elements("#Password", self.driver)

        input_email.send_keys(USER_EMAIL)
        input_pass.send_keys(USER_PASS)

        btn, *_ = get_elements("#bbR", self.driver)
        btn.click()

    def next_page(self) -> bool:
        """Función que obtiene el boton de paginación y lo presiona. Retorna True o False"""

        pagination_btn = get_next_pagination_button(self.driver)

        if pagination_btn:
            pagination_btn.click()
            return True

        return False

    def list_of_candidates(self) -> None:
        """Función para obtener candidatos en un determinado puesto de trabajo"""

        print("...obteniendo los datos")

        loop_validator = True
        exist_page_to_scrap = go_to_jobposition_page(self.driver)

        counter = 1
        while loop_validator:
            if exist_page_to_scrap:
                print(f"página {counter} ")

                candidates = get_candidates_webelements(self.driver)
                self.extract_data_from_candidates(candidates)
                loop_validator = self.next_page()
            else:
                print("=="*50)
                print("Usuario no quiso hacer el scraping...le dio miedito :(")
                print("=="*50)

                loop_validator = False

            counter += 1

        if exist_page_to_scrap:
            print("=="*50)
            print(f"Se encontraron {len(self.candidates)} candidatos")

            self.candidates = save_candidates(self.candidates)

    def extract_data_from_candidates(self, candidates: list) -> None:
        """Función para extraer la información de cada candidato"""

        local_candidates = []
        for candidate in candidates:
            person = PersonData(candidate)

            data = dict([
                ("name", person.name()),
                ("image", person.image()),
                ("profile_page", person.profile_page()),
                ("application_time", person.application_time()),
                ("age", person.age()),
                ("grade", person.grade()),
                ("match", person.match()),
            ])

            local_candidates.append(data)

        self.candidates += local_candidates

    def details_of_candidate(self) -> None:
        """Función para extraer información detallada del candidato"""

        local_candidates = []
        for candidate in self.candidates:

            person = PersonDetails(candidate, self.driver)
            person.profile_page()

            data = dict([
                ("email", person.email()),
                ("dni", person.dni()),
                ("phone", person.phone()),
                ("city", person.city()),
                ("expectation", person.expectation()),
                ("personal_summary", person.personal_summary()),
                ("work_experience", person.work_experience()),
            ])

            local_candidates.append({**candidate, **data})

        self.candidates = local_candidates
        save_candidates(self.candidates)

    def end(self) -> None:
        print("%%"*50)
        print("%%"*50)
        print("FIN")
        print("%%"*50)
        print("%%"*50)
