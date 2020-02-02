from constants import TOKEN
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from patterns import patterns

#Working with patterns and returning a more comfortable answer
def find_pattern(text):
    s = ""
    used_responses = []
    import re
    for i in patterns:
        if re.match(i[0], text.lower(), re.IGNORECASE) is not None:
            print(i)
            for j in i[1]:
                s+=j+'\n'
            used_responses.append(i)
    return s, used_responses

    
if __name__ == "__main__":
    find_pattern("привет")
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            message_text = find_pattern(event.text)[0]
            import random
            vk.messages.send(
                user_id = event.user_id,
                message = message_text,
                random_id = random.randint(0,10000000)
            )