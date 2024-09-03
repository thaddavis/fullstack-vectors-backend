from pydantic import BaseModel

class SpreadsheetSwarmPrompt(BaseModel):
    content: str
    sessionId: str
    agentsConfig: dict