import vk
import random
from flask import request, json
from settings import *
import messageHandler
import requests
#import time


session = vk.Session()
api = vk.API(session, v=5.8)


def get_random_wall_picture(group_id):
    max_num = api.photos.get(owner_id=group_id, album_id='wall', count=0)['count']
    num = random.randint(1, max_num)
    photo = api.photos.get(owner_id=str(group_id), album_id='wall', count=1, offset=num)['items'][0]['id']
    attachment = 'photo' + str(group_id) + '_' + str(photo)
    return attachment


def send_message(user_id, token, message, attachment=""):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def hello_answer():
    data = json.loads(request.data)
    object = data['object']
    user_id = object['user_id']
    profiles = api.users.get(user_id=user_id,  fields = 'bdate, city, sex, country, nickname, followers_count, occupation, activities')


                        # 1. Открываем файл со списком уже заходивших юзеров
                        # 2. Если юзера нет в списке, то добавляем его в список и заводим на него файл-досье


    file = open("/home/Kirill/mysite/statistics/ids_list/ids_list.txt", 'r')
    idsList = file.read()
    if idsList.find(str(user_id)) == -1:
        file = open("/home/Kirill/mysite/statistics/ids_list/ids_list.txt", 'a')
        file.write(str(user_id) + '\n')
        file.close()
        file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'w')
        userInfo = {
                       "id": str(user_id),
                       "info": {
                           "sex": profiles[0]['sex'],
                    	   "firstName": profiles[0]['first_name'],
                    	   "lastName": profiles[0]['last_name'],
                    	   "birthday": profiles[0]['bdate'],
                    	   "city": profiles[0]['city']['title'],
                    	   "country": profiles[0]['country']['title'],
                           "followers_count": profiles[0]['followers_count'],
                           "nickname": profiles[0]['nickname'],
                           "occupation": profiles[0]['occupation']['type'],
                    	   },
                    	"look": {
                    	   "eyeColor": "",
                    	   "hairColor": "",
                    	   "skinColor": "",
                    	   "tone": "",
                    	   }
                    }
        json.dump(userInfo, file)
        file.close()


    message = 'Привет, '+profiles[0]['first_name'] + "!\n" + "Меня зовут Вивьен. Я - чат-бот.\n" + "Если ты расскажешь о своей внешности я дам тебе подробные рекомендации по макияжу.\n" + "Какого цвета твои глаза?"
    return message

def eye_answer():
    data = json.loads(request.data)
    object = data['object']
    user_id = object['user_id']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'r')
    userDate = file.read()
    userDate = json.loads(userDate)
    file.close()
    userDate['look']['eyeColor'] = object['body']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'w')
    json.dump(userDate, file)
    file.close()
    message = "Я запомнила... Какой у тебя оттенок кожи, розовый или оливковый?"
    return message



def skin_answer():
    data = json.loads(request.data)
    object = data['object']
    user_id = object['user_id']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'r')
    userDate = file.read()
    userDate = json.loads(userDate)
    file.close()
    userDate['look']['skinColor'] = object['body']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'w')
    json.dump(userDate, file)
    file.close()
    message = "Хорошо... Какой у тебя цвет волос?"
    return message

def hair_answer():
    data = json.loads(request.data)
    object = data['object']
    user_id = object['user_id']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'r')
    userDate = file.read()
    userDate = json.loads(userDate)
    file.close()
    userDate['look']['hairColor'] = object['body']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'w')
    json.dump(userDate, file)
    file.close()
    message = "Ясно... А что для тебя главное в тональном средстве, стойкость, естественность или легкость?"
    return message

def tone_answer():
    data = json.loads(request.data)
    object = data['object']
    user_id = object['user_id']
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'r')
    userDate = file.read()
    userDate = json.loads(userDate)
    file.close()
    userDate['look']['tone'] = object['body'].lower()
    file = open("/home/Kirill/mysite/statistics/" + str(user_id) + ".json", 'w')
    json.dump(userDate, file)
    file.close()
    message = "Отлично... Вот рекомендации для тебя:\n\n" + messageHandler.testing()
    return message


#Поиск фотографий по лицу
############################################################################################################################

key = "JFVcKkyuyiVPmoJ8OxZ9z_UQIIMpotpr"
secret = "DfpHhYpdDLxLyLXjvpcBhj9Wd7C8Oj6Z"

def search_face(image_url, outer_id):
    r = requests.post("https://api-us.faceplusplus.com/facepp/v3/search", data={'api_key': key, 'api_secret': secret, 'image_url': image_url, 'outer_id': outer_id, 'return_result_count': "5"})
    result = json.loads(r.content)
    print(r.status_code, r.reason)
    return result

def img_answer():
    data = json.loads(request.data)
    photo = data['object']['attachments'][0]['photo']['photo_604']
    photo_url = str(photo)
    found = search_face(photo_url, 'faces_test_013')
    tokens = found['results'][0]['face_token'] + " " + found['results'][1]['face_token'] + " " + found['results'][2]['face_token'] + " " + found['results'][3]['face_token'] + " " + found['results'][4]['face_token']
    token_list = tokens.split()
    f = open('/home/Kirill/mysite/strings/mapping.txt')
    line_list = []
    for line in f.readlines():
        i = 0
        while i < len(token_list):
            if line.find(token_list[i]) > -1:
                line = line.replace("\n", "")
                img_url = line.split(" ")
                line_list.append(img_url[2])
                img_url.clear()
            i = i + 1
    attachment = line_list[0] + "," + line_list[1] + "," + line_list[2] + "," + line_list[3] + "," + line_list[4]
    #message = line_list[0] + "," + line_list[1] + "," + line_list[2] + "," + line_list[3] + "," + line_list[4]
    return attachment


############################################################################################################################
















