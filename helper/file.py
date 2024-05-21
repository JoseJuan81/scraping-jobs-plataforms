import pandas as pd

from pathlib import Path

from helper.constant import CandidateFields


def save_file_path(file_name: str = "", file_extension:str = "csv") -> Path:
    """Función que retorna la ruta del archivo donde se guardaran los datos"""

    main_dir = Path().absolute()
    _file_name = f"{file_name}.{file_extension}"
    return Path(main_dir, "result", _file_name)

def convert_data_into_dt(candidates) -> pd.DataFrame:
    """Funcion que transforma la lista de dict en un dataframe"""

    return pd.DataFrame.from_dict(candidates, orient="columns")

def filtering_dt(dt) -> pd.DataFrame:
    """Funcion que filtra los datos obtenidos"""

    _unusefull_data = dt[CandidateFields.NAME.value] != "Sin Nombre"
    dt = dt.loc[_unusefull_data]
    return dt

def save_candidates(candidates: list, file_name: str) -> list[dict]:
    """Función para guardar lista de candidatos scrapeados"""

    dt = convert_data_into_dt(candidates)
    dt = filtering_dt(dt)

    print("Contactos filtrados:")
    print(f"{len(dt.index)} contactos a guardar")
    print("=="*50)
    
    save_path = save_file_path(file_name=file_name, file_extension="csv")
    if save_path.exists():
        dt.to_csv(save_path, index=False, mode="a", header=False)
    else:
        dt.to_csv(save_path, index=False, mode="a")


    return (dt.to_dict(orient="records"), save_path)
