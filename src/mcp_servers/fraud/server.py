from fastmcp import FastMCP
from typing import List, Dict, Any

mcp = FastMCP("Fraud")

@mcp.tool()
def score_transaction_risk(txn_id: str, amount: float, payee_id: str) -> Dict[str, Any]:
    """Returns risk score and flag list for a transaction."""
    score = 0.85 if payee_id == "UNKNOWN_PAYEE" or amount > 40000 else 0.1
    flags = ["unknown_payee"] if score > 0.7 else []
    return {"risk_score": score, "flags": flags}

@mcp.tool()
def get_customer_alerts(customer_id: str) -> List[Dict[str, Any]]:
    """Returns active fraud alerts for a customer."""
    alerts = {
        "S3_FRAUD_CUST": [{"id": "ALRT_001", "severity": "high", "date": "2024-03-12", "reason": "Suspicious login from new device"}]
    }
    return alerts.get(customer_id, [])

@mcp.tool()
def flag_transaction(txn_id: str, reason: str) -> Dict[str, Any]:
    """Creates a fraud case for a transaction."""
    return {
        "case_id": f"CASE_{txn_id}",
        "status": "flagged",
        "escalation_flag": True
    }

if __name__ == "__main__":
    mcp.run()
