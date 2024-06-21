import os

from typing import Generator

from selenium.webdriver.remote import webelement

from Class.Scraper import Scraper
from Class.Scraping.Computrabajo.ComputrabajoCssSelectors import ComputrabajoCssSelectors
from Class.ExternalApi import ExternalApi
from Class.SavingData import SavingData
from Class.Scraping.Computrabajo.ComputrabajoPerson import ComputrabajoPersonData

from helper.constant import CandidateFields

class ComputrabajoScraper:
    def __init__(self) -> None:
        self.scraper:Scraper = Scraper()
        self.css_selectors:ComputrabajoCssSelectors = ComputrabajoCssSelectors()
        self.API = ExternalApi()
        self.FILE = SavingData()
        self.pagination:int = 1
        self.candidates:list = list()
        self.candidates_links:list[webelement] = list()
        self.job_plataform:str = "Computrabajo"

    def start_browser(self) -> None:
        """Iniciar el navegador"""

        print("Iniciando navegador...")
        self.scraper.init()

    def login(self, login_url:str = "", user_email:str = "", user_pass:str = "") -> None:
        """Funcion para iniciar sesion en bumeran"""

        print("Ingresando a la cuenta...")
        self.scraper.login(
            url_page=login_url,
            user=user_email,
            password=user_pass,
            email_css_selector=self.css_selectors.EMAIL_INPUT,
            password_css_selector=self.css_selectors.PASSWORD_INPUT,
            btn_css_selector=self.css_selectors.BTN_INGRESAR,
        )

    def job_post(self, job_url) -> None:
        """Funcion para ir a la pagina del aviso publicado"""

        self.scraper.driver.get(job_url)

    def start_scraping(self) -> None:
        """Funcion para hacer scraping de los candidatos que postularon"""

        self.get_candidates_links()
        candidate_generator = self.loop_candidates()        
        candidate_data_generator = self.extract_candidate_data(candidate_generator)

        for candidate in candidate_data_generator:
            print(f'Datos de {candidate["name"]} guardados en variable self.candidates')
           
            self.candidates.append(candidate)

    def get_candidates_links(self) -> None:
        """Funcion para obtener listado de postulantes de la pagina en formato de webelements"""

        print("Extrayendo candidatos de lista principal...")
        candidates_webelement = self.scraper.get_elements(css=self.css_selectors.CANDIDATES)
        candidates_href = [c.get_attribute('href') for c in candidates_webelement]
        self.candidates_links += candidates_href

        next_page = self.next_page()
        if next_page:
            self.get_candidates_links()

    def loop_candidates(self) -> Generator[any, any, any]:
        """Funcion que recorre uno a uno postulantes"""

        print("Iterando los candidatos...")
        for candidate in self.candidates_links:
            yield candidate

    def extract_candidate_data(self, candidate_generator) -> Generator[dict, any, any]:
        """Funcion que retorna la informacion del postulante"""

        print("Extrayendo informacion de cada candidato...")
        for candidate_url in candidate_generator:
            print("Iniciando extraccion de datos por postulante")

            self.scraper.driver.get(candidate_url)
            # time.sleep(2)

            person = ComputrabajoPersonData(self.scraper, self.css_selectors)

            image = person.image()
            name = person.name()
            phone = person.phone()
            email = person.email()
            dni = person.dni()
            address = person.address()
            age = person.age()
            summary = person.summary()
            experience = person.experience()
            study = person.study()
            skills = person.skills()
            expectation = person.expectation()

            candidate = dict([
                (CandidateFields.IMAGE.value, image),
                (CandidateFields.NAME.value, name),
                (CandidateFields.PHONE.value, phone),
                (CandidateFields.EMAIL.value, email),
                (CandidateFields.DNI.value, dni),
                (CandidateFields.ADDRESS.value, address),
                (CandidateFields.AGE.value, age),
                (CandidateFields.PERSONAL_SUMMARY.value, summary),
                (CandidateFields.WORK_EXPERIENCE.value, experience),
                (CandidateFields.STUDY.value, study),
                (CandidateFields.SKILL.value, skills),
                (CandidateFields.EXPECTATION.value, expectation),
                (CandidateFields.PROFILE_PAGE.value,  self.scraper.driver.current_url),
                (CandidateFields.PLATAFORM.value,  self.job_plataform)
            ])

            yield candidate 

    def get_prop(self, css_selector:str = "", err:str = "") -> str:
        """Funcion para extraer valor de una propiedad del postulante"""

        try:
            prop = self.scraper.get_element(css_selector)
            return prop.text
        except:
            return err
        
    def get_list_of_prop(self, css_selector:str = "", err:str = "") -> str:
        """Funcion para extraer valores de una propiedad del postulante"""

        try:
            text_list = self.scraper.get_elements(css_selector)
            return [t.text for t in text_list]
        except:
            return err

    def next_page(self) -> bool:
        """Funcion para presionar botones de paginacion"""

        n_page_pagintation = self.scraper.get_element(self.css_selectors.NEXT_PAGE)

        if n_page_pagintation:
            n_page_pagintation.click()
            return True
        
        return False

    def save_css_file(self, job_position_name:str="")-> None:
        """Funcion para guardar data en archivo csv"""

        self.FILE.save_candidates(
            candidates=self.candidates,
            file_name=f'{self.job_plataform}_{job_position_name}'
        )

    def end(self, job_position_name:str="") -> None:
        """
        Funcion para terminar el scraping
        """

        print(f"{self.job_plataform}: Scraping Finalizado para '{job_position_name}'")