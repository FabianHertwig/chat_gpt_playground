import logging

import streamlit as st
from streamlit_chat import message

from src.app.login import check_password
from src.app.secrets import get_secret
from src.llm_interface import (
    MessageHistory,
    Role,
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
        st.markdown("# Settings")
        history_length = st.slider(
            "Messages in context",
            1,
            100,
            10,
            key="history_length",
            help=(
                "The number of messages of the current conversation "
                "which are used as context for the model."
            ),
        )
        temperature = st.slider(
            "Temperature",
            0.0,
            2.0,
            1.0,
            0.1,
            key="temperature",
            help=(
                "What sampling temperature to use, between 0 and 2. "
                "Higher values like 0.8 will make the output more random, "
                "while lower values like 0.2 will make it more focused and "
                "deterministic."
            ),
        )
        top_p = st.slider(
            "Top P",
            0.0,
            1.0,
            1.0,
            0.1,
            key="top_p",
            help=(
                "An alternative to sampling with temperature, called nucleus sampling, "
                "where the model considers the results of the tokens with top_p "
                "probability mass. So 0.1 means only the tokens comprising the "
                "top 10% probability mass are considered."
            ),
        )

    st.title("Chat GPT Playground")

    if "message_history" not in st.session_state:
        st.session_state["message_history"] = MessageHistory(
            system_message, history_length
        )

    if st.button("Clear chat"):
        st.session_state.message_history = MessageHistory(
            system_message, history_length
        )
    st.session_state.message_history.history_length = history_length

    def send_message():
        message_history = chat(
            st.session_state["input"],
            st.session_state.message_history,
            model=open_ai_model,
            engine=open_ai_engine,
        )
        st.session_state.message_history = message_history
        st.session_state["input"] = ""

    user_input = st.text_area(
        "You: ", "", key="input", on_change=send_message, height=200
    )

    for i, mes in enumerate(st.session_state.message_history.get_messages()[::-1]):
        if mes.role == Role.SYSTEM:
            continue

        is_user = mes.role == Role.USER
        if is_user:
            avatar_id = 10
        else:
            avatar_id = 11
        message(
            mes.content, is_user=is_user, key=i, avatar_style="thumbs", seed=avatar_id
        )
