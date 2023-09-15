import base64
from pathlib import Path
from model import deidentifier
from utils import render_file

import streamlit as st

# set the streamlit layout to be wide, don't have too many spaces
st.set_page_config(layout="wide")

st.title("Remove personal information from your documents with GPT 3.5.")

OPENAI_API_KEY = None
with st.sidebar:
    OPENAI_API_KEY = st.text_input("OpenAI API Key", key = "openai_api_key", type="password")

if not OPENAI_API_KEY:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

# handle session:
if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state['OPENAI_API_KEY'] = OPENAI_API_KEY 
st.info("Sucessfully added OpenAI key!")

if 'first_query' not in st.session_state:
    st.session_state['first_query'] = True

if 'assistant' not in st.session_state:
    st.session_state['assistant'] = None


uploaded_pdfs = st.file_uploader("Choose a pdf file to de-identify", accept_multiple_files = True)

if len(uploaded_pdfs) > 0 : 
    bytes_data = uploaded_pdfs[0].read()
else:
    st.info("Please upload a pdf file")
    st.stop()

with open("data/original/temp.pdf", "wb") as f:
    f.write(bytes_data)

# The first time, we send a query to openai endpoint
if st.session_state['first_query']:
    assistant = deidentifier(st.session_state['OPENAI_API_KEY'])
    assistant.pipeline()
    st.session_state['first_query'] = False
    st.session_state['assistant'] = assistant

# load the assistant from session state
assistant = st.session_state['assistant']

# choose the page to display corresponding redact word list
page_index = st.selectbox(
    'Select a single page to review the redact word list:',
    (str(i) for i in range(assistant.page_count)
))

redact_word_string = st.text_area('Redact word list detected by GPT 3.5, you can modify the list of words, seperate each word by a single comma:', ', '.join(assistant.redact_words[int(page_index)]))

render_btn = st.button("Visualize the files:")

if render_btn:
    # if there are changes to the redact words
    if redact_word_string != ', '.join(assistant.redact_words[int(page_index)]):
        assistant.redact_words[int(page_index)] = redact_word_string.split(', ')
        assistant.pipeline(send_query = False)

        # update session state
        st.session_state['assistant'] = assistant

    # render two pdfs
    render_file(bytes_data)
   
