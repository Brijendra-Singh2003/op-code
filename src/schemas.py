from pydantic import BaseModel, Field


class Chat(BaseModel):
    id: int
    type: str
    title: str | None = "None"


class User(BaseModel):
    id: int
    is_bot: bool = False
    first_name: str | None = None


class Message(BaseModel):
    message_id: int
    date: int
    chat: Chat
    text: str = ""
    from_user: User = Field(alias="from")


class Update(BaseModel):
    update_id: int
    message: Message | None = None
    channel_post: Message | None = None
