
def destructure_name(full_name: str) -> tuple[str]:
    """Función que recive un str y extrae el nombre y apellido"""
    print(full_name)
    if full_name == "":
        return ("", "")

    name_list = full_name.split(" ")
    name_len = len(name_list)

    if name_len == 2:
        name, last_name = name_list
        return (name, last_name)

    if name_len == 3:
        name, *_last_name = name_list
        last_name = " ".join(_last_name)
        return (name, last_name)

    if name_len == 4:
        f_name, s_name, f_last_name, s_last_name = name_list
        name = " ".join([f_name, s_name])
        last_name = " ".join([f_last_name, s_last_name])
        return (name, last_name)

    if name_len == 5:
        f_name, s_name, t_name, f_last_name, s_last_name = name_list
        name = " ".join([f_name, s_name, t_name])
        last_name = " ".join([f_last_name, s_last_name])
        return (name, last_name)

    if name_len >= 6:
        f_name, f_last_name, *rest = name_list
        name = f_name
        last_name = f_last_name
        return (name, last_name)


def extract_expectation_amount(expectation: str) -> str:
    """Función para extraer el valor del sueldo esperado por el candidato"""

    expectation_list = expectation.split(" ")
    amount = expectation_list[-1]
    return amount
