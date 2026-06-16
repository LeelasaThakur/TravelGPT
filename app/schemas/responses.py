from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatResponse(BaseModel):
    reply: str
    intent: str
    requires_action: bool = False
    options: List[Dict[str, Any]] = []

class BaseAPIResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
