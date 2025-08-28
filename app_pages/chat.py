import os 
from dotenv import load_dotenv
import streamlit as st
import logging
import time
from modules.ragRetrivalProcess import retrive_rag_info

load_dotenv()

tenant_id = os.getenv('TENANT_ID')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
dbname = os.getenv('DBNAME')
openai_api_key = os.getenv('OPENAI_API_KEY')
llama_cloud_api_key = os.getenv('LLAMA_CLOUD_API_KEY')

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["LLAMA_CLOUD_API_KEY"] = llama_cloud_api_key

connection_string = f'postgresql+psycopg://{username}:{password}@{host}:{port}/{dbname}'


def display_chatbot_page(selected_site_id):
    """
    This function will display the chatbot UI interface and we can query the chatbot with this UI
    """
    
    # Dynamically load logo based on the selected site name
    logo_path = f'logos/{selected_site_id}.png'  # Ensure filenames match site names

    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    else:
        st.title("LUCAS CHATBOT")

    if 'messages' not in st.session_state:
        default_chat_message = {"role": "assistant", "content": f"Hello! I am your chat assistant. How can I help you today?"}
        st.session_state['messages'] = [default_chat_message]
    if 'processing' not in st.session_state:
        st.session_state['processing'] = False
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    logging.info('Chatbot page loaded')

    if 'messages' in st.session_state:
        for message in st.session_state['messages']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the uploaded documents:", key="user_input"):
        st.session_state['messages'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state['processing'] = True
        response = retrive_rag_info(prompt, selected_site_id, tenant_id)
        st.session_state['processing'] = False
        response_text = ""
        with st.chat_message("assistant"):
            text_container = st.empty()
            text = ""
            for chunk in response:
                chunk_message = chunk.choices[0].delta.content  # extract the message
                if(chunk_message is None):
                    continue
                text += chunk_message
                text_container.markdown(text)
                time.sleep(0.003)
            response_text = text
        
        st.session_state['messages'].append({"role": "assistant", "content": response_text})
        st.rerun()
