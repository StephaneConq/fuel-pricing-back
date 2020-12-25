import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from config import PROJECT_ID

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': PROJECT_ID,
})

db = firestore.client()


def read_all(collection):
    collection = db.collection(collection)
    docs = collection.stream()
    doc_list = []
    for doc in docs:
        doc_list.append(doc.to_dict())
    return doc_list


def add(collection, payload, id):
    doc_ref = db.collection(collection).document(id)
    doc_ref.set(payload)
