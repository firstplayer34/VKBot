from patterns import REQUEST_URL
import re
from bs4 import BeautifulSoup
import requests
import random
import utilites

class Task:
    def __init__(self, number):
        
        self.number = number
        if self.number is None:
            self.number = random.randint(1,10000)
            while self.isExisting() is False:
                self.number = random.randint(1,10000)
        self.url = REQUEST_URL+str(self.number)
        self.text = self.get_task_text().replace("\xad","")
        self.text = utilites.format_choise_task(self.text)
        try:
            self.get_task_number()
        except IndexError:
            self.__init__(None)

    def isExisting(self):
        page_text = requests.get(REQUEST_URL+str(self.number)).text 
        if "Такого задания не существует." in page_text:
            return False
        else:
            return True  

    def get_task_text(self):
        request_text = requests.get(self.url).text
        soup = BeautifulSoup(request_text, "html.parser")
        return soup.find('p', class_ = "left_margin").get_text()

    def get_task_number(self):
        request_text = requests.get(self.url).text
        soup = BeautifulSoup(request_text, "html.parser")
        task_number = soup.find('p', class_ = "left_margin").get_text()
        self.task_number = utilites.get_numbers(task_number)[0]

    def __repr__(self):
        s = ""
        s+=self.url+'\n'
        s+=str(self.number)+'\n'
        s+=self.task_number+'\n'
        s+=self.text
        return s

if __name__ == "__main__":
    test = Task(7643)
    print(test)