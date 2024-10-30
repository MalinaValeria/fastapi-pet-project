from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MessageRead(BaseModel):
    id: int = Field(..., description='Message ID')
    sender: int = Field(..., description='Sender')
    recipient: int = Field(..., description='Recipient')
    content: str = Field(..., description='Message content')
    created_at: Optional[datetime] = Field(..., description='Message creation time')


class MessageCreate(BaseModel):
    recipient: int = Field(..., description='Recipient ID')
    content: str = Field(..., description='Message content')
