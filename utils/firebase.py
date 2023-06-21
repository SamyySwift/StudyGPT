import pyrebase
from httplib2 import ServerNotFoundError
import streamlit as st
from streamlit_lottie import st_lottie
from utils.config import load_lottiefile

firebaseConfig = {
    "apiKey": "AIzaSyB6mhQJR3zKAh7XP4GX8YxgDXadgPlguac",
    "authDomain": "flipbot-4f922.firebaseapp.com",
    "projectId": "flipbot-4f922",
    "storageBucket": "flipbot-4f922.appspot.com",
    "databaseURL": "",
    "serviceAccount": "utils/serviceAccountKey.json",
}

try:
    firebase_storage = pyrebase.initialize_app(firebaseConfig)
    storage = firebase_storage.storage()
except ServerNotFoundError:
    error = load_lottiefile("lotties/error.json")
    st_lottie(error)


def upload_to_firestore(filename, file):
    storage.child(f"{filename}").put(file)
    print("--Done Uploading")


def folder_exist(folder_name):
    print("--Checking for folder")
    blobs = storage.list_files()
    for f in blobs:
        if f.name == f"{folder_name}":
            return True
