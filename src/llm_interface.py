from dataclasses import dataclass
from datetime import datetime

import openai


def get_default_system_message():
    knowledge_cutoff = "September 2021"
    current_date = datetime.now().strftime("%B %d, %Y")
    return (
        "You are ChatGPT, a large language model trained by OpenAI."
        " Answer as concisely as possible. "
        f"Knowledge cutoff: {knowledge_cutoff} Current date: {current_date}"
    )


def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message


@dataclass
class Message:
    role: str
    content: str


class MessageHistory:
    def __init__(self, system_message: str, history_length: int = 10):
        self.messages = [Message("system", system_message)]
        self.history_length = history_length

    def add_message(self, role, content):
        self.messages.append(Message(role, content))
        self.messages = self.messages[-self.history_length :]

    def get_messages(self):
        return self.messages

    def get_messages_as_dict(self):
        return [message.__dict__ for message in self.messages]


def chat(message, message_history: MessageHistory):
    message_history.add_message("user", message)
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message_history.get_messages_as_dict()
    )
    message_history.add_message(
        result.choices[0].message.role, result.choices[0].message.content
    )
    return message_history
