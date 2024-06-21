import json
import argparse

from pathlib import Path

class UpdateConfigFiles:
    def __init__(self):
        
        json_file, process_name, job_page = self.get_terminal_input()
        file_path = self.get_config_file_path(config_file=json_file)
        self.update_config_file(json_file=file_path, process_name=process_name, job_page=job_page)

    def update_config_file(self, json_file:Path = Path(), process_name:str="", job_page:str="") -> None:
        """Funcion que actualiza el archivo json con los datos pasados como argumento"""

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
            
            data["processes"][process_name] = job_page
            
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
        parser.add_argument("--json_file", help="Nombre del archivo json a actualizar")
        parser.add_argument("--process_name", help="Nombre del puesto de trabajo")
        parser.add_argument("--job_page", help="Url de la pagina del puesto de trabajo")
        args = parser.parse_args()

        return (args.json_file, args.process_name, args.job_page)