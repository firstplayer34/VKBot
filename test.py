from task import Task
import re

def insert_char(text, index, char):
    return text[:index]+str(char)+text[index:]

text = Task(4993).text.replace("\xad","")
iterator = re.finditer(r"\d+\S", text)
t = 0
for match in iterator:
    position = match.span()[0]
    print(position+t)
    text = insert_char(text,position+t,'\n')
    t+=1
print(text)