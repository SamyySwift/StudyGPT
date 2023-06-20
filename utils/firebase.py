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
    storage.child(f"Documents/{filename}").put(file)
    print("--Done Uploading")


# storage.download(
#     "EEE401-Lecture Note On Microprocessor and Microcontroller Theory and Applications-EEE-2010-(Learnclax.com).pdf",
#     "micro.pdf",
# )
folder_path = "Chromadb"


def retrieve_path(folder_path):
    files = storage.bucket.list_blobs(prefix=folder_path)
    persist_dir = ""
    for file in files:
        # Skip the folder itself
        if file.name == folder_path:
            continue
        # Extract the file name without the folder path
        file_name = file.name.replace(folder_path + "/", "")[:4]

        persist_dir += file_name + "+"
    # Remove the trailing "+" symbol if any
    if persist_dir.endswith("+"):
        persist_dir = persist_dir[:-1]
    return persist_dir[1:]


# folder_to_check = "b"
# # List all the blobs/files under the folder prefix
# blobs = storage.bucket.list_blobs(prefix=folder_path)

# # Check if any blobs/files exist under the folder prefix
# folder_exists = any(True for _ in blobs)

# # Print the result
# if folder_exists:
#     print(f"Folder '{folder_to_check}' exists within '{folder_path}' in Firestore.")
# else:
#     print(
#         f"Folder '{folder_to_check}' does not exist within '{folder_path}' in Firestore."
#     )
