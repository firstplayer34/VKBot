#Всякие функции, полезные в использовании в нескольких пакетах

import re
import patterns

def get_numbers(string):
    """
    Получает все числа из строки. Подходит для поиска номеров заданий

    params:
        string: Строка для поиска чисел
    returns:
        numbers: Все числа, найденные в строке (list)
    """
    pattern = r"\d+"
    numbers = re.findall(pattern,string)
    return numbers

#Форматирует текст задания с выбором ответа
def format_choise_task(text):
    """
    Форматирует текст задания с выбором ответа
    params:
        text: Текст задания
    returns:
        text: Отформатированный текст

    """
    iterator = re.finditer(patterns.PATTERN_ANSWER_OPTION, text)
    t = 0
    for match in iterator:
        position = match.span()[0]
        text = insert_char(text,position+t,'\n')
        t+=1
    return text

#Вставка символа/подстроки в строку
def insert_char(text, index, char):
    return text[:index]+str(char)+text[index:]

#Возвращает случайное значение. Полезно для получения message_id
def g_id():
    import random
    return random.randint(0,10000000)