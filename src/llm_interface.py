from dataclasses import dataclass
import openai


def get_default_system_message(knowledge_cutoff, current_date):
    ("You are ChatGPT, a large language model trained by OpenAI."
     " Answer as concisely as possible. "
     "Knowledge cutoff: {knowledge_cutoff} Current date: {current_date}")

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
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

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

def chat(message, message_history, system_message):
    openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )