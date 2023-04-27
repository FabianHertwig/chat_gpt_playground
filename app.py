import openai
import streamlit as st
from streamlit_chat import message

from src.llm_interface import MessageHistory, chat, get_default_system_message

openai.api_key = st.secrets["open_ai_api_key"]


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
    message_history = chat(st.session_state["input"], st.session_state.message_history)
    st.session_state.message_history = message_history
    st.session_state["input"] = ""


user_input = st.text_input("You: ", "", key="input", on_change=clear_text_input)


for i, mes in enumerate(st.session_state.message_history.get_messages()[::-1]):
    is_user = mes.role == "user"
    if is_user:
        avatar_id = 10  # 6
    else:
        avatar_id = 11
    message(mes.content, is_user=is_user, key=i, avatar_style="thumbs", seed=avatar_id)
