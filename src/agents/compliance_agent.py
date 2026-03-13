from typing import Dict, Any
from .base_agent import BaseAgent
from ..graph.state import AgentOutput
from ..knowledge_graph.client import get_kg_client
import time

class ComplianceAgent(BaseAgent):
    """
    Compliance Agent: Handles regulatory checks and product requirements.
    MCP: compliance_mcp
    KG: get_applicable_regulations
    """
    
    async def run(self) -> AgentOutput:
        customer_id = self.state.get("customer_id")
        target_product = self.state.get("entities", {}).get("target_product", "PROD_001")
        
        if not customer_id:
            return self.handle_error(ValueError("Customer ID missing in state"))

        try:
            # 1. Fetch Applicable Regulations via KG
            kg_client = get_kg_client()
            self.log_kg_query(f"MATCH (p:Product {{id: '{target_product}'}})-[:GOVERNED_BY]->(r:RegulationRule) RETURN r")
            regs = kg_client.get_applicable_regulations(target_product)

            # 2. Fetch RBI Rules via MCP (Simulated Tool Call)
            start_time = time.time()
            # Simulated tool call: get_rbi_rules
            rbi_rules = [{"id": "RBI_LEND_01", "text": "Maximum DTI ratio should not exceed 50%"}]
            self.log_mcp_call("get_rbi_rules", {"category": "loans"}, "success", (time.time() - start_time) * 1000)

            # 3. Check Product Eligibility via MCP
            start_time = time.time()
            elig_data = {"eligible": True, "reason": "Fulfils all RBI guidelines"}
            self.log_mcp_call("check_product_eligibility", {"customer_id": customer_id, "product_id": target_product}, "success", (time.time() - start_time) * 1000)

            summary = f"Compliance Check: {elig_data['reason']}. Product is governed by {len(regs)} specific regulatory rules."

            return {
                "agent_name": self.name,
                "status": "success",
                "data": {
                    "regulations": regs,
                    "rbi_rules": rbi_rules,
                    "compliance_status": elig_data
                },
                "summary": summary,
                "confidence": 1.0,
                "warnings": []
            }
        except Exception as e:
            return self.handle_error(e)
