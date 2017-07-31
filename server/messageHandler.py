import vkapi
import os
import importlib
from command_system import command_list
from flask import request, json

def damerau_levenshtein_distance(s1, s2):
   d = {}
   lenstr1 = len(s1)
   lenstr2 = len(s2)
   for i in range(-1, lenstr1 + 1):
       d[(i, -1)] = i + 1
   for j in range(-1, lenstr2 + 1):
       d[(-1, j)] = j + 1
   for i in range(lenstr1):
       for j in range(lenstr2):
           if s1[i] == s2[j]:
               cost = 0
           else:
               cost = 1
           d[(i, j)] = min(
               d[(i - 1, j)] + 1,  # deletion
               d[(i, j - 1)] + 1,  # insertion
               d[(i - 1, j - 1)] + cost,  # substitution
           )
           if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
               d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
   return d[lenstr1 - 1, lenstr2 - 1]


def load_modules():
   files = os.listdir("mysite/commands")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("commands." + m[0:-3])


def get_answer(body):
   message = "Прости, не понимаю тебя. Напиши 'помощь', чтобы узнать мои команды"
   attachment = ''
   distance = len(body)
   command = None
   key = ''
   for c in command_list:
       for k in c.keys:
           d = damerau_levenshtein_distance(body, k)
           if d < distance:
               distance = d
               command = c
               key = k
               if distance == 0:
                   message, attachment = c.process()
                   return message, attachment
   if distance < len(body)*0.4:
       message, attachment = command.process()
       message = 'Я поняла ваш запрос как "%s"\n\n' % key + message
   return message, attachment


def create_answer(data, token):
   load_modules()
   user_id = data['user_id']
   message, attachment = get_answer(data['body'].lower())
   #Если присутствует опечатка в запросе
   if message.find('Я поняла ваш запрос как') > -1:
          message = message.split('"')[1]
          i = 0
          while i < 6:
              commands = ''.join(command_list[i].keys)
              if commands.find(message) > -1:
                  commandName = command_list[i].name
                  if commandName == 'Если назовешь цвет своих волос':
                      jsonRewright('hairColor', message)
                      message = 'Я понял ваш запрос как "%s"\n\n' % message + "Ясно... А что для тебя главное в тональном средстве, стойкость, естественность или легкость?"
                  elif commandName == 'привет':
                      message, attachment = get_answer(data['body'].lower())
                  elif commandName == 'Если назовешь цвет своих глаз':
                      jsonRewright('eyeColor', message)
                      message = 'Я понял ваш запрос как "%s"\n\n' % message + "Я запомнила... Какой у тебя оттенок кожи, розовый или оливковый?"
                  elif commandName == 'Если назовешь цвет своей кожи':
                      jsonRewright('skinColor', message)
                      message = 'Я поняла ваш запрос как "%s"\n\n' % message + "Хорошо... Какой у тебя цвет волос?"
                  elif commandName == 'Если назовешь главное для тебя в тональном средстве':
                      jsonRewright('tone', message)
                      message = 'Я поняла ваш запрос как "%s"\n\n' % message + "Отлично, вот рекомендации специально для тебя:\n"  + testing()
              i = i + 1
   vkapi.send_message(user_id, token, message, attachment)


def jsonRewright(item, message):
    data = json.loads(request.data)
    object = data['object']
    user_id = object['user_id']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'r')
    userDate = file.read()
    userDate = json.loads(userDate)
    file.close()
    userDate['look'][item] = message.lower()
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'w')
    json.dump(userDate, file)
    file.close()


def testing():
    data = json.loads(request.data)
    object = data['object']
    user_id = object['user_id']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'r')
    userDate = file.read()
    userDate = json.loads(userDate)
    file.close()
    eyesColor = userDate['look']['eyeColor'].lower()
    hairColor = userDate['look']['hairColor'].lower()
    skinColor = userDate['look']['skinColor'].lower()
    tone = userDate['look']['tone'].lower()

    hairColorsRusList = ['ярко-русые', 'ярко-русая', 'ярко-русый', 'русые', 'русая', 'русый', 'бледно-коричневатые', 'бледно-коричневатый', 'бледно-коричневатая',
                           'коричневый', 'бледно-коричневый', 'бледно-коричневая', 'бледно-коричневые', 'бледно-коричневатый', 'бледно-коричневатая',
                           'светло-коричневый', 'светлобурый', 'светло-русый', 'средне-русый', 'тёмно-русый']
    hairColorsBlondList = ['блонд', 'блонда', 'блондинка', 'блондинистая', 'белый', 'льняной', 'платина', 'платиновый', 'платиновые', 'золотистый',
                       'золотистые', 'золотые', 'золото', 'пепельный', 'пепельные', 'пепельная', 'пшеничные', 'пшеничный', 'пшеничная', 'бежевые', 'бежевый', 'бежевая']
    hairColorsShatenList = ['каштановый', 'каштановые', 'каштанового', 'нежно-шоколадный', 'нежно-шоколадного', 'шатен', 'шатенка']
    hairColorsBrunetList = ['брюнет', 'брюнетка', 'темные', 'чернявая', 'черные', 'темная', 'черный']

    hairColorsRusString = ' '.join(hairColorsRusList)
    hairColorsBlondString = ' '.join(hairColorsBlondList)
    hairColorsShatenString = ' '.join(hairColorsShatenList)
    hairColorsBrunetString = ' '.join(hairColorsBrunetList)

    result = "Что-то пошло не так..."
    file = open("/home/Kirill/mysite/strings/strings.json", 'r')
    temp = file.read()
    resultTexts = json.loads(temp)
    file.close()

    if eyesColor=="карие":
        result = resultTexts['eyes']['broun']
    elif eyesColor=="голубые" or eyesColor=="голубого" or eyesColor=="серо-голубые" or eyesColor=="серо-голубого" or eyesColor=="синего" or eyesColor=="синие":
        result = resultTexts['eyes']['blue']
    elif eyesColor=="зеленые" or eyesColor=="зеленого" or eyesColor=="серо-зеленые" or eyesColor=="серо-зеленого":
        result = resultTexts['eyes']['green']
    elif eyesColor=="серые" or eyesColor=="серого":
        result = resultTexts['eyes']['grey']

    if hairColorsRusString.find(hairColor) > -1:
        result = result + "\n\n" + resultTexts['hairs']['rus']
    elif hairColorsBlondString.find(hairColor) > -1:
        result = result + "\n\n" + resultTexts['hairs']['blond']
    elif hairColorsShatenString.find(hairColor) > -1:
        result = result + "\n\n" + resultTexts['hairs']['shaten']
    elif hairColorsBrunetString.find(hairColor) > -1:
        result = result + "\n\n" + resultTexts['hairs']['brunet']

    if skinColor == "розовый" or skinColor == "розового":
        result = result + "\n\n" + resultTexts['skin']['rose']
    elif skinColor == "оливковый" or skinColor == "оливкового":
        result = result + "\n\n" + resultTexts['skin']['olive']

    return result














