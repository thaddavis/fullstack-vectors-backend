from pydantic import BaseModel

class ChatSessionPrompt(BaseModel):
    content: str
    sessionId: str