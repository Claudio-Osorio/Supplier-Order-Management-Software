import re

# Validates input by rejecting strings that could cause sql injection
def validate_by_regex(input_string, regex_rule):
    regex = re.compile(regex_rule)
    if re.fullmatch(regex, input_string):
      return True
    return False

def validate_email(input_string):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]'
                       r'+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, input_string):
        return True
    return False

def validate_phone(input_string):
    regex = re.compile(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??"
                       r"\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})")
    if re.fullmatch(regex, input_string):
        return True
    return False

def validate_address(input_string):
    regex = re.compile(r"^[A-Za-z0-9\s,#]*")
    if re.fullmatch(regex, input_string):
        return True
    return False

def validate_amount(input_string):
    regex = re.compile(r"^[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}")
    if re.fullmatch(regex, input_string):
        return True
    return False

def validate_date(input_string):
    try:
        regex = re.compile(r"^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/(?=20\d{2})\d{4}$")
        if re.fullmatch(regex, input_string):
            return True
        return False
    except ValueError:
        return False

def validate_all_numbers(input_string):
    regex  = re.compile(r"^[0-9]{1,9}")
    if re.fullmatch(regex, input_string):
        return True
    return False

def blank_input(input_string):
    if input_string.isspace() or \
            input_string == "":
        return True
    return False