"""
Finance Calculator Tools
========================
Pure Python financial calculation functions used by the AI via function calling.
All amounts are in Indian Rupees (₹).
"""

import math


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> dict:
    """
    Calculate EMI using the standard formula:
    EMI = P × r × (1 + r)^n / ((1 + r)^n - 1)
    """
    if annual_rate == 0:
        emi = principal / tenure_months
        total_payment = emi * tenure_months
        return {
            "emi": round(emi, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": 0,
            "principal": principal,
            "annual_rate": annual_rate,
            "tenure_months": tenure_months,
        }

    monthly_rate = annual_rate / (12 * 100)
    emi = principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months) / \
          (math.pow(1 + monthly_rate, tenure_months) - 1)

    total_payment = emi * tenure_months
    total_interest = total_payment - principal

    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "principal": principal,
        "annual_rate": annual_rate,
        "tenure_months": tenure_months,
        "tenure_years": round(tenure_months / 12, 1),
    }


def calculate_budget(monthly_income: float) -> dict:
    """
    Create a budget plan using the 50/30/20 rule:
    - 50% for needs (rent, food, utilities, EMIs)
    - 30% for wants (entertainment, dining out, shopping)
    - 20% for savings & investments
    """
    needs = monthly_income * 0.50
    wants = monthly_income * 0.30
    savings = monthly_income * 0.20

    return {
        "monthly_income": monthly_income,
        "needs_50_percent": round(needs, 2),
        "wants_30_percent": round(wants, 2),
        "savings_20_percent": round(savings, 2),
        "breakdown": {
            "needs": {
                "total": round(needs, 2),
                "rent_suggested": round(needs * 0.45, 2),
                "food_groceries": round(needs * 0.25, 2),
                "utilities_transport": round(needs * 0.20, 2),
                "insurance_emis": round(needs * 0.10, 2),
            },
            "wants": {
                "total": round(wants, 2),
                "entertainment": round(wants * 0.30, 2),
                "dining_out": round(wants * 0.25, 2),
                "shopping": round(wants * 0.25, 2),
                "subscriptions": round(wants * 0.20, 2),
            },
            "savings": {
                "total": round(savings, 2),
                "emergency_fund": round(savings * 0.25, 2),
                "sip_investments": round(savings * 0.50, 2),
                "short_term_goals": round(savings * 0.25, 2),
            }
        }
    }


def calculate_savings_goal(
    goal_amount: float,
    current_savings: float,
    monthly_contribution: float,
    annual_rate: float,
) -> dict:
    """
    Calculate months needed to reach savings goal with compound interest.
    """
    if monthly_contribution <= 0:
        return {"error": "Monthly contribution must be greater than 0"}

    remaining = goal_amount - current_savings
    if remaining <= 0:
        return {
            "goal_amount": goal_amount,
            "current_savings": current_savings,
            "months_needed": 0,
            "years_needed": 0,
            "message": "You have already reached your savings goal! 🎉",
        }

    monthly_rate = annual_rate / (12 * 100)

    if monthly_rate == 0:
        months = math.ceil(remaining / monthly_contribution)
    else:
        # Solve: FV = PMT * ((1+r)^n - 1) / r + PV * (1+r)^n
        # Using numerical approach
        months = 0
        balance = current_savings
        while balance < goal_amount and months < 1200:  # cap at 100 years
            balance = balance * (1 + monthly_rate) + monthly_contribution
            months += 1

    total_contributed = monthly_contribution * months + current_savings
    interest_earned = goal_amount - total_contributed

    return {
        "goal_amount": goal_amount,
        "current_savings": current_savings,
        "monthly_contribution": monthly_contribution,
        "annual_rate": annual_rate,
        "months_needed": months,
        "years_needed": round(months / 12, 1),
        "total_contributed": round(total_contributed, 2),
        "interest_earned": round(max(interest_earned, 0), 2),
    }


def calculate_fd_returns(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    compounding_frequency: int = 4,
) -> dict:
    """
    Calculate Fixed Deposit maturity value using compound interest:
    A = P * (1 + r/n)^(n*t)
    """
    n = compounding_frequency
    t = tenure_years
    r = annual_rate / 100

    maturity_amount = principal * math.pow(1 + r / n, n * t)
    interest_earned = maturity_amount - principal

    compounding_map = {1: "Annually", 2: "Semi-Annually", 4: "Quarterly", 12: "Monthly"}
    compounding_label = compounding_map.get(n, f"{n} times/year")

    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "tenure_years": tenure_years,
        "compounding": compounding_label,
        "maturity_amount": round(maturity_amount, 2),
        "interest_earned": round(interest_earned, 2),
        "effective_annual_rate": round((math.pow(1 + r / n, n) - 1) * 100, 2),
    }


def calculate_sip_returns(
    monthly_investment: float,
    annual_rate: float,
    tenure_years: float,
) -> dict:
    """
    Calculate SIP returns using the standard SIP formula:
    FV = P × ((1 + r)^n - 1) / r × (1 + r)
    where r = monthly rate, n = number of months
    """
    monthly_rate = annual_rate / (12 * 100)
    n = int(tenure_years * 12)

    if monthly_rate == 0:
        future_value = monthly_investment * n
    else:
        future_value = monthly_investment * (math.pow(1 + monthly_rate, n) - 1) / monthly_rate * (1 + monthly_rate)

    total_invested = monthly_investment * n
    wealth_gained = future_value - total_invested

    return {
        "monthly_investment": monthly_investment,
        "annual_rate": annual_rate,
        "tenure_years": tenure_years,
        "total_months": n,
        "total_invested": round(total_invested, 2),
        "future_value": round(future_value, 2),
        "wealth_gained": round(wealth_gained, 2),
        "returns_percentage": round((wealth_gained / total_invested) * 100, 2) if total_invested > 0 else 0,
    }
