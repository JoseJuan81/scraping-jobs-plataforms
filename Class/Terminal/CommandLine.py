import json
import argparse
import sys

from pathlib import Path

class CommandLine:
    def __init__(self):
        
        config_file, process_name, company_name = self.get_terminal_input()
        file = self.get_config_file_path(config_file=config_file)
        user_email, user_pass, login_url, job_url = self.get_config_file_data(file_path=file, process_name=process_name, company_name=company_name)

        self.user_email:str = user_email
        self.user_pass:str = user_pass
        self.login_url:str = login_url
        self.job_url:str = job_url
        self.process_name:str = process_name

    def get_config_file_data(self, file_path:Path = Path(), process_name:str = "", company_name:str = "") -> tuple:
        """Funcion que retorna los valores introducidos por el usuario en la terminal y las credenciales de la compania"""

        with open(file_path, 'r') as config_file:
            config = json.load(config_file)

        company_data = config[company_name]
        (_, user_email), (_, user_pass) = company_data["company_credentials"].items()
        login_url = company_data["loginUrl"]
        job_url = company_data["processes"][process_name.lower()]

        return (user_email, user_pass, login_url, job_url)

    def get_config_file_path(self, config_file:str = "") -> Path:
        """Funcion para obtener la ruta completa del archivo de configuracion"""

        current_folder = Path.cwd()
        return Path(current_folder, Path("config", config_file))

    def get_terminal_input(self) -> tuple:
        """Funcion para obtener los datos que el usuario introdujo desde la terminal"""

        parser = argparse.ArgumentParser()
        parser.add_argument("--company_name", help="Nombre compania a usar")
        parser.add_argument("--config_file", help="Nombre archivo de configuracion")
        parser.add_argument("--process_name", help="Nombre del proceso o puesto de trabajo")
        args = parser.parse_args()

        company_name = args.company_name
        config_file = args.config_file
        process_name = args.process_name

        if not company_name:
            sys.exit("Es necesario el nombre de la compania para ejecutar el scraping")

        if not config_file:
            sys.exit("Es necesario definir el archivo de configuracion para ejecutar el scraping")

        if not process_name:
            sys.exit("Es necesario definir el puesto de trabajo para ejecutar el scraping")

        return (config_file, process_name, company_name)