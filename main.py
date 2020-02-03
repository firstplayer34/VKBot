from constants import TOKEN
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from patterns import ANSWER_ASK_MESSAGE, patterns
from task import Task
import utilites

ON_TASK = False

#Working with patterns and returning a more comfortable answer
def find_pattern(text):
    s = ""
    used_responses = []
    import re
    for i in patterns:
        if re.match(i[0], text.lower(), re.IGNORECASE) is not None:
            for j in i[1]:
                s+=j
            used_responses.append(i)
    return s, used_responses

def Vk_send_message(vk,event,text):
    vk.messages.send(
        user_id = event.user_id,
        message = text,
        random_id = utilites.g_id()
    )

    
if __name__ == "__main__":
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            try:
                if (event.text == "Случайное задание") and ON_TASK is False:
                    test = Task(None)
                    Vk_send_message(vk,event,test.__repr__())
                    Vk_send_message(vk, event, ANSWER_ASK_MESSAGE)
                    ON_TASK = True
                else:
                    Vk_send_message(vk,event,find_pattern(event.text)[0])
            except vk_api.exceptions.ApiError:
                Vk_send_message(vk, event, "Произошла ошибка.\nПопробуйте ещё раз")