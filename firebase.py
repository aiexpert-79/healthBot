import firebase_admin
from firebase_admin import credentials, db
import json

# Initialize Firebase
cred = credentials.Certificate('./serviceAccountKey.json')
myapp = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://consultant-bot-e7bb3-default-rtdb.asia-southeast1.firebasedatabase.app'
})

ref = db.reference('/users')
data = ref.set([
  {'gender': 'male', 'name':'Honey','email':'hmh0907@outlook.com'},
  {'gender':'female', 'name':'Ro', 'email':'ro2@ionq.com'},
  {'gender':'male', 'name':'John', 'email':'john@simple.com'}
])

#add data to firebase
ref = db.reference('/doctors')
data = ref.set([
  {'gender': 'male', 'name':'Michael','email':'michael11@outlook.com', 'location':'London','major':'dentist'},
  {'gender': 'female', 'name':'Olivia','email':'olivia@stedeller.com', 'location':'US', 'major':'surgery'},
])

def handle_event(event):
    print('Data changed:', event.data)
# # db change listen
# ref = db.reference('/')
# ref.listen(handle_event)

## export data from firebase
# documents = firestore.client().collection('doctors').stream()
ref = db.reference('/')
data = ref.get()
json_file = './docs/firebase.json'
documents = data
for doc in documents:
    # data[doc.id] = doc.to_dict()
  print(doc)

with open(json_file, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Data has been exported to {json_file}")