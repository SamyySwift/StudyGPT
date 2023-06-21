import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyB6mhQJR3zKAh7XP4GX8YxgDXadgPlguac",
    "authDomain": "flipbot-4f922.firebaseapp.com",
    "projectId": "flipbot-4f922",
    "storageBucket": "flipbot-4f922.appspot.com",
    "databaseURL": "",
    "serviceAccount": "utils/serviceAccountKey.json",
}


firebase_storage = pyrebase.initialize_app(firebaseConfig)
storage = firebase_storage.storage()


def upload_to_firestore(filename, file):
    storage.child(f"{filename}").put(file)
    print("--Done Uploading")


def folder_exist(folder_name):
    print("--Checking for folder")
    blobs = storage.list_files()
    for f in blobs:
        if f.name == f"{folder_name}":
            return True


# import tempfile
# import pickle

# temp_file = tempfile.NamedTemporaryFile(delete=False)
# storage.download("EEE4", temp_file.name)
# with open(temp_file.name, "rb") as file:
#     loaded_vectordb = pickle.load(file)

# print(loaded_vectordb)
