from backend.models import Text


def get_text_by_language_and_key(lang: Text.Language, key: str) -> Text.Translate:
    print(key)
    if key is None:
        return "Нет текста"
    text_key = Text.Text.objects.filter(key=key).first()
    return (
        Text.Translate.objects.filter(text_key=text_key, language=lang)
        .first()
        .translate
    )


def get_key_by_text(text: str):
    return Text.Translate.objects.filter(translate=text).first().text_key.key


def get_translate_by_text(text: str) -> Text.Translate:
    return


def get_default_language():
    return Text.Language.objects.first()


def get_all_languages():
    return Text.Language.objects.all()


def get_language_by_name(lang_name: str) -> Text.Language:
    return Text.Language.objects.filter(name=lang_name).first()
