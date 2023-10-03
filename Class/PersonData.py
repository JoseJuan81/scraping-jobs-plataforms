from helper.selenium import get_element
from helper.css_selector import CANDIDATE_NAME, CANDIDATE_IMG, CANDIDATE_PROFILE_PAGE, CANDIDATE_MATCH
from helper.css_selector import CANDIDATE_APLICATION_TIME, CANDIDATE_AGE, CANDIDATE_GRADE


class PersonData:
    def __init__(self, web_element) -> None:
        self.web_element = web_element

    def name(self) -> str:
        """Función para extraer el nombre del candidato"""

        _name = get_element(CANDIDATE_NAME, self.web_element)
        return _name.text if _name else "Sin Nombre"

    def image(self) -> str:
        """Función para extraer la imagen del candidato"""

        _image = get_element(CANDIDATE_IMG, self.web_element)
        return _image.get_attribute("src") if _image else "Sin Imagen"

    def profile_page(self) -> str:
        """Función para extraer la url del perfil del candidato"""

        _profile_page = get_element(CANDIDATE_PROFILE_PAGE, self.web_element)
        return _profile_page.get_attribute("href") if _profile_page else "Sin perfil de usuario"

    def application_time(self) -> str:
        """Función para extraer el tiempo en que aplicó al puesto el candidato"""

        _time = get_element(CANDIDATE_APLICATION_TIME, self.web_element)
        return _time.text if _time else "Sin Tiempo"

    def age(self) -> int:
        """Función para extraer la edad del candidato"""

        _old = get_element(CANDIDATE_AGE, self.web_element)
        return int(_old.text) if _old else 0

    def grade(self) -> str:
        """Función para extraer nivel de estudios del candidato"""

        _grade = get_element(CANDIDATE_GRADE, self.web_element)
        return _grade.text if _grade else "Sin estudios"

    def match(self) -> str:
        """Función para extraer el match del candidato al puesto de trabajo"""

        _match = get_element(CANDIDATE_MATCH, self.web_element)
        return _match.text if _match else "Sin match"
