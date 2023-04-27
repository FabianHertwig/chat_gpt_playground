import pytest
from dotenv import load_dotenv

from src.llm_interface import MessageHistory, chat, get_default_system_message
from tests.test_config import no_online_tests


def test_chat_history_should_return_dict():
    # GIVEN
    message_history = MessageHistory("Hello, how are you?")
    # WHEN
    result = message_history.get_messages_as_dict()
    # THEN
    assert isinstance(result, list)
    assert isinstance(result[0], dict)


@pytest.mark.skipif(no_online_tests, reason="No online tests")
def test_chat_should_return_an_answer():
    load_dotenv()

    # GIVEN
    message_history = MessageHistory(get_default_system_message())
    # WHEN
    user_input = "Why did the chicken cross the road?"
    answer = chat(user_input, message_history=message_history)
    # THEN
    assert answer.get_messages()[-1].role == "assistant"
    assert answer.get_messages()[-1].content != ""
