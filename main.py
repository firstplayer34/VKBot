#Запуск на компьютере создаст второго бота и все сообщения будут дублироваться

from constants import TOKEN #токен высылаю на ВК
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from patterns import ANSWER_ASK_MESSAGE, WARNING_ANSWER, SOURCE, patterns
from task import Task
import utilites
import os.path

#Работа с паттернами для получения подходящего ответа
def find_pattern(text):

    """
    Находит и составляет ответ из patterns.py
    Подходит для запросов, не связанных с заданиями

    params:
        text: Текст, по которому будет искаться ответ

    returns:
        s: Текст сообщения для ответа
        used_responses: Все сообщения из patterns, используемые для ответа
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
    """
    Отправляет сообщение по event.user_id с переданным текстом
    
    params:
        vk: Сессия VK
        event: Событие сессии
        text: Текст сообщения
    
    """
    vk.messages.send(
        user_id = event.user_id,
        message = text,
        random_id = utilites.g_id()
    )

#Проверяет наличие файла и нужен ли ответ пользователю на задание
def answer_required(event):
    """
    Проверяет наличие файла и нужен ли ответ пользователю на задание

    """
    if os.path.exists("users/"+str(event.user_id)+".txt") is True:
        if len(open("users/"+str(event.user_id)+".txt","r").read()) != 0:
            return True
        else:
            return False
    return False


def log_task(event, task):
    """
    Записывает в файл номер задания, которое запросил пользователь

    """
    f = open("users/"+str(event.user_id)+".txt", "w")
    f.write(str(task.number))
    f.close()


def delog_task(event):
    """
    Удаляет задание из списка ученика

    """

    f = open("users/"+str(event.user_id)+".txt", "w")
    f.close()


if __name__ == "__main__":
    #Создание сессии работы бота
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    #Ожидание события
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

            #TODO: Проработать ответы для простого ответа и для работы с заданиями

            try:
                #Мы не знаем, просил ли ранее пользователь задание. Поэтому,
                #проверка работает так: для каждого пользователя создаётся файл
                #в папке users с его id. В единственной строке записывается номер задания
                #которое он запаршивал. Если файл не пустой, то первая строка - номер задания
                #на которое требуется вывести ответ
                #Если файл пустой, то и ответ на запрошенное задание не требуется
                if event.text.lower() == "случайное задание":
                    if answer_required(event):
                        Vk_send_message(vk, event, "Закончите предыдущее задание!")
                    else:
                        task = Task(None)
                        Vk_send_message(vk, event, task.__repr__())
                        Vk_send_message(vk, event, ANSWER_ASK_MESSAGE)
                        log_task(event,task)
                elif event.text == "\q":
                    if answer_required(event):
                        Vk_send_message(vk, event, "Отмена задания")
                        delog_task(event)      
                elif "Ответ:" in event.text or "ответ:" in event.text:
                    try: #На случай, если пользователь просто так написал "Ответ"
                        with open("users/"+str(event.user_id)+".txt") as f:
                            task_number = int(f.read())
                        task = Task(task_number)
                        Vk_send_message(vk, event, task.answer+'\n'+task.url)
                        
                        delog_task(event)
                    except Exception:
                        Vk_send_message(vk, event, "Нет задачи - нет ответа")
                elif event.text.lower() == "текущее задание":
                    if answer_required(event):
                        with open("users/"+str(event.user_id)+".txt") as f:
                            task_number = int(f.read())
                        task = Task(task_number)
                        Vk_send_message(vk, event, task.__repr__())
                    else:
                        Vk_send_message(vk, event, "Текущего задания нет")
                else:
                    Vk_send_message(vk, event,find_pattern(event.text)[0])

            except vk_api.exceptions.ApiError:
                Vk_send_message(vk, event, "Произошла ошибка.\nПопробуйте ещё раз")