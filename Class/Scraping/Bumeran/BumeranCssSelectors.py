class BumeranCssSelectors:
    def __init__(self) -> None:
        """Funcion para iniciar clase BumeranCssSelectors"""

        self.EMAIL_INPUT = "input#user"
        self.PASSWORD_INPUT = "input#password"
        self.BTN_INGRESAR = "button#ingresar"

        self.CANDIDATES = "div.card-listadocv div.resumen-cv"

        self.NAME = "div.datospersonales h3 div.title-cv-adquirido"
        self.PHONE = "div.datospersonales div.number a.numero-whatsapp"
        self.EMAIL = "div.datospersonales div.mail > a"
        self.AGE = "div.datospersonales span[title='DATOS USUARIO'] + span"
        self.DNI = "div.datospersonales span[title='DNI'] + span"
        self.ADDRESS = "div.datospersonales div:nth-child(8)"
        self.EXPERIENCE = "div#main-experiencia > div"
        self.STUDY = "div#main-estudios > div"
        self.SKILLS = "div.skills-categories ul li"
        self.ACTIVE_PAGE = "div.pagination ul li a.active"
        self.PAGINATION_TOTAL_PAGE = "div.pagination ul li"