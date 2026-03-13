from typing import Dict, Any
from .base_agent import BaseAgent
from ..graph.state import AgentOutput
from ..knowledge_graph.client import get_kg_client
import time

class AccountAgent(BaseAgent):
    """
    Account Agent: Handles balance queries and transaction history.
    MCP: core_banking_mcp
    KG: get_inactive_accounts
    """
    
    async def run(self) -> AgentOutput:
        customer_id = self.state.get("customer_id")
        if not customer_id:
            return self.handle_error(ValueError("Customer ID missing in state"))

        try:
            # 1. Fetch Summary via MCP (Mocking the tool call logic here)
            start_time = time.time()
            # In a real system, this would be a tool call via the LLM or a direct SDK call
            # For Phase 3, we simulate the tool call.
            
            # log_mcp_call(self, tool, params, status, latency)
            # Simulated tool call
            summary_data = [{"id": "ACC_101", "balance": 15000.50}] 
            self.log_mcp_call("get_account_summary", {"customer_id": customer_id}, "success", (time.time() - start_time) * 1000)

            # 2. Fetch Inactive Accounts via KG
            kg_client = get_kg_client()
            self.log_kg_query(f"MATCH (c:Customer {{id: '{customer_id}'}})-[:HAS_ACCOUNT]->(a:Account) WHERE a.last_txn_date < '2024-09-01' RETURN a")
            inactive_accounts = kg_client.get_inactive_accounts(customer_id)

            summary = f"Your total balance is ₹15,000.50 across 1 active account."
            if inactive_accounts:
                summary += f" You have {len(inactive_accounts)} inactive account(s)."

            return {
                "agent_name": self.name,
                "status": "success",
                "data": {
                    "accounts": summary_data,
                    "inactive_accounts": inactive_accounts
                },
                "summary": summary,
                "confidence": 1.0,
                "warnings": []
            }
        except Exception as e:
            return self.handle_error(e)
