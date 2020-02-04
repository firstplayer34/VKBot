from constants import TOKEN #токен высылаю на ВК
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from patterns import ANSWER_ASK_MESSAGE, patterns
from task import Task
import utilites

#Работа с паттернами для получения подходящего ответа
def find_pattern(text):

    """
    Находит и составляет ответ из patterns.py
    Подходит для запросов, не связанных с заданиями
    """

    #TODO: Увеличить количество пустяковых запросов

    s = "" #Строка ответа на запрос
    used_responses = []     #Получение строк, участвующих в ответе
    import re
    for i in patterns:
        if re.match(i[0], text.lower(), re.IGNORECASE) is not None:
            for j in i[1]:
                s+=j        #Формирование ответа
            used_responses.append(i)
    return s, used_responses


def Vk_send_message(vk,event,text):

    """Отправляет сообщение по event.user_id с переданным текстом"""

    vk.messages.send(
        user_id = event.user_id,
        message = text,
        random_id = utilites.g_id()
    )

if __name__ == "__main__":
    import os.path

    #Создание сессии работы бота
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    #Ожидание события
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

            #TODO: Проработать ответы для простого ответа и для работы с заданиями
            #TODO: Переработать код представленный ниже

            try:
                if (os.path.exists("users/"+str(event.user_id)+".txt")) is False:
                    f = open("users/"+str(event.user_id)+".txt",'w')
                    f.close()
                file = open("users/"+str(event.user_id)+".txt", "r")
                if (event.text == "Случайное задание") and file.read() == "":
                    test = Task(None)
                    Vk_send_message(vk,event,test.__repr__())
                    Vk_send_message(vk, event, ANSWER_ASK_MESSAGE)
                    with open("users/"+str(event.user_id)+".txt","w") as o:
                        o.write(str(test.number))
                elif len(file.read()) != 0:
                    task_number = int(file.read())
                    test = Task(task_number)
                    Vk_send_message(vk, event, test.answer)
                    with open("users/"+str(event.user_id)+".txt",'w') as o:
                        o.write("")
                else:
                    Vk_send_message(vk,event,find_pattern(event.text)[0])
                file.close()
            except vk_api.exceptions.ApiError:
                Vk_send_message(vk, event, "Произошла ошибка.\nПопробуйте ещё раз")