import os
import requests

from dotenv import load_dotenv

from helper.ghl import build_ghl_data
from helper.constant import CandidateFields

load_dotenv()

GHL_URL = os.getenv("GHL_URL")


class GoHighLevel:
    def __init__(self, candidate: dict = {}) -> None:
        self.candidate = candidate
        self.custom_fields: dict = {}

    def send(self) -> None:
        """Función para enviar contacto a Go High Level"""

        _candidate = build_ghl_data(self.candidate)

        try:
            res = requests.post(GHL_URL, json=_candidate)

            print("&&"*50)
            print("Resultado satisfactorio al crear contactos en GHL")
            print(res.json())
            print("&&"*50)

        except Exception as error:
            print("&&"*50)
            print(
                f"Error al enviar contacto a GHL ({self.candidate[CandidateFields.NAME.value]})")
            print(error)
            print("&&"*50)
