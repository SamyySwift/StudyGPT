import pyrebase
from httplib2 import ServerNotFoundError
import streamlit as st
import os

key_path = os.path.join("utils", "serviceAccountKey.json")

firebaseConfig = {
    "apiKey": "AIzaSyB6mhQJR3zKAh7XP4GX8YxgDXadgPlguac",
    "authDomain": "flipbot-4f922.firebaseapp.com",
    "projectId": "flipbot-4f922",
    "storageBucket": "flipbot-4f922.appspot.com",
    "databaseURL": "",
    "messagingSenderId": "37185214139",
    "appId": "1:37185214139:web:5d530ebd8f8373b8877b9e",
    "measurementId": "G-SQTDYT12Z8",
    "serviceAccount": key_path,
}

try:
    firebase_storage = pyrebase.initialize_app(firebaseConfig)
    storage = firebase_storage.storage()
except ServerNotFoundError:
    st.error("Connection Error")


def upload_to_firestore(filename, file):
    storage.child(f"{filename}").put(file)
    print("--Done Uploading")


def folder_exist(folder_name):
    print("--Checking for folder")
    blobs = storage.list_files()
    for f in blobs:
        if f.name == f"{folder_name}":
            return True
