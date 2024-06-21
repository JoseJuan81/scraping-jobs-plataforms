import re
from selenium.webdriver.remote import webelement

class ComputrabajoPersonData:
    def __init__(self, scraper, css_selectors) -> None:
        self.scraper = scraper
        self.css_selectors = css_selectors
        self.left_side = scraper.get_elements(css_selectors.LEFT_SIDE)
        self.right_side = scraper.get_elements(css_selectors.RIGHT_SIDE)

    def image(self):
        """
        Funcion para obtener la imagen del candidato
        """
        image = self.get_prop(css_selector=self.css_selectors.IMAGE, err="Sin Imagen", attribute="src")
        return image

    def name(self):
        """
        Funcion para obtener el nombre del candidato
        """
        _name = self.get_prop(css_selector=self.css_selectors.NAME, err="Sin Nombre")
        name = _name[14:]
        print(f'Nombre: {name}')
        return name
    
    def phone(self):
        """
        Funcion para obtener el telefono del candidato
        """
        phone = self.find_one_by_re(
            default_msg="Sin Telefono",
            patron=r'\b(?:\+?51(?:\s|-)?(?:\d(?:\s|-)?\d{7}|\d{2}(?:\s|-)?\d{3}(?:\s|-)?\d{3})|(?:51(?:\s|-)?\d{9}))\b',
            parent=self.left_side
        )
        
        return phone
    
    def email(self):
        """
        Funcion para obtener el correo del candidato
        """
        email = self.find_one_by_re(
            default_msg="Sin correo",
            patron=r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            parent=self.left_side
        )
        
        return email
    
    def dni(self):
        """
        Funcion para obtener el DNI del candidato
        """
        dni = self.find_one_by_re(
            default_msg="Sin DNI",
            patron=r'\b(?<!\d)(?:\d{8}|\d{9})(?!\d)\b',
            parent=self.left_side
        )
        
        return dni
    
    def address(self):
        """
        Funcion para obtener la direccion del candidato
        """
        address = self.find_one_by_re(
            default_msg="Sin Direccion",
            patron=r'[A-Za-z\s]+ / [A-Za-z\s]+',
            parent=self.left_side
        )
        
        return address
    
    def age(self):
        """
        Funcion para obtener la edad del candidato
        """
        age = self.find_one_by_re(
            default_msg="Sin Edad",
            patron=r'\b\d{1,3}\s*años\b',
            parent=self.left_side
        )
        
        return age
    
    def summary(self):
        """
        Funcion para obtener el resumen del candidato
        """
        summary = self.get_prop(css_selector=self.css_selectors.SUMMARY, err="Sin Resumen en perfil")
        return summary
    
    def experience(self):
        """
        Funcion para obtener la experiencia del candidato
        """

        exp = []
        lis = self.get_list_of_prop(css_selector=self.css_selectors.EXPERIENCE, err="Sin Experiencia")
        for l in lis:
            print(f'l: {l}')
            exp.append(l)
        
        return exp
    
    def study(self):
        """
        Funcion para obtener los estudios del candidato
        """
        study = self.get_list_of_prop(css_selector=self.css_selectors.STUDY, err="Sin Estudios")
        return study
    
    def skills(self):
        """
        Funcion para obtener los estudios del candidato
        """
        skills = self.get_list_of_prop(css_selector=self.css_selectors.SKILLS, err="Sin Habilidades")
        return skills
    
    def expectation(self):
        """
        Funcion para obtener la expectativa economica del candidato
        """
        money = self.find_one_by_re(
            default_msg="0",
            patron=r'\bS?S?\/?\.\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b',
            parent=self.left_side
        )
        
        return money
 
    def get_prop(self, css_selector:str = "", err:str = "", attribute:str = "text") -> str:
        """Funcion para extraer valor de una propiedad del postulante"""

        try:
            prop = self.scraper.get_element(css_selector)
            if attribute == "text":
                return prop.text
            else:
                return prop.get_attribute(attribute)
        except Exception as e:
            print(f"error en get_prop: {e}")
            return err
        
    def get_list_of_prop(self, css_selector:str = "", err:str = "") -> str:
        """Funcion para extraer valores de una propiedad del postulante"""

        try:
            text_list = self.scraper.get_elements(css_selector)
            return [t.text for t in text_list]
        except:
            return err
        
    def find_one_by_re(self, default_msg:str = "", patron:str = "", parent:webelement = None):
        """
        Funcion generica para obtener datos usando expresion regular
        """
        data = default_msg
        for el in parent:
            result = re.search(patron, el.text)
            if result and result.group():
                data = result.group()
                break
        
        return data