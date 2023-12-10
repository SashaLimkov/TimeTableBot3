import re


def group_num_validator(user_input: str) -> bool:
    pattern = r"\d\d-\d\d\d"
    return True if re.search(pattern, user_input) else False

