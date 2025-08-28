import streamlit as st
from app_pages.files import display_directory_page
from app_pages.chat import display_chatbot_page
import logging
from config.tenant_site_mapping import tenant_site_mapping
from modules.constant import default_tenant_name

# logging.basicConfig(
#     format='%(asctime)s - %(message)s',
#     level=logging.INFO
# )
logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Azure Data Lake & Chatbot Explorer", layout="wide")

st.sidebar.title("Navigation")

# Keep the tenant site mapping logic
site_mapping = {site['displayName']: site['id'] for site in tenant_site_mapping[default_tenant_name]}
display_names = list(site_mapping.keys())

selected_display_name = st.sidebar.selectbox('Select Site:', display_names)
logging.info(str(display_names))
selected_site_id = site_mapping[selected_display_name]

logging.info("**********")
logging.info(selected_site_id)

        
page = st.sidebar.selectbox("Choose a page", ["Chatbot Interface", "Directory Control"])

if page == "Chatbot Interface":
    logging.info("Chatbot Interface")
    display_chatbot_page(selected_site_id)  # Call the chatbot page function
elif page == "Directory Control":
    logging.info("Directory Control")
    display_directory_page(selected_site_id)  # Call the directory page function
