import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("connectionToken.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dagitik-436e4-default-rtdb.europe-west1.firebasedatabase.app/'
})


class A:
    def __init__(self):
        self.a = ["a"]

    def toObject(self):
        return {"a": self.a}


a = A()

ref = db.reference("user")
ref.set({"test": a.toObject()})
data = ref.get()
print(data)
