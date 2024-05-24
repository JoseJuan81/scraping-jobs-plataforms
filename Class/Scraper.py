from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement

class Scraper:
    """Clase que realiza el scraping de los candidatos de un anuncio de empleo en computrabajo"""

    def __init__(self) -> None:
        self.driver: webdriver = None
        self.candidates: list = []
        self.next_button: webdriver.Remote._web_element_cls = None
        self.ghl_contacts: list[dict] = []
        self.external_api: str = ""
        self.job_position: str = ""

    def init(self) -> None:
        """Inicio del webdriver para hacer scraper"""

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def login(self,
              url_page:str = "",
              user:str = "",
              password:str = "",
              email_css_selector:str = "",
              password_css_selector:str = "",
              btn_css_selector:str = "") -> None:
        """Inicio de sesión"""

        self.driver.get(url_page)

        input_email = self.get_element(email_css_selector, self.driver)
        input_pass = self.get_element(password_css_selector, self.driver)

        input_email.send_keys(user)
        input_pass.send_keys(password)

        btn = self.get_element(btn_css_selector, self.driver)
        btn.click()

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
