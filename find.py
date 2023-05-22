import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['twitter_scraper']
collection = db['tweets']

docs = collection.find()
for doc in docs:
    print('username: ' + doc["username"])
    print('text: ' + doc["text"])
    print('date: ' + doc["date"])
    print('##########')
