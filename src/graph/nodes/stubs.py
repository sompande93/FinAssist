from typing import Dict, Any
from ..state import BankingGraphState

def query_parser_node(state: BankingGraphState) -> Dict[str, Any]:
    """Layer 1: Parses raw query into intent and entities (Stub for Phase 2)."""
    print(f"[Query Parser] Parsing: '{state['query']}'")
    # Stub: blindly assume account query for the skeleton
    return {
        "intent": ["account_query"],
        "entities": {},
        "customer_id": "CUST_001"
    }

def router_node(state: BankingGraphState) -> Dict[str, Any]:
    """Layer 2: Routes query to appropriate agents (Stub for Phase 2)."""
    print("[Router] Determining active agents based on intents...")
    # Stub: Route everything to account_agent for now
    return {
        "active_agents": ["account_agent"]
    }

def account_agent_node(state: BankingGraphState) -> Dict[str, Any]:
    """Layer 3: Account Agent (Stub for Phase 2)."""
    print("[Account Agent] Fetching account data...")
    return {
        "agent_outputs": {
            "account_agent": {
                "agent_name": "Account Agent",
                "status": "success",
                "data": {"balance": 15000.50},
                "summary": "Customer has a balance of ₹15,000.50.",
                "confidence": 1.0,
                "warnings": []
            }
        }
    }

def loan_agent_node(state: BankingGraphState) -> Dict[str, Any]:
    print("[Loan Agent] Running...")
    return {}

def fraud_agent_node(state: BankingGraphState) -> Dict[str, Any]:
    print("[Fraud Agent] Running...")
    return {}

def compliance_agent_node(state: BankingGraphState) -> Dict[str, Any]:
    print("[Compliance Agent] Running...")
    return {}

def aggregator_node(state: BankingGraphState) -> Dict[str, Any]:
    """Layer 6: Synthesize agent outputs into final response (Stub for Phase 2)."""
    print("[Aggregator] Synthesizing final response...")
    outputs = state.get("agent_outputs", {})
    
    # Very simple string join of summaries for the stub
    summaries = [out["summary"] for out in outputs.values()]
    final_text = " ".join(summaries) if summaries else "Placeholder response."
    
    return {
        "final_response": final_text,
        "confidence": 1.0
    }
