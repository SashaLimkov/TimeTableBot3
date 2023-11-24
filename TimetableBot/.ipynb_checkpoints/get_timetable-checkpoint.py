import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def write_raw_xlsx_timetable(url:str, headers: dict):
    response = requests.get(url=url, headers=headers)
    with open("actual_timetable.xlsx", "wb") as file:
        file.write(response.content)

def get_actual_timetable():
    url = "https://kpfu.ru/computing-technology/raspisanie"
    ua = UserAgent()
    user_agent = ua.random
    headers = {
        "User-Agent": user_agent
    }
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text)
    selector = "div.visit_link > p:nth-child(3) > a"
    xlsx_url = soup.select_one(selector=selector).get("data-cke-saved-href")
    write_raw_xlsx_timetable(url=xlsx_url, headers=headers)

# if __name__ == "__main__":
#     get_actual_timetable()