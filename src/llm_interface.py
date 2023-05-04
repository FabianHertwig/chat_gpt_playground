import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import openai

logger = logging.getLogger(__name__)


def configure_openai_api(
    api_key, api_type="open_ai", api_base="https://api.openai.com/v1", api_version=None
):
    openai.api_key = api_key
    openai.api_base = api_base
    openai.api_type = api_type
    openai.api_version = api_version


class Role(str, Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"


@dataclass
class Message:
    role: Role
    content: str


class MessageHistory:
    def __init__(self, system_message: str, history_length: int = 10):
        self.messages = [Message(Role.SYSTEM, system_message)]
        self.history_length = history_length

    def add_message(self, role, content):
        self.messages.append(Message(role, content))
        self.messages = self.messages[-self.history_length :]

    def get_messages(self):
        return self.messages

    def get_messages_as_dict(self):
        return [message.__dict__ for message in self.messages]


def get_default_system_message():
    knowledge_cutoff = "September 2021"
    current_date = datetime.now().strftime("%B %d, %Y")
    return (
        "You are ChatGPT, a large language model trained by OpenAI."
        " Answer as concisely as possible. "
        f"Knowledge cutoff: {knowledge_cutoff} Current date: {current_date}"
    )


def chat(message, message_history: MessageHistory, model, engine):
    message_history.add_message(Role.USER, message)

    logger.debug(f"{model=}, {engine=},")
    result = openai.ChatCompletion.create(
        model=model, engine=engine, messages=message_history.get_messages_as_dict()
    )
    message_history.add_message(
        Role(result.choices[0].message.role), result.choices[0].message.content
    )
    return message_history
