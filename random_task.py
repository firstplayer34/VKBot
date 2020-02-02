import requests

class Task:
    def __init__(self):
        pass

def get_task_number(text):
    import re
    from patterns import TASK_NUMBER_PATTERN as tnp
    return re.findall(tnp, text)[0]

test = requests.get("https://inf-ege.sdamgia.ru/problem?id=16380")

def format_task(number):
    from bs4 import BeautifulSoup
    soup  = BeautifulSoup(test.text, "html.parser")
    task_number = soup.find(class_ = 'prob_nums').get_text()
    task = soup.find('p',class_ = "left_margin").get_text()
    print(get_task_number(task_number))
    print(task)

if __name__ == "__main__":
    import random