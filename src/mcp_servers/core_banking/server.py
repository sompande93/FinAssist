from fastmcp import FastMCP
from typing import List, Dict, Any
import random

mcp = FastMCP("CoreBanking")

# Sample mock data for direct tool returns
MOCK_ACCOUNTS = {
    "CUST_001": [
        {"id": "ACC_101", "type": "savings", "balance": 15000.50, "status": "active", "last_txn_date": "2024-03-12"},
        {"id": "ACC_102", "type": "fd", "balance": 500000.00, "status": "active", "last_txn_date": "2024-01-01"}
    ],
    "S2_LOAN_CUST": [
        {"id": "ACC_S2", "type": "savings", "balance": 45000.00, "status": "active", "last_txn_date": "2024-03-10"}
    ],
    "S3_FRAUD_CUST": [
        {"id": "ACC_FRAUD_001", "type": "savings", "balance": 1000.00, "status": "active", "last_txn_date": "2024-03-12"}
    ],
    "S8_INACTIVE_CUST": [
        {"id": "ACC_INACTIVE_001", "type": "savings", "balance": 5000.00, "status": "inactive", "last_txn_date": "2024-01-10"}
    ]
}

@mcp.tool()
def get_account_summary(customer_id: str) -> List[Dict[str, Any]]:
    """Returns balance, type, status, and last txn date for all accounts of a customer."""
    return MOCK_ACCOUNTS.get(customer_id, [])

@mcp.tool()
def get_transactions(account_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Returns transaction history for a specific account."""
    # Mock transactions
    txns = []
    for i in range(limit):
        txns.append({
            "id": f"TXN_{account_id}_{i}",
            "amount": round(random.uniform(500, 5000), 2),
            "timestamp": "2024-03-12T12:00:00",
            "payee_id": f"PAYEE_{i}",
            "description": f"Sample transaction {i}"
        })
    return txns

@mcp.tool()
def get_all_accounts(customer_id: str) -> List[Dict[str, Any]]:
    """Returns all accounts including inactive ones."""
    return MOCK_ACCOUNTS.get(customer_id, [])

if __name__ == "__main__":
    mcp.run()
