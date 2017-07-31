
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, json
from settings import *
import messageHandler

app = Flask(__name__)

@app.route('/')
def hello_world():
    file = open("/home/Kirill/mysite/statistics/ids_list/ids_list.txt", 'r')
    fileTemp = file.read()
    fileList = fileTemp.split("\n")
    file.close()
    file1 = open("/home/Kirill/mysite/strings/table.html", 'r')
    file2 = open("/home/Kirill/mysite/strings/table-2.html", 'r')
    firstPartHtml = file1.read()
    secondPartHtml = file2.read()
    file1.close()
    file2.close()
    n = len(fileList)-1
    i = 0
    while i < n:
        file = open("/home/Kirill/mysite/statistics/" + str(fileList[i]) + ".json", 'r')
        fileTemp = file.read()
        userDate = json.loads(fileTemp)
        string = "<tr>" + "<td>" + userDate['id'] + "</td><td>" + userDate['info']['firstName'] + "</td><td>" + userDate['info']['lastName'] + "</td><td>" + userDate['info']['nickname'] + "</td><td>" + str(userDate['info']['sex']) + "</td><td>" + userDate['info']['birthday'] + "</td><td>" + userDate['info']['country'] + "</td><td>" +str(userDate['info']['city']) + "</td><td>" + str(userDate['info']['followers_count']) + "</td><td>" + userDate['info']['occupation'] + "</td><td>" + userDate['look']['eyeColor'] + "</td><td>" + userDate['look']['hairColor'] + "</td><td>" + userDate['look']['skinColor'] + "</td><td>" + userDate['look']['tone'] + "</td>" + "</tr>"
        firstPartHtml = firstPartHtml + string
        i = i+1

    return firstPartHtml+secondPartHtml




@app.route('/', methods=['POST'])
def processing():
    #Распаковываем json из пришедшего GET-запроса
    data = json.loads(request.data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        messageHandler.create_answer(data['object'], token)
        return 'ok'
        # Сообщение о том, что обработка прошла успешно