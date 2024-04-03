import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit_authenticator as stauth

from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

import pickle
from pathlib import Path
import os

 
# Sidebar contents
with st.sidebar:
    st.title("🤖 Docu Chat-Bot")
    st.markdown("""
    ## About
    Curious about something? 
    Just ask! Our chat-bot, powered by cutting-edge large language models (LLM), 
    has been trained on a library of documents. 
                
    This allows it to answer your questions in a clear and conversational way.
    Think of it as having your own personal knowledge expert,
    with all the information pre-loaded and ready to be tapped into!
                
    This app is currently in proof of concept (PoC) phase.
    """)
    add_vertical_space(5)
    st.write("### For more information contact:")
    st.write("📧 Gábor Buday [budayg@gmail.com]")
    st.write("📧 Deeraj Rajkarnikar [deeraj.rk@gmail.com]")
    add_vertical_space(3)
 

# --- User authentication ---
hashed_pw_file_path = Path(__file__).parent / "auth/hashed_pw.pkl"
with hashed_pw_file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {
    "usernames": {
        "deeraj.rk@gmail.com": {
            "name": "Deeraj Rajkarnikar",
            "password": hashed_passwords[0],
            "isAdmin": "True"
        },
        "buday@gmail.com": {
            "name": "Gábor Buday",
            "password": hashed_passwords[1],
            "isAdmin": "True"
        },
        "deeraj_@hotmail.com": {
            "name": "Jon Doe",
            "password": hashed_passwords[2],
            "isAdmin": "False"
        }
    }
}

authenticator = stauth.Authenticate(credentials, "pdf_chatbot", "BP2RnMBSTtK*wj", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("main")

if authentication_status == False:
    st.error("Your username or password is incorrect!")

if  authentication_status == None:
    st.warning("Please enter your username and password")



def main():
    # load_dotenv()

    authenticator.logout("Logout", "sidebar")

    st.write(f"## Welcome {name}")

    st.header("Chat with PDF 💬")
 
    openai_api_key = st.text_input("Enter OpenAI API key:")

    # upload a PDF file
    pdf = st.file_uploader("Upload your PDF", type="pdf")
 
    # st.write(pdf)
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
 
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
        chunks = text_splitter.split_text(text=text)
 
        # # embeddings
        store_name = pdf.name[:-4]
        st.write(f"{store_name}")
        # st.write(chunks)
 
        # if os.path.exists(f"{store_name}.pkl"):
        #     with open(f"{store_name}.pkl", "rb") as f:
        #         VectorStore = pickle.load(f)
        #     # st.write("Embeddings Loaded from the Disk")s
        # else:
        #     embeddings = OpenAIEmbeddings()
        #     VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        #     with open(f"{store_name}.pkl", "wb") as f:
        #         pickle.dump(VectorStore, f)

        embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
 
        # embeddings = OpenAIEmbeddings()
        # VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
 
        # Accept user questions/query
        query = st.text_input("Ask questions about your PDF file:")
        # st.write(query)
 
        if query:
            docs = VectorStore.similarity_search(query=query, k=3)
 
            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(cb)
            st.write(response)


if authentication_status:
    main()