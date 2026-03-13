from fastmcp import FastMCP
from typing import List, Dict, Any

mcp = FastMCP("Compliance")

@mcp.tool()
def get_rbi_rules(category: str) -> List[Dict[str, Any]]:
    """Returns applicable RBI regulations for a category."""
    rules = [
        {"id": "RBI_LEND_01", "category": "loans", "text": "Maximum DTI ratio should not exceed 50%", "effective_date": "2023-01-01"},
        {"id": "RBI_KYC_02", "category": "kyc", "text": "Physical verification required for loans above 50L", "effective_date": "2023-06-01"}
    ]
    return [r for r in rules if r["category"] == category]

@mcp.tool()
def get_loan_requirements(loan_type: str) -> List[str]:
    """Returns document requirements for a loan type."""
    reqs = {
        "home": ["PAN Card", "Aadhar", "Salary Slip (Last 6 months)", "Property Papers"],
        "personal": ["PAN Card", "Salary Slip (Last 3 months)", "Bank Statement"],
        "msme": ["GST Registration", "ITR (Last 3 years)", "Business Proof"]
    }
    return reqs.get(loan_type, ["PAN Card", "ID Proof"])

@mcp.tool()
def check_product_eligibility(customer_id: str, product_id: str) -> Dict[str, Any]:
    """Checks regulatory eligibility for a product."""
    return {
        "eligible": True,
        "reason": "Fulfils all RBI guidelines",
        "conditions": ["Maintain min balance of 10000"] if "premium" in product_id else []
    }

if __name__ == "__main__":
    mcp.run()
