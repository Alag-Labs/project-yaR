import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("video_processing/yar-v2.json")

firebase_admin.initialize_app(cred, {"storageBucket": "yar-v2.appspot.com"})

db = firestore.client()
bucket = storage.bucket()
