import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("config/serviceAccountKey.json")
# initialize admin SDK to call in auth.py for BE token verification and decoding
firebase_admin.initialize_app(cred)