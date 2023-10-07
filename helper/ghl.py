from helper.utils import destructure_name
from helper.constant import CandidateFields

from pydantic import BaseModel
from typing import Union

GHL_APP = "ghl"


class GHLContactModel(BaseModel):
    address1: Union[str, None] = ""
    custom_field: Union[dict, None] = {}
    email: str
    firstName: str
    lastName: str
    phone: str
    source: str = "computrabajo_scrapper"


def build_ghl_data(candidate: dict = {}) -> dict:
    """Función para transformar la data a la estructura de GHL"""

    first_name, last_name = destructure_name(candidate[CandidateFields.NAME])
    custom_fields = build_custom_fields(candidate)

    _data = dict([
        ("email", candidate[CandidateFields.EMAIL]),
        ("firstName", first_name),
        ("lastName", last_name),
        ("phone", candidate[CandidateFields.PHONE]),
        ("address1", candidate[CandidateFields.CITY]),
        ("customFields", custom_fields),
        ("tags", ["Digital Disruptor", "scrapping computrabajo", "JJ81"])
    ])

    data = GHLContactModel(**_data)
    return data.model_dump()


def build_custom_fields(candidate: dict) -> dict:
    """Función para construir campos personalizado para GHL"""

    data = dict([
        ("contact.dni", candidate[CandidateFields.DNI]),
        ("contact.expectativa_salarial",
         candidate[CandidateFields.EXPECTATION]),
        ("contact.resumen_personal",
         candidate[CandidateFields.PERSONAL_SUMMARY]),
        ("contact.experiencia_laboral",
         candidate[CandidateFields.WORK_EXPERIENCE]),
    ])

    return data
