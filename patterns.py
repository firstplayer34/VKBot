from datetime import datetime

PATTERN_TIME = r".*врем.*"
PATTERN_HELLO = r".*прив.*"
PATTERN_TASK = r">Задание.*<a"
PATTERN_TASK_NUMBER = r"\d+"
PATTERN_ANSWER_OPTION = r"\d+[\)\.]"

HELLO_MESSAGE = "Привет, я бот. В настоящий момент я располагаюсь где-то на серверах Heroku в Европе, но это не мешает мне беседовать с тобою. В данный момент я учусь работать с базами данных. И да, если я не буду доступен, то тебе придётся подождать - я очень люблю спать, без шуток. Сервера закрываются, если со мною никто не общается 30 минут и это обидно :()"
REVIEW_MESSAGE = "Мы можем познакомиться поближе. Например, я могу тебе подсказать время с точностью до десятитысячных одной секунды! Чтобы воспользоваться этим, просто спроси меня \"Сколько времени?\" или что-то подобное. Главное запомни - я не умею читать твои мысли и иногда я ошибаюсь!"
ANSWER_ASK_MESSAGE = "Введите ответ\nЛибо введите \"\q\" для отмены"
TIME_MESSAGE = "Московское время: {}".format(datetime.now())

REQUEST_URL = 'https://hist-ege.sdamgia.ru/problem?id='

patterns = list(zip([PATTERN_HELLO, PATTERN_TIME],[[HELLO_MESSAGE,REVIEW_MESSAGE],TIME_MESSAGE]))


