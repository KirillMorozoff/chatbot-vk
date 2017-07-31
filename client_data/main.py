# -*- coding: utf-8 -*-
#Программа предварительно формирующая базу данных лиц.
#В дальнейшем по ней будет осуществляться поиск
import requests
from flask import request, json
from os import listdir
from urllib.request import urlretrieve
import vk, os, time, math

key = "you key"
secret = "you secret"



#    Формирование списков фотографий
########################################################################################################################
def vk_photos_get(album_url):
    login = 'your login'
    password = 'your password'
    vk_id = '6120276'
    session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password)
    vkapi = vk.API(session)
    # Разбираем ссылку
    album_id = album_url.split('/')[-1].split('_')[1]
    owner_id = album_url.split('/')[-1].split('_')[0].replace('album', '')
    photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id)
    photos_count = vkapi.photos.getAlbums(owner_id=owner_id, album_ids=album_id)[0]['size']
    #print (json.dumps(photos, indent=4, sort_keys=True))
    print (photos_count)
    photos_list = []
    i=0
    while i < photos_count:
        photos_list.append("photo" + str(photos[i]['owner_id']) + "_" + str(photos[i]['pid']))
        i=i+1
    print (photos_list)
    return photos_list

def vk_list(album_url):
    login = 'your login'
    password = 'your password'
    vk_id = '6120276'
    session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password)
    vkapi = vk.API(session)
    # Разбираем ссылку
    album_id = album_url.split('/')[-1].split('_')[1]
    owner_id = album_url.split('/')[-1].split('_')[0].replace('album', '')
    photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id)
    photos_count = vkapi.photos.getAlbums(owner_id=owner_id, album_ids=album_id)[0]['size']
    #print (json.dumps(photos, indent=4, sort_keys=True))
    print (photos_count)
    img_url_list = []
    i=0
    while i < photos_count:
        img_url_list.append(photos[i]['src_big'])
        i=i+1
    return img_url_list

########################################################################################################################

def creating_faceset(display_name, outer_id):
    r = requests.post("https://api-us.faceplusplus.com/facepp/v3/faceset/create", data={'api_key': key, 'api_secret': secret, 'display_name': display_name, 'outer_id': outer_id})
    data = json.loads(r.content)
    print(r.status_code, r.reason)
    print(str(data))

def face_token_get(image_url):
    r = requests.post("https://api-us.faceplusplus.com/facepp/v3/detect", data={'api_key': key, 'api_secret': secret, 'image_url': image_url})
    data = json.loads(r.content)
    print(r.status_code, r.reason)
    print(str(data))
    try:
        token = data['faces'][0]['face_token']
    except KeyError:
        print("Key Error!")
    return token

def create_face_token_list(img_url_list, photos_list):
    token_list = []
    i=0
    file = open("mapping.txt", "a")
    while i < len(img_url_list):
        try:
            token_list.append(face_token_get(img_url_list[i]))
            file.write(img_url_list[i] + " " + token_list[i] + " " + photos_list[i] + "\n")
        except IndexError:
            print ("an index error!")
        i = i+1

    file.close()
    print (token_list)
    return token_list

def add_faces(outer_id, token_list):
    for face_tokens in token_list:
        r = requests.post("https://api-us.faceplusplus.com/facepp/v3/faceset/addface", data={'api_key': key, 'api_secret': secret, 'outer_id': outer_id, 'face_tokens': face_tokens})
        data = json.loads(r.content)
        print(r.status_code, r.reason)
        print(str(data))

def get_set_detail(outer_id):
    r = requests.post("https://api-us.faceplusplus.com/facepp/v3/faceset/getdetail", data={'api_key': key, 'api_secret': secret, 'outer_id': outer_id})
    data = json.loads(r.content)
    print(r.status_code, r.reason)
    print(str(data))


def search_face(image_url, outer_id):
    r = requests.post("https://api-us.faceplusplus.com/facepp/v3/search", data={'api_key': key, 'api_secret': secret, 'image_url': image_url, 'outer_id': outer_id, 'return_result_count': "5"})
    data = json.loads(r.content)
    print(r.status_code, r.reason)
    print(str(data))


########################################################################################################################

creating_faceset("Faces013", "faces_test_013")
add_faces('faces_test_013', create_face_token_list(vk_list("https://vk.com/album-147469960_244513401"), vk_photos_get("https://vk.com/album-147469960_244513401")))

#face_token_get('http://www.a-listinternational.com/wp-content/uploads/2016/06/brad-pitt-doesn-t-really-look-much-like-brad-pitt-in-these-photos-727400.jpg')

#vk_list("https://vk.com/album-147469960_244513401")


#get_set_detail('faces_test_016')
#search_face('http://www.a-listinternational.com/wp-content/uploads/2016/06/brad-pitt-doesn-t-really-look-much-like-brad-pitt-in-these-photos-727400.jpg', 'faces_test_014')
