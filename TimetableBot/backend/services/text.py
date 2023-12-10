import json
import os
from TimetableBot.settings import BASE_DIR
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


def create_data_json():
    data = {}
    for text_key in Text.Text.objects.all():
        name = text_key.key
        ru_l = Text.Language.objects.filter(name="Русский язык").first()
        rus_translate = text_key.all_translates.filter(language=ru_l).first().translate
        data.update({
            name:{
                "Русский язык":rus_translate
            }
        })
    with open('text_result.json', 'w') as fp:
        json.dump(data, fp)

def fill_text():
    f = open(os.path.join(BASE_DIR, 'text_result.json'))
    data = json.load(f)
    for k, v in data.items():
        t = Text.objects.create(key=k)
        t.save()
        for lang_code, text in v.items():
            lang = get_language_by_name(lang_name=lang_code)
            r = Text.Translate.objects.create(text_key=t, language=lang, translate=text)
            r.save()

