import pickle
import os

from pydash_app.user import User

def datastore_filename():
    return './_data/datastore.pkl'

def load():
    with open(datastore_filename(), 'rb+') as datastore_file:
        return pickle.load(datastore_file)

def seed_datastore():
    seed_data = {
        'users': {
            "Qqwy": User(name="Qqwy", password="topsecret")
        }
    }
    with open(datastore_filename(), 'xb+') as datastore_file:
         pickle.dump(seed_data, datastore_file)
    print("Seedsfile persisted successfully!")

