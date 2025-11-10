
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

password=quote_plus('Kadak21@')

uri = f"mongodb+srv://gwkadak:{password}@cluster0.h93js.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


database =client['Database']
collection =database['Students_embeddings']

a=collection.insert_one({'a':1})
print(a.inserted_id)









    