import json
from helper.utils import destructure_name
from helper.constant import CandidateFields

from pydantic import BaseModel
from typing import Union

GHL_APP = "ghl"


class GHLContactModel(BaseModel):
    address1: Union[str, None] = ""
    email: str
    firstName: str
    lastName: str
    phone: str
    source: str = "computrabajo_scrapper"
    tags: Union[list[str], None] = []
    city: Union[str, None] = ""
    customField: Union[dict, None] = {}


def build_ghl_data(candidate: dict = {}) -> dict:
    """Función para transformar la data a la estructura de GHL"""

    first_name, last_name = destructure_name(
        candidate[CandidateFields.NAME.value])
    custom_field = build_custom_fields(candidate)

    _data = dict([
        ("email", candidate[CandidateFields.EMAIL.value]),
        ("firstName", first_name),
        ("lastName", last_name),
        ("phone", candidate[CandidateFields.PHONE.value]),
        ("address1", candidate[CandidateFields.CITY.value]),
        ("customField", custom_field),
        ("tags", candidate[CandidateFields.TAGS.value])
    ])

    data = GHLContactModel(**_data)
    return data.dict()


def build_custom_fields(candidate: dict) -> dict:
    """Función para construir campos personalizado para GHL"""

    # todo esto debe ir en la clase GHL
    # asi como tambien los enums

    data = dict([
        ("dni", candidate[CandidateFields.DNI.value]),
        ("expectativa_salarial",
         candidate[CandidateFields.EXPECTATION.value]),
        ("resumen_personal",
         candidate[CandidateFields.PERSONAL_SUMMARY.value]),
        ("experiencia_laboral",
         candidate[CandidateFields.WORK_EXPERIENCE.value]),
    ])

    return data
