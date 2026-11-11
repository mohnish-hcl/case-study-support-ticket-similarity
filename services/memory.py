from collections import deque

from services.config import (
    MAX_CHAT_HISTORY
)

chat_memory = deque(
    maxlen=MAX_CHAT_HISTORY
)


def add_user_message(message: str):

    chat_memory.append({
        "role": "user",
        "content": message
    })


def add_assistant_message(message: str):

    chat_memory.append({
        "role": "assistant",
        "content": message
    })


def get_chat_history():

    return list(chat_memory)


def build_history_text():

    history = []

    for message in chat_memory:

        history.append(
            f"{message['role'].upper()}: "
            f"{message['content']}"
        )

    return "\n".join(history)