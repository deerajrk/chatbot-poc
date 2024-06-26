from streamlit_gsheets import GSheetsConnection
import pandas as pd
import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
from firestore_db import get_firestore_creds
import firebase_admin


try:
  firebase_admin.get_app()
except ValueError:
  cred = credentials.Certificate(get_firestore_creds())
  initialize_app(cred)
  db = firestore.client()

col_ref = db.collection('chat-bot-poc-logs')

data_objects = []

def create_data_object(doc_ref, doc_data):
  data = {
      'timestamp': doc_data.get('timestamp'),
      'username': doc_data.get('username'),
      'agent': doc_data.get('agent'),
      'question': doc_data.get('question'),
      'answer': doc_data.get('answer'),
  }
  data['document_id'] = doc_ref.id
  data_objects.append(data)

query = col_ref.order_by('timestamp')
stream = query.stream()

for snapshot in stream:
  doc_ref = snapshot.reference
  doc_data = snapshot.to_dict()
  create_data_object(doc_ref, doc_data)

data_objects.sort(key=lambda obj: obj['timestamp'])

dataframe = pd.DataFrame(data_objects)

conn = st.connection("gsheets", type=GSheetsConnection)
conn.update(worksheet="Logs", data=dataframe)
    