import os
import requests
import json
import pandas as pd
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement

from dotenv import load_dotenv

from helper.file import save_candidates
from helper.selenium import get_element, get_candidates_webelements
from helper.selenium import go_to_jobposition_page, get_next_pagination_button
from helper.constant import CandidateFields
from helper.ghl import GHL_APP

from Class.PersonData import PersonData
from Class.PersonDetails import PersonDetails
from Class.GHL import GoHighLevel

from pathlib import Path


load_dotenv()

USER_EMAIL = os.getenv("COMPUTRABAJO_USER_EMAIL")
USER_PASS = os.getenv("COMPUTRABAJO_USER_PASSWORD")
COMPUTRABAJO_URL_LOGIN = os.getenv("COMPUTRABAJO_URL_LOGIN")


class Scraper:
    """Clase que realiza el scraping de los candidatos de un anuncio de empleo en computrabajo"""

    def __init__(self) -> None:
        self.driver: webdriver = None
        self.candidates: list = []
        self.next_button: webdriver.Remote._web_element_cls = None
        self.ghl_contacts: list[dict] = []
        # external api debe ser una list[str] para incluir varias aplicaciones.
        self.external_api: str = ""
        self.job_position: str = ""

    def init(self) -> None:
        """Inicio del webdriver para hacer scraper"""

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(15)

    def login(self,
              url_page:str = "",
              user:str = "",
              password:str = "",
              email_css_selector:str = "",
              password_css_selector:str = "",
              btn_css_selector:str = "") -> None:
        """Inicio de sesión"""

        self.driver.get(url_page)

        input_email = get_element(email_css_selector, self.driver)
        input_pass = get_element(password_css_selector, self.driver)

        input_email.send_keys(user)
        input_pass.send_keys(password)

        btn = get_element(btn_css_selector, self.driver)
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
        self.job_position = input(
            "Introduce el nombre del puesto de trabajo\n")

        exist_page_to_scrap = go_to_jobposition_page(self.driver)

        counter = 1
        while loop_validator:
            if exist_page_to_scrap:
                print(f"página {counter} ")

                candidates = get_candidates_webelements(self.driver)
                self.extract_initial_data_from_candidates(candidates)
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

            self.candidates = save_candidates(
                self.candidates, self.job_position)
            print("información preliminar de los candidatos guardada!!")
            print("__"*50)

    def extract_initial_data_from_candidates(self, candidates: list) -> None:
        """Función para extraer la información de cada candidato"""

        local_candidates = []
        for candidate in candidates:
            person = PersonData(candidate)

            data = dict([
                (CandidateFields.NAME.value, person.name()),
                (CandidateFields.IMAGE.value, person.image()),
                (CandidateFields.PROFILE_PAGE.value, person.profile_page()),
                (CandidateFields.APPLICATION_TIME.value, person.application_time()),
                (CandidateFields.AGE.value, person.age()),
                (CandidateFields.GRADE.value, person.grade()),
                (CandidateFields.MATCH.value, person.match()),
            ])

            local_candidates.append(data)

        self.candidates += local_candidates

    def details_of_candidate(self) -> None:
        """Función para extraer información detallada del candidato"""

        counter = 1
        local_candidates = []
        for candidate in self.candidates:

            print(
                f'{counter} - Candidato: {candidate[CandidateFields.NAME.value]}')

            person = PersonDetails(candidate, self.driver)
            person.profile_page()

            data = dict([
                (CandidateFields.EMAIL.value, person.email()),
                (CandidateFields.DNI.value, person.dni()),
                (CandidateFields.PHONE.value, person.phone()),
                (CandidateFields.CITY.value, person.city()),
                (CandidateFields.EXPECTATION.value, person.expectation()),
                (CandidateFields.PERSONAL_SUMMARY.value, person.personal_summary()),
                (CandidateFields.WORK_EXPERIENCE.value, person.work_experience()),
            ])

            candidate_full_data = {**candidate, **data}
            local_candidates.append(candidate_full_data)

            self.send_data_to_external_api(candidate_full_data)

            counter += 1

        self.candidates = local_candidates
        save_candidates(self.candidates, self.job_position)

    def send_data_to_external_api(self, candidate_data) -> None:
        """Función que determina si la información del candidato debe envivarse a una Api externa"""

        if self.external_api == GHL_APP:
            ghl = GoHighLevel(candidate=candidate_data)
            ghl.set_recruitment_platform("computrabajo")
            ghl.set_tags([self.job_position])
            ghl.send()

    def use_external_api(self, send: str = "") -> None:
        """Función que registra las aplicaciones externas para envío de datos"""

        self.external_api = send

    def get_elements(self, css:str = "", web_element:webelement = {}) -> list[webelement]:
        """Funcion para obtener listado de webelements"""

        driver = web_element if web_element else self.driver
        try:
            ele = driver.find_elements(By.CSS_SELECTOR, css)
        except:
            ele = []

        return ele
    
    def get_element(self, css:str = "", web_element:webelement = {}) -> webelement:
        """Funcion para obtener listado de webelements"""

        driver = web_element if web_element else self.driver
        try:
            ele = driver.find_element(By.CSS_SELECTOR, css)
        except:
            ele = None

        return ele

    def end(self) -> None:
        print("%%"*50)
        print("%%"*50)
        print("FIN")
        print("%%"*50)
        print("%%"*50)
