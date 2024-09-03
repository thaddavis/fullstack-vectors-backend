from pydantic import BaseModel

class RearrangeSwarmPrompt(BaseModel):
    content: str
    sessionId: str
    agentsConfig: dict
    flow: str