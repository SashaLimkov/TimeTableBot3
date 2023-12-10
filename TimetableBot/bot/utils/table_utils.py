import pandas as pd
from bot.utils.group_num_validator import group_num_validator
from TimetableBot.settings import BASE_DIR
import os
from fuzzywuzzy import process
import re
from typing import Tuple, Dict
import datetime

class NotGroupNumStyle(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'NotGroupNumStyle, {self.message} '
        else:
            return 'NotGroupNumStyle has been raised'
            
    def get_message(self):
        return self.message

class GroupNotFound(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'GroupNotFound, {self.message} '
        else:
            return 'GroupNotFound has been raised'
            
    def get_message(self):
        return self.message
    


def read_timetable(path:str)->pd.DataFrame:
    skiprows = list(range(16))
    try:
        df = pd.read_excel(path, skiprows=lambda ind: ind in skiprows)
        df = df.fillna(0)
        return df
    except Exception:
        return "Выбран не подходящий файл"
    

def get_cleaned_group_names(df: pd.DataFrame) -> Tuple:
    pattern = r"\d\d-\d\d\d"
    result = []
    for col in df.columns:
        if res := re.search(pattern, col):
            result.append(res.string)
    return tuple(result)

def get_only_group_numbers(df: pd.DataFrame, cleaned_group_names: Tuple|None = None) -> Tuple:
    if cleaned_group_names is None:
        cleaned_group_names = get_cleaned_group_names(df=df)
    pattern = r"\d\d-\d\d\d"
    return tuple([re.search(pattern, group).group() for group in cleaned_group_names])

def get_groups_dict_by_group_numbers(df: pd.DataFrame, cleaned_group_names: Tuple|None = None) -> Dict:
    if cleaned_group_names is None:
        cleaned_group_names = get_cleaned_group_names(df=df)
    pattern = r"\d\d-\d\d\d"
    group_dict = {}
    for group in cleaned_group_names:
        g_data = re.search(pattern, group)
        group_num, group_full_name = g_data.group(), g_data.string 
        if group_dict.get(group_num):
            group_dict[group_num].append(group_full_name)
            continue
        group_dict.update({
            group_num:[group_full_name]
        })
    return group_dict

def get_group_num(user_input: str) -> bool:
    pattern = r"\d\d-\d\d\d"
    return re.search(pattern, user_input).group()

def get_founded_group_names(user_input:str, groups_dict: dict)-> list[str]:
    if group_num_validator(user_input):
        g_num = get_group_num(user_input)
        if result := groups_dict.get(g_num):
            return result
        raise GroupNotFound(f"Введенный номер группы - {g_num}, не найден в рассписании")
    else:
        raise NotGroupNumStyle("Введен неверный формат номера группы.\nНомер должен быть вида XX-XXX,  например 01-001")


def get_today_weekday():
    date = datetime.datetime.today()
    weekday_number = date.weekday()
    weekday_names = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', "воскресенье"]
    weekday_name = weekday_names[weekday_number]
    return weekday_name

def get_weekday_rows(df:pd.DataFrame)->Dict[str, list]:
    df = df[["1 курс", "1 курс.1"]]
    day_dict:[str, list] = {}
    for row in df.itertuples():
        index, day = row[:2]
        if len(day)==2:
            continue
        if day_dict.get(day):
            day_dict[day].append(index)
        else:
            day_dict.update({
                day: [index]
            })
        if row[0] == 89:
            break
    return day_dict

def get_timetable_dict_by_group_and_day(df:pd.DataFrame, selected_group:str, selected_weekday:str, is_odd:bool = True)->Dict[str, set]:
    weekday_rows = get_weekday_rows(df=df)
    df = df[["1 курс", "1 курс.1", selected_group]]
    res = {}
    for row in df.itertuples():
        index, day, time, subj = row
        if index not in weekday_rows[selected_weekday] :
            continue
        if subj:
            subj = subj.strip()
            data = [time, subj]
            if is_odd and is_odd_subj(subj=subj.strip()):
                if res.get(time):
                    res[time].add(subj)
                else:
                    s = set()
                    s.add(subj)
                    res.update({
                        time: s
                    })
            elif not is_odd and is_even_subj(subj=subj.strip()):
                if res.get(time):
                    res[time].add(subj)
                else:
                    s = set()
                    s.add(subj)
                    res.update({
                        time: s
                    })
            if both(subj):
                if res.get(time):
                    res[time].add(subj)
                else:
                    s = set()
                    s.add(subj)
                    res.update({
                        time: s
                    })
        if row[0] == 89:
            break
    return res

def is_odd_subj(subj: str)-> bool:
    return "н/н" in subj  

def is_even_subj(subj: str)-> bool:
    return "ч/н" in subj 

def both(subj: str)-> bool:
    return not is_odd_subj(subj) and not is_even_subj(subj)

def get_dates_from_to(subj:str)->str:
    pattern = r"\d{2}\.\d{2}.\d{2}-\d{2}\.\d{2}.\d{2}"
    second_pattern = r"\(\d+-\d+.{1,10}\)"
    res = re.search(pattern, subj)
    if res:
        return res.group()
    elif res := re.search(second_pattern, subj):
        return res.group()
    return "-"


def get_timetable_text(selected_weekday:str, tt_dict:dict[str,set])->str:
    text = f"{selected_weekday.capitalize()} рассписание:\n"
    for time, subjects in tt_dict.items():
        text += f"{time} :\n"
        for sub in subjects:
            text += f"\t{sub}\n"
        text+="\n"
    if not tt_dict.items():
        text+="Пар нет"
    return text

def get_main_df():
    path = os.path.join(BASE_DIR, "fixed.xlsx")
    tt_df = read_timetable(path=path)
    return tt_df

def get_today_tt(selected_group:str):
    df = get_main_df()
    selected_weekday = get_today_weekday()
    if selected_weekday == "воскресенье":
        return "В воскресенье нет пар"
    is_odd = get_today_is_odd()
    tt_dict = get_timetable_dict_by_group_and_day(df=df, selected_group=selected_group, selected_weekday=selected_weekday, is_odd=is_odd) 
    return get_timetable_text(selected_weekday=selected_weekday, tt_dict=tt_dict)

def get_tt(selected_group:str, selected_weekday:str, is_odd:int):
    df = get_main_df()
    tt_dict = get_timetable_dict_by_group_and_day(df=df, selected_group=selected_group, selected_weekday=selected_weekday, is_odd=is_odd)
    return get_timetable_text(selected_weekday=selected_weekday, tt_dict=tt_dict)

def get_today_is_odd():
    return datetime.date.today().isocalendar()[1] % 2 == 1


def get_today_is_odd_txt():
    return "Нечетная" if get_today_is_odd else "Четная"