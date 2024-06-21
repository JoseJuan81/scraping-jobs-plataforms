import requests

from pathlib import Path

class ExternalApi:
    def __init__(self):
        self.file_path:Path = None

    def set_path_file(self, file_path:Path = Path()):
        """Funcion para establecer file_path"""

        self.file_path = file_path

    def send(self, url:str = ""):
        """Funcion para enviar informacion a una api externa"""

        if not self.file_path:
            print("No esta definida la ubicacion del archivo con la data")
            return False

        with open(self.file_path, 'rb') as f:
            archivos = { 'file': f }

            response = requests.post(url=url, files=archivos)

            if response.status_code == 200:
                print("Achivo enviado exitosamente")
            else:
                print("Error al enviar el archivo. Codigo de estado: ", response.status_code)
