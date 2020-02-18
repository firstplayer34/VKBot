from botCode.patterns import REQUEST_URL, SOURCE
import re
from bs4 import BeautifulSoup
import requests
import random
import botCode.utilites as utilites

class Task:
    def __init__(self, number):
        """
        params: 

            number : Номер задания(В случае отстутствия передаётся None)

        description: 

            Создаёт объект задания.

            Поля:
                number: Номер задания, как на сайте (пример: 6567)
                url: Ссыла на задание
                text: Текст задания
                task_number: ??? (Должен быть порядковый номер в варианте (например, задание 22))
                answer: Ответ на задание (пример: Ответ: 123)

        """
        self.number = number
        if self.number is None:
            self.number = random.randint(1,10000)
            while self.isExisting() is False: #перебор номеров до тех пор, пока не попадём на существующее
                self.number = random.randint(1,10000)
        self.url = REQUEST_URL+str(self.number)
        self.text = self.get_task_text().replace("\xad","") #в некоторых заданиях есть символы, похожие на пробелы
        self.text = utilites.format_choise_task(self.text) #Если задание с выбором ответа, то добавление переноса строки перед вариантами ответа
        self.find_answer()
        self.source = SOURCE

        #TODO: Проработать задания с выбором ответа, когда есть, например, несколько отрывков текста и они помечены буквами
        
        try:
            self.get_task_number()
        except IndexError:
            self.__init__(None)

    def isExisting(self):

        """
        Проверяет существование созданного задания в __init__ на сайте
        """

        page_text = requests.get(REQUEST_URL+str(self.number)).text 
        if "Такого задания не существует." in page_text:
            return False
        else:
            return True  

    def get_task_text(self):
        """

        Использует BeautifulSoup для поиска в теге текста задания

        """
        request_text = requests.get(self.url).text #получение html кода страницы с заданием
        soup = BeautifulSoup(request_text, "html.parser")
        return soup.find('p', class_ = "left_margin").get_text()


    def get_task_number(self):
        """
        
        Использует BeautifulSoup для поиска номера задания 
        
        """
        request_text = requests.get(self.url).text
        soup = BeautifulSoup(request_text, "html.parser")
        task_number = soup.find('p', class_ = "left_margin").get_text()
        self.task_number = utilites.get_numbers(task_number)[0]

    def find_answer(self):
        """

        Ищут ответ на странице прямым поиском без использования BeatufulSoup

        """
        task_text = requests.get(self.url).text
        if "Ответ: " in task_text:
            task_answer = task_text.rfind("Ответ:")
            end_answer = task_text[task_answer:].find('<')
            self.answer = task_text[task_answer:task_answer+end_answer]
        else:
            self.answer = "Ответ на задание недоступен"


    def __repr__(self):
        s = ""
        s+=self.text+'\n'
        s+=self.source
        return s

if __name__ == "__main__":
    test = Task(7643)
    print(test.url)
    print(test.answer)