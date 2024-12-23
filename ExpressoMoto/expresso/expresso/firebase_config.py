import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Replace with your Firebase project credentials
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-firebase-project-id.firebaseio.com/'
})
