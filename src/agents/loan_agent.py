from typing import Dict, Any
from .base_agent import BaseAgent
from ..graph.state import AgentOutput
from ..knowledge_graph.client import get_kg_client
import time

class LoanAgent(BaseAgent):
    """
    Loan Agent: Handles loan eligibility and EMI burden analysis.
    MCP: credit_mcp
    KG: get_loan_emi_burden
    """
    
    async def run(self) -> AgentOutput:
        customer_id = self.state.get("customer_id")
        if not customer_id:
            return self.handle_error(ValueError("Customer ID missing in state"))

        try:
            # 1. Fetch Total EMI Burden via KG
            kg_client = get_kg_client()
            self.log_kg_query(f"MATCH (c:Customer {{id: '{customer_id}'}})-[:HAS_LOAN]->(l:Loan {{status: 'active'}}) RETURN sum(l.emi) AS total_burden")
            total_burden = kg_client.get_loan_emi_burden(customer_id)

            # 2. Fetch Credit Profile via MCP (Simulated Tool Call)
            start_time = time.time()
            # Simulated tool call: get_credit_profile
            credit_data = {"score": 750, "history_months": 36, "defaults": 0}
            self.log_mcp_call("get_credit_profile", {"customer_id": customer_id}, "success", (time.time() - start_time) * 1000)

            # 3. Check Eligibility (Simulated Tool Call)
            start_time = time.time()
            elig_data = {"eligible": True, "max_amount": 5000000, "interest_rate": 8.5}
            self.log_mcp_call("check_loan_eligibility", {"customer_id": customer_id, "amount": 1000000}, "success", (time.time() - start_time) * 1000)

            summary = f"Loan eligibility: {elig_data['eligible']}. Max eligible amount: ₹{elig_data['max_amount']:,}. "
            summary += f"Your current monthly EMI burden is ₹{total_burden:,}."

            return {
                "agent_name": self.name,
                "status": "success",
                "data": {
                    "credit_profile": credit_data,
                    "eligibility": elig_data,
                    "total_emi_burden": total_burden
                },
                "summary": summary,
                "confidence": 0.95,
                "warnings": []
            }
        except Exception as e:
            return self.handle_error(e)
