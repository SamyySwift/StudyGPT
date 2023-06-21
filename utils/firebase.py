import pyrebase
import pickle

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


# def retrieve_path(folder_path):
#     files = storage.bucket.list_blobs(prefix=folder_path)
#     persist_dir = ""
#     for file in files:
#         # Skip the folder itself
#         if file.name == folder_path:
#             continue
#         # Extract the file name without the folder path
#         file_name = file.name.replace(folder_path + "/", "")[:4]

#         persist_dir += file_name + "+"
#     # Remove the trailing "+" symbol if any
#     if persist_dir.endswith("+"):
#         persist_dir = persist_dir[:-1]
#     return persist_dir[1:]


def folder_exist(folder_name):
    print("--Checking for folder")
    blobs = storage.list_files()
    for f in blobs:
        if f.name == f"{folder_name}":
            return True
