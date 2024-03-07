import streamlit as st
from urllib.request import urlopen
from langchain_community.vectorstores import ElasticsearchStore
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import Bedrock
from langchain.chains import RetrievalQA
import boto3
import json
from dataclasses import dataclass
from typing import Literal
import os
import streamlit.components.v1 as components



st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str


def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


st.markdown("""
<div style="text-align: center; margin-top: 10px;">
    <img src="https://github.com/EloiseYiyunXu/AI-Chatbot.github.io/blob/main/static/nfl.png?raw=true" alt="NFL Logo" class="nfl-logo"/>
</div>
""", unsafe_allow_html=True)


def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0

    # Adding an initial greeting from the AI if the chat history is empty
    if not st.session_state.history:  # Check if the history is empty
        st.session_state.history.append(Message("ai", "Welcome Seahawk fans, how can I help you? 🤗"))


if "retriever" not in st.session_state:
    AWS_ACCESS_KEY = st.secrets['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = st.secrets['AWS_SECRET_KEY']
    AWS_REGION = st.secrets['AWS_REGION']

    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    CLOUD_ID = st.secrets['ELASTIC_SEARCH_ID']
    CLOUD_USERNAME = "elastic"
    CLOUD_PASSWORD = st.secrets['ELASTIC_PASSWORD']

    vector_store = ElasticsearchStore(
        es_cloud_id=CLOUD_ID,
        es_user=CLOUD_USERNAME,
        es_password=CLOUD_PASSWORD,
        index_name="seahawk6",
        strategy=ElasticsearchStore.SparseVectorRetrievalStrategy()
    )

    default_model_id = "amazon.titan-text-express-v1"
    AWS_MODEL_ID = default_model_id
    llm = Bedrock(
        client=bedrock_client,
        model_id=AWS_MODEL_ID
    )

    retriever = vector_store.as_retriever()

    st.session_state.retriever = RetrievalQA.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )


def llm_response_temp(human_prompt):
    response = st.session_state.retriever(human_prompt)
    answer = response['result']
    source = []
    for doc in response["source_documents"]:
        source = doc.metadata['title']

    return answer, source


def on_click_callback():
    human_prompt = st.session_state.human_prompt
    llm_response, llm_source = llm_response_temp(human_prompt)
    st.session_state.history.append(
        Message("human", human_prompt)
    )
    st.session_state.history.append(
        Message("ai", llm_response)
    )


load_css()
initialize_session_state()


page_bg_img = """
<style>
[data-testid= "stAppViewContainer"] {
background-image: url("https://github.com/EloiseYiyunXu/AI-Chatbot.github.io/blob/main/static/bg.png?raw=true");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center; font-family: "Montserrat", sans-serif; font-size: 40px; font-weight: bold; color: #005f73;'>
    Seahawk 2024 Draft AI Chatbot
</h1>""", unsafe_allow_html=True)

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
credit_card_placeholder = st.empty()

ai_icon_url = "https://raw.githubusercontent.com/zzjy222/seahawkAItool.github.io/main/static/Seahawks_Chatbot_Logo.png"
user_icon_url = "https://raw.githubusercontent.com/zzjy222/seahawkAItool.github.io/main/static/human.png"

with chat_placeholder:
    for chat in st.session_state.history:
        image_url = ai_icon_url if chat.origin == 'ai' else user_icon_url
        div = f"""
<div class="chat-row 
    {'' if chat.origin == 'ai' else 'row-reverse'}">
    <img class="chat-icon" src="{image_url}"
         width=32 height=32>
    <div class="chat-bubble
    {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
        {chat.message}
</div>
        """
        st.markdown(div, unsafe_allow_html=True)

    for _ in range(3):
        st.markdown("")

with prompt_placeholder:
    st.markdown("**Chat**")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        value="Who should Seahawks pick at No.16",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "Submit",
        type="primary",
        on_click=on_click_callback,
    )

credit_card_placeholder.caption(f"""
Used {st.session_state.token_count} tokens""")

components.html("""
<script>
const streamlitDoc = window.parent.document;

const buttons = Array.from(
    streamlitDoc.querySelectorAll('.stButton > button')
);
const submitButton = buttons.find(
    el => el.innerText === 'Submit'
);

streamlitDoc.addEventListener('keydown', function(e) {
    switch (e.key) {
        case 'Enter':
            submitButton.click();
            break;
    }
});
</script>
""",
                height=0,
                width=0,
                )
