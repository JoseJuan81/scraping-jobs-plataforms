class IndeedCssSelectors:
    def __init__(self) -> None:
        """Funcion para iniciar clase ComputrabajoCssSelectors"""

        self.EMAIL_INPUT = "input[type='email']"
        self.CONTINUE_BTN = "button[type='submit']"
        # self.PASSWORD_INPUT = "input[name='Password']"

        self.FIRST_CANDIDATE = "div[data-testid='candidateListLayout'] table tbody tr"
        self.CANDIDATES = "li[data-testid='CandidateListItem']"

        self.NAME = "span[data-testid='namePlate-candidateName']"
        self.PHONE_BTN = "div#fullActionButtons button[aria-haspopup]"
        self.PHONE = "div[data-testid='call-modal-body'] div:nth-child(2) div div:nth-child(2) span"
        self.EMAIL = "a#namePlate-candidate-email"
        self.ADDRESS_CONTAINER = "div#candidateProfileContainer > div:nth-child(3) > div:nth-child(2) > div > div"
        self.ADDITIONAL_INFORMATION = "div#candidateProfileContainer > div:last-child > div"
        # iterar  sobre cada contenedor y obtener el texto de cada boton y si cumple con la condicion
        # obtener el hermano que es un div. De esta manera obtengo "experiencias, educacion y habilidades"

        self.LOAD_MORE = "button#fetchNextCandidates"