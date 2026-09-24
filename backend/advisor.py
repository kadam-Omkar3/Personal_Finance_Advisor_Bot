"""
Gemini AI Finance Advisor
=========================
Handles all AI interactions using Google Gemini with:
- Multi-turn conversation support
- Function calling for finance calculators
- Streaming support
- Automatic retry for temporary 503 errors
"""

import os
import asyncio
from typing import AsyncGenerator, Optional

from google import genai
from google.genai import types

from tools import (
    calculate_emi,
    calculate_budget,
    calculate_savings_goal,
    calculate_fd_returns,
    calculate_sip_returns,
)


SYSTEM_INSTRUCTION = """You are FinBot, an expert Personal Finance Advisor specialized in Indian personal finance.

You help users with:
- Budgeting and expense planning (50/30/20 rule)
- Loan and EMI calculations
- Investment advice (SIP, FD, PPF, ELSS, NPS)
- Savings goal planning
- Tax saving tips under Section 80C
- Emergency fund planning
- Credit score improvement

Guidelines:
- Always respond in a friendly, professional manner
- Use Indian currency (₹ - Rupees) and Indian financial context
- When a user asks for calculations (EMI, SIP, budget, FD, savings goal), use the provided tools
- Provide actionable, practical advice
- For investment advice, always mention that markets carry risk
- Keep responses concise but comprehensive
- Use bullet points and formatting for clarity
- If user provides income/expenses, give personalized advice

You have access to these financial tools:
- calculate_emi: For loan EMI calculations
- calculate_budget: For budget planning using 50/30/20 rule
- calculate_savings_goal: To determine how long to reach a savings target
- calculate_fd_returns: For Fixed Deposit returns
- calculate_sip_returns: For SIP returns
"""


# ============================================================
# GEMINI FUNCTION DECLARATIONS
# ============================================================

FINANCE_TOOLS = [
    {
        "name": "calculate_emi",
        "description": "Calculate monthly EMI for a loan.",
        "parameters": {
            "type": "object",
            "properties": {
                "principal": {
                    "type": "number",
                    "description": "Loan principal amount in rupees"
                },
                "annual_rate": {
                    "type": "number",
                    "description": "Annual interest rate percentage"
                },
                "tenure_months": {
                    "type": "integer",
                    "description": "Loan tenure in months"
                }
            },
            "required": [
                "principal",
                "annual_rate",
                "tenure_months"
            ]
        }
    },

    {
        "name": "calculate_budget",
        "description": "Create a budget using the 50/30/20 rule.",
        "parameters": {
            "type": "object",
            "properties": {
                "monthly_income": {
                    "type": "number",
                    "description": "Net monthly income in rupees"
                }
            },
            "required": [
                "monthly_income"
            ]
        }
    },

    {
        "name": "calculate_savings_goal",
        "description": "Calculate how long it will take to reach a savings goal.",
        "parameters": {
            "type": "object",
            "properties": {
                "goal_amount": {
                    "type": "number",
                    "description": "Target savings amount in rupees"
                },
                "current_savings": {
                    "type": "number",
                    "description": "Current savings amount in rupees"
                },
                "monthly_contribution": {
                    "type": "number",
                    "description": "Monthly contribution in rupees"
                },
                "annual_rate": {
                    "type": "number",
                    "description": "Expected annual return percentage"
                }
            },
            "required": [
                "goal_amount",
                "current_savings",
                "monthly_contribution",
                "annual_rate"
            ]
        }
    },

    {
        "name": "calculate_fd_returns",
        "description": "Calculate FD maturity amount and interest earned.",
        "parameters": {
            "type": "object",
            "properties": {
                "principal": {
                    "type": "number",
                    "description": "FD principal amount in rupees"
                },
                "annual_rate": {
                    "type": "number",
                    "description": "Annual interest rate percentage"
                },
                "tenure_years": {
                    "type": "number",
                    "description": "FD tenure in years"
                },
                "compounding_frequency": {
                    "type": "integer",
                    "description": "Compounding frequency per year"
                }
            },
            "required": [
                "principal",
                "annual_rate",
                "tenure_years"
            ]
        }
    },

    {
        "name": "calculate_sip_returns",
        "description": "Calculate SIP returns and wealth created.",
        "parameters": {
            "type": "object",
            "properties": {
                "monthly_investment": {
                    "type": "number",
                    "description": "Monthly SIP amount in rupees"
                },
                "annual_rate": {
                    "type": "number",
                    "description": "Expected annual return percentage"
                },
                "tenure_years": {
                    "type": "number",
                    "description": "Investment tenure in years"
                }
            },
            "required": [
                "monthly_investment",
                "annual_rate",
                "tenure_years"
            ]
        }
    }
]


# ============================================================
# TOOL MAPPING
# ============================================================

TOOL_FUNCTIONS = {
    "calculate_emi": calculate_emi,
    "calculate_budget": calculate_budget,
    "calculate_savings_goal": calculate_savings_goal,
    "calculate_fd_returns": calculate_fd_returns,
    "calculate_sip_returns": calculate_sip_returns,
}


