import pandas as pd

from TimetableBot.settings import BASE_DIR
import os


def read_timetable(path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(path, skiprows=17)
        # df.drop(df.head(1).index, inplace=True)
        return df
    except Exception:
        return "Выбран не подходящий файл"


if __name__ == "__main__":
    path = os.path.join(BASE_DIR, "actual_timetable.xlsx")
    tt = read_timetable(path=path)
    print(tt)
