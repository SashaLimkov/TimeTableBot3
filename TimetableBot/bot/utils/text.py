from backend.models import Text
from backend.services.text import get_text_by_language_and_key


def get_text(key:str, lang:Text.Language):
    return get_text_by_language_and_key(key=key, lang=lang)