# ============================================================
# FINANCE ADVISOR
# ============================================================

class FinanceAdvisor:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set"
            )

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash"
        )

    # ========================================================
    # BUILD TOOLS
    # ========================================================

    def _build_tools(self):

        function_declarations = []

        for tool in FINANCE_TOOLS:

            function_declarations.append(
                types.FunctionDeclaration(
                    name=tool["name"],
                    description=tool["description"],
                    parameters=tool["parameters"],
                )
            )

        return [
            types.Tool(
                function_declarations=function_declarations
            )
        ]

    # ========================================================
    # GEMINI REQUEST WITH RETRY
    # ========================================================

    async def _generate_content_with_retry(
        self,
        contents,
        config,
        max_retries=3
    ):

        for attempt in range(max_retries):

            try:

                return self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config,
                )

            except Exception as e:

                error_text = str(e)

                is_temporary_error = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "high demand" in error_text.lower()
                )

                if not is_temporary_error:
                    raise

                if attempt == max_retries - 1:
                    raise

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                await asyncio.sleep(wait_time)

    # ========================================================
    # EXECUTE TOOL
    # ========================================================

    def _execute_tool(
        self,
        tool_name: str,
        arguments: dict
    ) -> dict:

        if tool_name not in TOOL_FUNCTIONS:

            return {
                "error": f"Unknown tool: {tool_name}"
            }

        try:

            result = TOOL_FUNCTIONS[tool_name](
                **arguments
            )

            return result

        except Exception as e:

            return {
                "error": str(e)
            }

    # ========================================================
    # CHAT
    # ========================================================

    async def chat(
        self,
        message: str,
        previous_interaction_id: Optional[str] = None,
    ) -> dict:

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=self._build_tools(),
        )

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=message
                    )
                ],
            )
        ]

        tool_used = None
        tool_result = None

        # ====================================================
        # FUNCTION CALL LOOP
        # ====================================================

        while True:

            response = await self._generate_content_with_retry(
                contents,
                config
            )

            if not response.candidates:
                return {
                    "reply": "Sorry, I could not generate a response.",
                    "interaction_id": None,
                    "tool_used": tool_used,
                    "tool_result": tool_result,
                }

            candidate = response.candidates[0]

            parts = candidate.content.parts

            function_call_part = None

            for part in parts:

                if (
                    hasattr(part, "function_call")
                    and part.function_call
                ):
                    function_call_part = part
                    break

            # =================================================
            # FUNCTION CALL
            # =================================================

            if function_call_part:

                fc = function_call_part.function_call

                tool_used = fc.name

                args = dict(fc.args)

                tool_result = self._execute_tool(
                    fc.name,
                    args
                )

                # IMPORTANT:
                # Preserve complete model response including
                # thought signature.

                contents.append(
                    candidate.content
                )

                # Add tool response

                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=fc.name,
                                response=tool_result,
                            )
                        ],
                    )
                )

                continue

            # =================================================
            # FINAL RESPONSE
            # =================================================

            text_parts = []

            for part in parts:

                if (
                    hasattr(part, "text")
                    and part.text
                ):
                    text_parts.append(part.text)

            reply = "\n".join(text_parts)

            break

        return {
            "reply": reply,
            "interaction_id": getattr(
                response,
                "response_id",
                None
            ),
            "tool_used": tool_used,
            "tool_result": tool_result,
        }

    # ========================================================
    # STREAMING CHAT
    # ========================================================

    async def chat_stream(
        self,
        message: str,
        previous_interaction_id: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=self._build_tools(),
        )

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=message
                    )
                ],
            )
        ]

        # ====================================================
        # FIRST REQUEST
        # ====================================================

        response = await self._generate_content_with_retry(
            contents,
            config
        )

        if not response.candidates:
            yield "Sorry, I could not generate a response."
            return

        candidate = response.candidates[0]

        parts = candidate.content.parts

        function_call_part = None

        for part in parts:

            if (
                hasattr(part, "function_call")
                and part.function_call
            ):
                function_call_part = part
                break

        # ====================================================
        # HANDLE TOOL
        # ====================================================

        if function_call_part:

            fc = function_call_part.function_call

            args = dict(fc.args)

            tool_result = self._execute_tool(
                fc.name,
                args
            )

            # Preserve model response

            contents.append(
                candidate.content
            )

            # Add tool result

            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=fc.name,
                            response=tool_result,
                        )
                    ],
                )
            )

        # ====================================================
        # STREAM FINAL RESPONSE
        # ====================================================

        stream_config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
        )

        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=stream_config,
        ):

            if (
                chunk.candidates
                and chunk.candidates[0].content
                and chunk.candidates[0].content.parts
            ):

                for part in chunk.candidates[0].content.parts:

                    if (
                        hasattr(part, "text")
                        and part.text
                    ):
                        yield part.text