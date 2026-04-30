from pydantic import BaseModel, Field
from typing import Optional


class Chat(BaseModel):
    id: int
    type: str
    title: Optional[str] = None


class User(BaseModel):
    id: int
    is_bot: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Message(BaseModel):
    message_id: int
    date: int
    chat: Chat
    text: Optional[str] = None
    from_user: Optional[User] = Field(default=None, alias="from")


class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    channel_post: Optional[Message] = None