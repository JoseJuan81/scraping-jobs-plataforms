import os
import json
import requests

from dotenv import load_dotenv

from helper.ghl import build_ghl_data
from helper.constant import CandidateFields

load_dotenv()

GHL_URL = os.getenv("GHL_URL")
GHL_TOKEN = os.getenv("GHL_TOKEN")

class GoHighLevel:
    def __init__(self, candidate: dict = {}) -> None:
        self.candidate = candidate
        self.custom_fields: dict = {}
        self.tags: list[str] = []
        self.recruitment_platform: str = ""

        self.set_tags_in_candidate()

    def set_tags_in_candidate(self) -> None:
        """Funcion para agrgar la propiedad tags en candidate"""

        self.candidate.update({ "tags": [] })

    def set_tags(self, tags: list[str]) -> None:
        """Funcion que establece tags a agregar en cada candidato"""

        self.tags = tags
        self.candidate["tags"] += self.tags

    def set_recruitment_platform(self, platform: str) -> None:
        """Funcion que establece la plataforma que se esta scrapeando"""

        self.recruitment_platform = platform
        self.candidate["tags"] += [platform]

    def send(self) -> None:
        """Función para enviar contacto a Go High Level"""

        _candidate = build_ghl_data(self.candidate)
        headers = self.ghl_headers()

        try:
            res = requests.post(GHL_URL, headers=headers, json=_candidate)

            print("&&"*50)
            if res.status_code == 200:
                print("Resultado satisfactorio al crear contactos en GHL")
            else:
                print("Error al crear contacto en GHL")

            print(res.json())
            print("&&"*50)

        except Exception as error:
            print("&&"*50)
            print(
                f"Error al enviar contacto a GHL ({self.candidate[CandidateFields.NAME.value]})")
            print(error)
            print("&&"*50)

    def ghl_headers(self) -> dict:
        """Funcion que construye el header para enviar token de cuenta GHL"""

        headers = dict([
            ("Authorization", f"Bearer {GHL_TOKEN}"),
            ("Content-Type", "application/json")
        ])

        return headers
    
    def build_ghl_data(self, candidate: dict = {}) -> dict:
        """Función para transformar la data a la estructura de GHL"""
        pass