import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
from mongoengine import connect, Document, StringField, BooleanField

uri = "mongodb+srv://1234554321:1234554321@alona.3jegrtc.mongodb.net/"


# Подключение с использованием TLS/SSL и CAFile
connect(db="hw_8", host=uri, ssl=True, tlsCAFile=certifi.where())

class User(Document):
    fullname = StringField(required=True, unique=True)
    email = StringField(max_length=150)
    completed = BooleanField(default=False)
    meta = {"collection": "users"}

if __name__ == '__main__':
    # Создание базы данных и коллекций (если они еще не существуют)
    User._get_collection()