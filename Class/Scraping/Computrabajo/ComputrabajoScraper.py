import os

from typing import Generator

from selenium.webdriver.remote import webelement

from Class.Scraper import Scraper
from Class.Scraping.Computrabajo.ComputrabajoCssSelectors import ComputrabajoCssSelectors
from Class.ExternalApi import ExternalApi

from helper.file import save_candidates
from helper.constant import CandidateFields

USER_EMAIL = os.getenv("COMPUTRABAJO_USER_EMAIL")
USER_PASS = os.getenv("COMPUTRABAJO_USER_PASSWORD")
LOGIN_PAGE = os.getenv("COMPUTRABAJO_URL_LOGIN")
JOB_PAGE = os.getenv("COMPUTRABAJO_JOB_PAGE")

class ComputrabajoScraper:
    def __init__(self) -> None:
        self.scraper:Scraper = Scraper()
        self.css_selectors:ComputrabajoCssSelectors = ComputrabajoCssSelectors()
        self.API = ExternalApi()
        self.pagination:int = 1
        self.candidates:list = list()
        self.candidates_webelements:list[webelement] = list()
        self.job_position:str = "asistente_marketing"
        self.job_plataform:str = "Bumeran"

    def start_browser(self) -> None:
        """Iniciar el navegador"""

        print("Iniciando navegador...")
        self.scraper.init()

    def login(self) -> None:
        """Funcion para iniciar sesion en bumeran"""

        print("Ingresando a la cuenta...")
        self.scraper.login(
            url_page=LOGIN_PAGE,
            user=USER_EMAIL,
            password=USER_PASS,
            email_css_selector=self.css_selectors.EMAIL_INPUT,
            password_css_selector=self.css_selectors.PASSWORD_INPUT,
            btn_css_selector=self.css_selectors.BTN_INGRESAR,
        )

    def job_post(self) -> None:
        """Funcion para ir a la pagina del aviso publicado"""

        self.scraper.driver.get(JOB_PAGE)
        input("\nCerrar modales de anuncios para continuar\n")

    def start_scraping(self) -> None:
        """Funcion para hacer scraping de los candidatos que postularon"""

        print("Extrayendo candidatos...")
        self.get_candidates()
        
        print("Iterando los candidatos...")
        candidates_generator = self.loop_candidates()
        
        print("Extrayendo informacion de cada candidato...")
        candidate_generator = self.extract_candidate_data(candidates_generator)

        for candidate in candidate_generator:
            print(f'Datos de {candidate["name"]} guardados en variable self.candidates')
           
            self.candidates.append(candidate)

    def get_candidates(self) -> None:
        """Funcion para obtener listado de postulantes de la pagina"""

        self.candidates_webelements = self.scraper.get_elements(css=self.css_selectors.CANDIDATES)

    def loop_candidates(self) -> Generator[any, any, any]:
        """Funcion que recorre uno a uno postulantes"""

        for candidate in self.candidates_webelements:
            yield candidate

        _, file_path = save_candidates(self.candidates, self.job_position)
        self.API.set_path_file(file_path=file_path)
        self.next_page()

    def extract_candidate_data(self, candidates_generator) -> Generator[dict, any, any]:
        """Funcion que retorna la informacion del postulante"""

        for candidate in candidates_generator:
            print("Iniciando extraccion de datos por postulante")

            candidate.click()
            # time.sleep(2)

            name = self.get_prop(css_selector=self.css_selectors.NAME, err="Sin Nombre")
            phone = self.get_prop(self.css_selectors.PHONE, err="Sin telefono")
            email = self.get_prop(self.css_selectors.EMAIL, err="Sin correo")
            dni = self.get_prop(self.css_selectors.DNI, err="Sin DNI")
            address = self.get_prop(self.css_selectors.ADDRESS, err="Sin Direccion")
            age = self.get_prop(self.css_selectors.AGE, err="Sin Edad")
            experience = self.get_list_of_prop(self.css_selectors.EXPERIENCE, err="Sin Experiencia")
            study = self.get_list_of_prop(self.css_selectors.STUDY, err="Sin Estudios")
            skills = self.get_list_of_prop(self.css_selectors.SKILLS, err="Sin Habilidades")

            candidate = dict([
                (CandidateFields.NAME.value, name),
                (CandidateFields.PHONE.value, phone),
                (CandidateFields.EMAIL.value, email),
                (CandidateFields.DNI.value, dni),
                (CandidateFields.ADDRESS.value, address),
                (CandidateFields.AGE.value, age),
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

    def next_page(self) -> None:
        """Funcion para presionar botones de paginacion"""

        current_page = self.scraper.get_element(self.css_selectors.ACTIVE_PAGE).text
        total_pages_list = self.scraper.get_elements(self.css_selectors.PAGINATION_TOTAL_PAGE)
        total_pages = total_pages_list[-3].text

        if current_page != total_pages:
            next_page = total_pages_list[-2]
            next_page.click()
