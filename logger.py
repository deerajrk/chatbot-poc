from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import datetime as dt
import streamlit as st
from firestore_db import get_firestore_creds


class Logger:
    def __init__(self):
        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(get_firestore_creds())
            initialize_app(cred)
        self.db = firestore.client()

    def log_to_firestore(self, username, agent, question, answer):
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_data = {
            "timestamp": timestamp,
            "username": username,
            "agent": agent,
            "question": question,
            "answer": answer
        }
        self.db.collection("chat-bot-poc-logs").add(log_data)
    