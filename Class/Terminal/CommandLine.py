import json
import argparse

from pathlib import Path

class CommandLine:
    def __init__(self):
        
        config_file, process_name = self.get_terminal_input()
        file = self.get_config_file_path(config_file=config_file)
        user_email, user_pass, login_url, job_url = self.get_config_file_data(file_path=file, process_name=process_name)

        self.user_email:str = user_email
        self.user_pass:str = user_pass
        self.login_url:str = login_url
        self.job_url:str = job_url
        self.process_name:str = process_name

    def get_config_file_data(self, file_path:Path = Path(), process_name:str = "") -> tuple:
        """Funcion que retorna los valores introducidos por el usuario en la terminal y las credenciales de la compania"""

        with open(file_path, 'r') as config_file:
            config = json.load(config_file)

        (_, user_email), (_, user_pass) = config["company_credentials"].items()
        login_url = config["loginUrl"]
        job_url = config["processes"][process_name.lower()]

        return (user_email, user_pass, login_url, job_url)

    def get_config_file_path(self, config_file:str = "") -> Path:
        """Funcion para obtener la ruta completa del archivo de configuracion"""

        return Path("Class", "config", config_file)

    def get_terminal_input(self) -> tuple:
        """Funcion para obtener los datos que el usuario introdujo desde la terminal"""

        parser = argparse.ArgumentParser()
        parser.add_argument("--config_file", help="Nombre archivo de configuracion")
        parser.add_argument("--process_name", help="Nombre del proceso o puesto de trabajo")
        args = parser.parse_args()

        return (args.config_file, args.process_name)