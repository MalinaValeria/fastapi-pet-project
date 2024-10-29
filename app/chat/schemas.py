from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MessageRead(BaseModel):
    id: int = Field(..., description='Message ID')
    sender_id: int = Field(..., description='Sender ID')
    recipient_id: int = Field(..., description='Recipient ID')
    content: str = Field(..., description='Message content')
    created_at: Optional[datetime] = Field(..., description='Message creation time')


class MessageCreate(BaseModel):
    recipient_id: int = Field(..., description='Recipient ID')
    content: str = Field(..., description='Message content')
