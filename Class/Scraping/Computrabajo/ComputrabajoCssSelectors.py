class ComputrabajoCssSelectors:
    def __init__(self) -> None:
        """Funcion para iniciar clase ComputrabajoCssSelectors"""

        self.EMAIL_INPUT = "input#UserName"
        self.PASSWORD_INPUT = "input[name='Password']"
        self.BTN_INGRESAR = "input[type='submit']"

        self.CANDIDATES = "article.rowuser.pos_rel.bClick.no_icons li.nombre a"

        self.NAME = "article header h1"
        self.PHONE = "article#candidato div ul li:nth-child(3) > span"
        self.EMAIL = "article#candidato div ul li:nth-child(1) > span"
        self.AGE = "article#candidato div ul li:nth-child(5) > span"
        self.DNI = "article#candidato div ul li:nth-child(2) > span"
        self.ADDRESS = "article#candidato div ul li:nth-child(4) > span"
        self.EXPERIENCE = "article#candidato div:nth-child(3) > ul li"
        self.STUDY = "article#candidato div:nth-of-type(2) div:nth-of-type(4) ul:nth-of-type(1)"
        self.SKILLS = "span.tag.big.bg_premium"

        self.NEXT_PAGE = "nav.pag_numeric a.b_next"