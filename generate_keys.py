import pickle
from pathlib import Path

from streamlit_authenticator.utilities.hasher import Hasher

names = ["Deeraj Rajkarnikar", "Gábor Buday", "Jon Doe"]
usernames = ["deeraj.rk@gmail.com", "buday@gmail.com", "deeraj_@hotmail.com"]
passwords = ["**********", "**********", "**********"]

hashed_passwords = Hasher(passwords).generate()

file_path = Path(__file__).parent / "auth/hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)