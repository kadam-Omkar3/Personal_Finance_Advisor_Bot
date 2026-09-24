"""
Personal Finance Advisor Bot - FastAPI Backend
============================================
Main entry point with API routes and streaming support.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

from models import ChatRequest, ChatResponse, NewChatResponse
from advisor import FinanceAdvisor

load_dotenv()

app = FastAPI(
    title="Personal Finance Advisor Bot",
    description="AI-powered personal finance advisor using Google Gemini",
    version="1.0.0",
)

# CORS — allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

advisor = FinanceAdvisor()


@app.get("/")
async def root():
    return {
        "message": "Personal Finance Advisor Bot API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat/new", response_model=NewChatResponse)
async def new_chat():
    """Start a new conversation session."""
    return NewChatResponse(message="New conversation started. How can I help you with your finances today?")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the finance advisor.
    Supports stateful multi-turn conversation via previous_interaction_id.
    """
    try:
        result = await advisor.chat(
            message=request.message,
            previous_interaction_id=request.previous_interaction_id,
        )
        return ChatResponse(
            reply=result["reply"],
            interaction_id=result["interaction_id"],
            tool_used=result.get("tool_used"),
            tool_result=result.get("tool_result"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming endpoint — sends tokens as Server-Sent Events (SSE).
    """
    async def generate():
        try:
            async for chunk in advisor.chat_stream(
                message=request.message,
                previous_interaction_id=request.previous_interaction_id,
            ):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/tools")
async def list_tools():
    """List available finance calculator tools."""
    return {
        "tools": [
            {
                "name": "calculate_emi",
                "description": "Calculate monthly EMI for a loan",
                "parameters": ["principal", "annual_rate", "tenure_months"],
            },
            {
                "name": "calculate_budget",
                "description": "50/30/20 budget planner",
                "parameters": ["monthly_income"],
            },
            {
                "name": "calculate_savings_goal",
                "description": "Time to reach a savings target",
                "parameters": ["goal_amount", "current_savings", "monthly_contribution", "annual_rate"],
            },
            {
                "name": "calculate_fd_returns",
                "description": "Fixed Deposit maturity calculator",
                "parameters": ["principal", "annual_rate", "tenure_years", "compounding_frequency"],
            },
            {
                "name": "calculate_sip_returns",
                "description": "SIP investment returns calculator",
                "parameters": ["monthly_investment", "annual_rate", "tenure_years"],
            },
        ]
    }
