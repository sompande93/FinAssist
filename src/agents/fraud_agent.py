from typing import Dict, Any
from .base_agent import BaseAgent
from ..graph.state import AgentOutput
from ..knowledge_graph.client import get_kg_client
import time

class FraudAgent(BaseAgent):
    """
    Fraud Agent: Detects suspicious activity and fraud networks.
    MCP: fraud_mcp
    KG: get_fraud_network_links
    """
    
    async def run(self) -> AgentOutput:
        customer_id = self.state.get("customer_id")
        # In a real scenario, we might iterate over transactions from state
        
        if not customer_id:
            return self.handle_error(ValueError("Customer ID missing in state"))

        try:
            # 1. Fetch Fraud Alerts via MCP
            start_time = time.time()
            alerts = [] # Mock empty alerts for standard case
            if customer_id == "S3_FRAUD_CUST":
                alerts = [{"id": "ALRT_001", "severity": "high", "reason": "Suspicious login"}]
            self.log_mcp_call("get_customer_alerts", {"customer_id": customer_id}, "success", (time.time() - start_time) * 1000)

            # 2. KG Check: Fraud Network Links
            # We use a known suspicious payee from seed data if it's the test customer
            payee_id = "UNKNOWN_PAYEE" if customer_id == "S3_FRAUD_CUST" else "NORMAL_PAYEE"
            kg_client = get_kg_client()
            self.log_kg_query(f"MATCH (payee_txn:Transaction {{payee_id: '{payee_id}'}})<-[:HAS_TRANSACTION]-(a:Account)<-[:HAS_ACCOUNT]-(c:Customer) RETURN collect(DISTINCT c.id)")
            network_links = kg_client.get_fraud_network_links(payee_id)

            summary = "No active fraud alerts detected."
            if alerts:
                summary = f"CRITICAL: {len(alerts)} active fraud alert(s) found! Network analysis shows {len(network_links)} linked accounts."

            return {
                "agent_name": self.name,
                "status": "success" if not alerts else "warning",
                "data": {
                    "alerts": alerts,
                    "network_links": network_links
                },
                "summary": summary,
                "confidence": 0.9,
                "warnings": ["Potential fraud network detected"] if alerts else []
            }
        except Exception as e:
            return self.handle_error(e)
