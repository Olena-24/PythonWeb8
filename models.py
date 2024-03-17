import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

uri = "mongodb+srv://1234554321:1234554321@alona.3jegrtc.mongodb.net/"

connect(db="hw_8", host=uri, ssl=True, tlsCAFile=certifi.where())

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}

class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)

if __name__ == '__main__':

    Author._get_collection()
    Quote._get_collection()