import json
import argparse
import sys

from pathlib import Path

class UpdateConfigFiles:
    def __init__(self):
        
        json_file, process_name, job_page, company_name = self.get_terminal_input()
        file_path = self.get_config_file_path(config_file=json_file)
        self.update_config_file(json_file=file_path, process_name=process_name, job_page=job_page, company_name=company_name)

    def update_config_file(self, json_file:Path = Path(), process_name:str="", job_page:str="", company_name:str="") -> None:
        """Funcion que actualiza el archivo json con los datos pasados como argumento"""

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
            
            data[company_name]["processes"][process_name] = job_page
            
            with open(json_file, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"La clave '{process_name}' ha sido actualizada o agregada en el archivo '{json_file}'.")
        except FileNotFoundError:
            print(f"El archivo '{json_file}' no existe.")
        except json.JSONDecodeError:
            print(f"El archivo '{json_file}' no es un archivo JSON válido.")
        except Exception as e:
            print(f"Se produjo un error: {e}")

    def get_config_file_path(self, config_file:str = "") -> Path:
        """Funcion para obtener la ruta completa del archivo de configuracion"""

        current_folder = Path.cwd()
        return Path(current_folder, Path("config", config_file))

    def get_terminal_input(self) -> tuple:
        """Funcion para obtener los datos que el usuario introdujo desde la terminal"""

        parser = argparse.ArgumentParser()
        parser.add_argument("--company_name", help="Nombre del archivo json a actualizar")
        parser.add_argument("--config_file", help="Nombre del archivo json a actualizar")
        parser.add_argument("--process_name", help="Nombre del puesto de trabajo")
        parser.add_argument("--job_page", help="Url de la pagina del puesto de trabajo")
        args = parser.parse_args()

        company_name = args.company_name
        config_file = args.config_file
        process_name = args.process_name
        job_page = args.job_page

        if not company_name:
            sys.exit("Es necesario el nombre de la compania para ejecutar el scraping")

        if not config_file:
            sys.exit("Es necesario definir el archivo de configuracion para ejecutar el scraping")

        if not process_name:
            sys.exit("Es necesario definir el puesto de trabajo para ejecutar el scraping")

        if not job_page:
            sys.exit("Es necesario definir la url del puesto de trabajo para ejecutar el scraping")

        return (config_file, process_name, job_page, company_name)