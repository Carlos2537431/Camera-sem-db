def is_valid_plate(plate):
    regex_mercosul = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")
    regex_antigo = re.compile(r"^[A-Z]{3}[0-9]{4}$")
    return bool(regex_mercosul.match(plate) or regex_antigo.match(plate))

def validate_and_normalize_plate(plate):
    plate = plate.upper().replace(" ", "").replace("-", "")
    if is_valid_plate(plate):
        return plate
    return None

def validate_plate_list(plates):
    return [validate_and_normalize_plate(plate) for plate in plates if validate_and_normalize_plate(plate) is not None]