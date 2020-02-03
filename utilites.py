import re
import patterns

def get_numbers(string):
    pattern = r"\d+"
    return re.findall(pattern,string)

def format_choise_task(text):
    iterator = re.finditer(patterns.PATTERN_ANSWER_OPTION, text)
    t = 0
    for match in iterator:
        position = match.span()[0]
        text = insert_char(text,position+t,'\n')
        t+=1
    return text

def insert_char(text, index, char):
    return text[:index]+str(char)+text[index:]

def g_id():
    import random
    return random.randint(0,10000000)