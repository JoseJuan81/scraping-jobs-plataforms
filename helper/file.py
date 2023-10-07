import pandas as pd

from pathlib import Path

from helper.constant import CandidateFields


def save_file_path() -> Path:
    """Función que retorna la ruta del archivo donde se guardaran los datos"""

    main_dir = Path().absolute()
    return Path(main_dir, "Scraping_computrabajo", "result", "data.csv")


def save_candidates(candidates: list) -> [dict]:
    """Función para guardar lista de candidatos scrapeados"""

    dt = pd.DataFrame.from_dict(candidates, orient="columns")

    _unusefull_data = dt[CandidateFields.NAME] != "Sin Nombre"
    dt = dt.loc[_unusefull_data]

    print("Contactos filtrados:")
    print(f"{len(dt.index)} contactos a guardar")
    print("=="*50)

    dt.to_csv(save_file_path(), index=False, header=True)

    return dt.to_dict(orient="records")
