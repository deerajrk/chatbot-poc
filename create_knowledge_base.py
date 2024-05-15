from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import streamlit as st


pdf_path = input("Enter path to the PDF: ")
chunk_size = input("Enter chunk size (1000): ")
chunk_overlap = input("Enter chunk overlap (200): ")
knowledge_folder_name = input("Enter folder name to save knowledge about the PDF: ")

openai_api_key = st.secrets["openai_api_key"]

pdf_reader = PdfReader(pdf_path)

text = ""
for page in pdf_reader.pages:
    text += page.extract_text()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
chunks = text_splitter.split_text(text=text)

embeddings = OpenAIEmbeddings(api_key=openai_api_key)
VectorStore = FAISS.from_texts(chunks, embedding=embeddings)

VectorStore.save_local("./knowledge_base/" + knowledge_folder_name)
