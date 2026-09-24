"""Pydantic models for request/response validation."""

from typing import Optional, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    previous_interaction_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Calculate EMI for ₹5 lakh loan at 8% for 5 years",
                "previous_interaction_id": None,
            }
        }


class ChatResponse(BaseModel):
    reply: str
    interaction_id: Optional[str] = None
    tool_used: Optional[str] = None
    tool_result: Optional[Any] = None

    class Config:
        json_schema_extra = {
            "example": {
                "reply": "Your monthly EMI would be ₹10,138...",
                "interaction_id": "abc123",
                "tool_used": "calculate_emi",
                "tool_result": {"emi": 10138.0},
            }
        }


class NewChatResponse(BaseModel):
    message: str
