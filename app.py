import logging

import streamlit as st
from streamlit_chat import message

from src.app.login import check_password
from src.app.secrets import get_secret
from src.llm_interface import (
    MessageHistory,
    chat,
    configure_openai_api,
    get_default_system_message,
)

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        "%(asctime)s.%(msecs)03d %(levelname)s %(module)s"
        " - %(funcName)s: %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger = logging.getLogger(__name__)

open_ai_api_key = get_secret("open_ai_api_key")
open_ai_model = get_secret("open_ai_model", is_optional=True)
open_ai_engine = get_secret("open_ai_engine", is_optional=True)
open_ai_api_type = get_secret("open_ai_api_type", "openai", is_optional=True)
open_ai_api_base = get_secret(
    "open_ai_api_base", "https://api.openai.com/v1", is_optional=True
)
open_ai_api_version = get_secret("open_ai_api_version", is_optional=True)

configure_openai_api(
    open_ai_api_key, open_ai_api_type, open_ai_api_base, open_ai_api_version
)

if check_password():
    with st.sidebar:
        system_message = st.text_area(
            "System Message",
            key="system_message",
            value=get_default_system_message(),
            height=200,
        )

    # Creating the chatbot interface
    st.title("Chat GPT Playground")

    # Storing the chat
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = MessageHistory(system_message)

    if st.button("Clear chat"):
        st.session_state.message_history = MessageHistory(system_message)

    def clear_text_input():
        message_history = chat(
            st.session_state["input"],
            st.session_state.message_history,
            model=open_ai_model,
            engine=open_ai_engine,
        )
        st.session_state.message_history = message_history
        st.session_state["input"] = ""

    user_input = st.text_input("You: ", "", key="input", on_change=clear_text_input)

    for i, mes in enumerate(st.session_state.message_history.get_messages()[::-1]):
        is_user = mes.role == "user"
        if is_user:
            avatar_id = 10  # 6
        else:
            avatar_id = 11
        message(
            mes.content, is_user=is_user, key=i, avatar_style="thumbs", seed=avatar_id
        )
