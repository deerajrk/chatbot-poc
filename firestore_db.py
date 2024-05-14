import streamlit as st


def get_firestore_creds ():
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