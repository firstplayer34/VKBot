from constants import TOKEN
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import re
from datetime import datetime
from patterns import *


vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if re.match(pattern_hello, event.text.lower()) is not None:
            vk.messages.send(
                user_id = event.user_id,
                message = hello_message,
                random_id = random.randint(0,1000000)
            )
            vk.messages.send(
                user_id = event.user_id,
                message = review_message,
                random_id = random.randint(0,1000000)
            )
            with open("output.txt", "a") as o:
                o.write("hello_request at {} from {}\n".format(datetime.now(),event.user_id))
        if re.match(pattern_time, event.text.lower()) is not None:
            vk.messages.send(
                user_id = event.user_id,
                message = "Московское время: "+str(datetime.now()),
                random_id = random.randint(0,1000000)
            )
            with open("output.txt", "a") as o:
                o.write("time_request at {} from {}\n".format(datetime.now(),event.user_id))
            