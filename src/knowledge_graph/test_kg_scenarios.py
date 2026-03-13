import asyncio
from src.knowledge_graph.client import get_kg_client

async def test_scenarios_data():
    client = get_kg_client()
    print("\n--- Testing Knowledge Graph Test Scenarios ---")
    
    # S2: Loan EMI Burden
    burden = client.get_loan_emi_burden("S2_LOAN_CUST")
    print(f"S2: Loan EMI Burden for S2_LOAN_CUST: {burden} (Expected: 40000)")
    
    # S8: Inactive Accounts
    inactive = client.get_inactive_accounts("S8_INACTIVE_CUST")
    print(f"S8: Inactive Accounts for S8_INACTIVE_CUST: {len(inactive)} (Expected: 1)")
    
    # S3: Fraud Network
    # TXN_S3_HIGH_RISK has payee 'UNKNOWN_PAYEE'
    fraud_links = client.get_fraud_network_links("UNKNOWN_PAYEE")
    print(f"S3: Fraud Network links for 'UNKNOWN_PAYEE': {fraud_links} (Expected at least S3_FRAUD_CUST)")

if __name__ == "__main__":
    asyncio.run(test_scenarios_data())
