import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit_authenticator as stauth
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from pathlib import Path
import time
from streamlit_lottie import st_lottie
from logger import Logger
from auth.auth_helper import get_user_credentials

import agents.digi_strategy as digi_strategy
import agents.management_messaging as management_messaging


# --- Initializations ---
log = Logger()
openai_api_key = st.secrets["openai_api_key"]

# --- Get query params from URL to determine which agent ---
query_params = st.query_params
agent_param = query_params.get("agent", "") if query_params is not None else ""
if (agent_param == "digiStrategy"):
    AGENT = digi_strategy
elif (agent_param == "managementMessaging"):
    AGENT = management_messaging
else:
    # Default agent is management messaging
    agent_param = "managementMessaging"
    AGENT = management_messaging


# --- Load baked in knowledge for respective agent
embeddings = OpenAIEmbeddings(api_key=openai_api_key)
VectorStore = FAISS.load_local(AGENT.KNOWLEDGE_FOLDER, embeddings=embeddings, allow_dangerous_deserialization=True)


# --- Sidebar contents ---
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 550px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
with st.sidebar:
    st.title("🤖 Docu Chat-Bot: " + AGENT.NAME)
    st.markdown(AGENT.DESCRIPTION)
    add_vertical_space(1)
    st.write(AGENT.CONTACT)


# --- User authentication ---
hashed_pw_file_path = Path(__file__).parent / "auth/hashed_pw.pkl"
st_creds = get_user_credentials(hashed_pw_file_path)
authenticator = stauth.Authenticate(st_creds, "pdf_chatbot", "BP2RnMBSTtK*wj", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("main")

if authentication_status == False:
    st.error("Your username or password is incorrect!")

if  authentication_status == None:
    st.warning("Please enter your username and password to interact with the agent!")


# --- Streamed response emulator ---
def response_generator(prompt):
    docs = VectorStore.similarity_search(query=prompt, k=3)
    llm = OpenAI(openai_api_key=openai_api_key)
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=prompt)
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

# --- Main page to interact with the agent ---
def main():
    authenticator.logout("Logout", "sidebar")

    # is_user_admin = st_creds["usernames"][username]["isAdmin"] == "True"

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"#### Welcome, {name} 👋")        
        st.header("Chat with Agent 💬")
    with col2:
        st_lottie(AGENT.AGENT_LOTTIE, key="user", quality="high", height="130px", width="130px")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # Accept user input
    if prompt := st.chat_input("Discuss about the document you just uploaded ..."):
    # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        log.log_to_firestore(username=username, agent=agent_param, question=prompt, answer=response)


if authentication_status:
    main()