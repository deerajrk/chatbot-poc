from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import datetime as dt
import streamlit as st


class Logger:
    def __init__(self):
        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(self._get_firestore_creds_dict())
            initialize_app(cred)
        self.db = firestore.client()

    def _get_firestore_creds_dict (self):
        creds_dict = {}
        creds_dict["type"] = st.secrets["fb_type"]
        creds_dict["project_id"] = st.secrets["fb_project_id"]
        creds_dict["private_key_id"] = st.secrets["fb_private_key_id"]
        creds_dict["private_key"] = st.secrets["fb_private_key"]
        creds_dict["client_email"] = st.secrets["fb_client_email"]
        creds_dict["client_id"] = st.secrets["fb_client_id"]
        creds_dict["auth_uri"] = st.secrets["fb_auth_uri"]
        creds_dict["token_uri"] = st.secrets["fb_token_uri"]
        creds_dict["auth_provider_x509_cert_url"] = st.secrets["fb_auth_provider_x509_cert_url"]
        creds_dict["client_x509_cert_url"] = st.secrets["fb_client_x509_cert_url"]
        creds_dict["universe_domain"] = st.secrets["fb_universe_domain"]

        return creds_dict

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
    