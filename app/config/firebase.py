import firebase_admin
from firebase_admin import credentials

# initialize admin SDK with creds from specified file
cred = credentials.Certificate("app/config/serviceAccountKey.json")
firebase_admin.initialize_app(cred)