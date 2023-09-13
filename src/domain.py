from enum import Enum
from fastapi.encoders import jsonable_encoder
import itertools
from pydantic import BaseModel


class Role(Enum):
    USER = "user"
    SYSTEM = "system"


class Message:
    id_generator: int = itertools.count(1)
    role: Role = None
    content: str = None

    def __init__(self, role: Role, content: str):
        self.id = next(self.id_generator)
        self.role = role
        self.content = content

    def __as_json__(self):
        return jsonable_encoder({"role": self.role, "content": self.content})


class ChatLog(BaseModel):
    messages: list
    id_map: dict[int, int]
    num_of_messages: int = 0

    def add_message(self, message: Message):
        self.messages.append(message.__as_json__())
        self.num_of_messages += 1
        self.id_map[message.id] = self.num_of_messages - 1
