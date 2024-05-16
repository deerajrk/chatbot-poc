from auth.credentials import CREDENTIALS # From app
# from credentials import CREDENTIALS # From command line

import pickle, os
from streamlit_authenticator.utilities.hasher import Hasher

CREDS = CREDENTIALS

# This function is to be run from command line
def pickle_hashed_pws():
    passwords = [user_info["password"] for user_info in CREDS.values()]
    hashed_passwords = Hasher(passwords).generate()
    file_path = os.getcwd() + "/auth/hashed_pw.pkl"
    print(file_path)
    with open(file_path, "wb") as file:
        pickle.dump(hashed_passwords, file)

# Uncomment if running from command line
# pickle_hashed_pws()

# This function is to be called from app
def get_user_credentials(hashed_pw_file_path):
    
    
    with open(hashed_pw_file_path, "rb") as file:
        hashed_passwords = pickle.load(file)
    for email, (index, user_info) in zip(CREDENTIALS.keys(), enumerate(CREDS.values())):
        CREDS[email]['password'] = hashed_passwords[index]
    st_creds = {
        "usernames": CREDS
    }
    return st_creds

