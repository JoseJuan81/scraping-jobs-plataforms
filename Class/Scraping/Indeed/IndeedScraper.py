import os

from typing import Generator

from selenium.webdriver.remote import webelement

from Class.Scraper import Scraper
from Class.Scraping.Indeed.IndeedCssSelectors import IndeedCssSelectors
from Class.ExternalApi import ExternalApi
from Class.SavingData import SavingData

from helper.constant import CandidateFields

class IndeedScraper:
    def __init__(self) -> None:
        self.scraper:Scraper = Scraper()
        self.css_selectors:IndeedCssSelectors = IndeedCssSelectors()
        self.API = ExternalApi()
        self.FILE = SavingData()
        self.pagination:int = 1
        self.candidates:list = list()
        self.candidates_webelement:list[webelement] = list()
        self.job_plataform:str = "Indeed"

    def start_browser(self) -> None:
        """Iniciar el navegador"""

        print("Iniciando navegador...")
        self.scraper.init()

    def login(self, login_url:str = "", user_email:str = "") -> None:
        """Funcion para iniciar sesion en bumeran"""

        print("Ingresando a la cuenta...")
        self.scraper.driver.get(login_url)
        # input_email = self.scraper.get_element(self.css_selectors.EMAIL_INPUT, self.scraper.driver)
        # input_email.send_keys(user_email)
        
        # continue_button = self.scraper.get_element(self.css_selectors.CONTINUE_BTN, self.scraper.driver)
        # continue_button.click()

        input("Manualmente haga el inicio de sesion y al finalizar presione 'Enter' para continuar con el scraping")

    def job_post(self, job_url) -> None:
        """Funcion para ir a la pagina del aviso publicado"""

        self.scraper.driver.get(job_url)

    def start_scraping(self) -> None:
        """Funcion para hacer scraping de los candidatos que postularon"""

        self.press_on_first_candidate()
        self.load_all_candidates()
        self.get_candidates()
        candidate_generator = self.loop_candidates()        
        candidate_data_generator = self.extract_candidate_data(candidate_generator)

        for candidate in candidate_data_generator:
            print(f'Datos de {candidate["name"]} guardados en variable self.candidates')
           
            self.candidates.append(candidate)

    def press_on_first_candidate(self) -> None:
        """Funcion para obtener hacer click al primer candidato y pueda mostrarse
        el modal lateral con la informacion detallada"""

        print("Presionando sobre el primer candidato para mostrar informacion detallada")
        first_candidate = self.scraper.get_element(self.css_selectors.FIRST_CANDIDATE)
        first_candidate.click()

    def load_all_candidates(self) -> None:
        """
        Funcion para presionar boton 'cargar mas' para cargar todos los
        candidatos
        """

        print("Cargando todos los candidatos...")
        print("Espere un momento por favor")
        
        load_more = self.scraper.get_element(self.css_selectors.LOAD_MORE)
        if load_more:
            load_more.click()
            self.load_all_candidates()

    def get_candidates(self) -> None:
        """
        Funcion para obtener todos los candidatos
        """

        self.candidates_webelement = self.scraper.get_elements(self.css_selectors.CANDIDATES)

    def loop_candidates(self) -> Generator[any, any, any]:
        """Funcion que recorre uno a uno postulantes"""

        print("Iterando los candidatos...")
        for candidate in self.candidates_webelement:
            yield candidate

    def extract_candidate_data(self, candidate_generator) -> Generator[dict, any, any]:
        """Funcion que retorna la informacion del postulante"""

        print("Extrayendo informacion de cada candidato...")
        for candidate_webelement in candidate_generator:
            print("Iniciando extraccion de datos por postulante")

            candidate_webelement.click()

            name = self.get_prop(css_selector=self.css_selectors.NAME, err="Sin Nombre")

            phone = self.get_phone(self.css_selectors.PHONE_BTN, err="Sin telefono")
            email = self.get_prop(self.css_selectors.EMAIL, err="Sin correo")
            address = self.get_address(self.css_selectors.ADDRESS_CONTAINER, err="Sin Direccion")
            experience, study, skills = self.get_additional_information(self.css_selectors.ADDITIONAL_INFORMATION)

            candidate = dict([
                (CandidateFields.NAME.value, name),
                (CandidateFields.PHONE.value, phone),
                (CandidateFields.EMAIL.value, email),
                (CandidateFields.DNI.value, "XXX"),
                (CandidateFields.ADDRESS.value, address),
                (CandidateFields.AGE.value, "YYY"),
                (CandidateFields.WORK_EXPERIENCE.value, experience),
                (CandidateFields.STUDY.value, study),
                (CandidateFields.SKILL.value, skills),
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

    def get_phone(self, css_selector:str, err:str) -> str:
        """
        Funcion para obtener el numero telefonico
        """

        phone_btn = self.scraper.get_element(css=css_selector)
        phone_btn.click()

        return self.get_prop(css_selector=self.css_selectors.PHONE, err=err)

    def get_address(self, css:str, err:str) -> str:
        """
        Funcion para obtener la direccion de la persona
        """

        address_container = self.get_list_of_prop(css_selector=css, err=err)
        return address_container[0] if len(address_container) == 1 else address_container[1]
    
    def get_additional_information(self, css) -> list[str]:
        """
        Funcion para obtener informacion adicional como:
        experiencia, educacion, habilidades
        """
        experiences = []
        studies = []
        skills = []

        info = self.scraper.get_elements(self.css_selectors.ADDITIONAL_INFORMATION)
        for ele in info:
            btn = self.scraper.get_element(css="button", web_element=ele)
            btn_text = btn.text if btn else ""

            if btn_text == "Experience":
                div = self.scraper.get_element(css="div", web_element=ele)
                experiences = div.text
            elif btn_text == "Education":
                div = self.scraper.get_element(css="div", web_element=ele)
                studies = div.text
            elif btn_text == "Skills":
                div = self.scraper.get_element(css="div", web_element=ele)
                skills = div.text

        return (experiences, studies, skills)    
    
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