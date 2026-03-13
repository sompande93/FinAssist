from fastmcp import FastMCP
from typing import List, Dict, Any

mcp = FastMCP("Credit")

@mcp.tool()
def get_credit_profile(customer_id: str) -> Dict[str, Any]:
    """Returns credit score, history months, and defaults count."""
    profiles = {
        "CUST_001": {"score": 780, "history_months": 48, "defaults": 0},
        "S2_LOAN_CUST": {"score": 750, "history_months": 36, "defaults": 0},
        "S3_FRAUD_CUST": {"score": 600, "history_months": 12, "defaults": 2}
    }
    return profiles.get(customer_id, {"score": 650, "history_months": 24, "defaults": 0})

@mcp.tool()
def get_emi_schedule(customer_id: str) -> List[Dict[str, Any]]:
    """Returns all active EMIs with amounts and due dates."""
    emis = {
        "S2_LOAN_CUST": [
            {"loan_id": "LN_S2_1", "amount": 25000, "due_date": "2024-04-05"},
            {"loan_id": "LN_S2_2", "amount": 15000, "due_date": "2024-04-15"}
        ]
    }
    return emis.get(customer_id, [])

@mcp.tool()
def check_loan_eligibility(customer_id: str, amount: float, type: str) -> Dict[str, Any]:
    """Checks if a customer is eligible for a loan based on basic criteria."""
    profile = get_credit_profile(customer_id)
    score = profile["score"]
    
    eligible = score > 700
    reason = "High credit score" if eligible else "Insufficient credit score"
    max_amount = 5000000 if score > 750 else 1000000
    
    return {
        "eligible": eligible,
        "reason": reason,
        "max_amount": max_amount,
        "interest_rate": 8.5 if score > 750 else 10.5
    }

if __name__ == "__main__":
    mcp.run()
