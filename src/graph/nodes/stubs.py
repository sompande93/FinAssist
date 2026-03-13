from typing import Dict, Any, List
from ..graph.state import BankingGraphState, AgentOutput
from ..agents.account_agent import AccountAgent
from ..agents.loan_agent import LoanAgent
from ..agents.fraud_agent import FraudAgent
from ..agents.compliance_agent import ComplianceAgent

async def query_parser_node(state: BankingGraphState) -> Dict[str, Any]:
    """Parses raw text into structured intents and entities."""
    query = state.get("query", "").lower()
    
    # Deterministic mapping for Phase 3/4
    customer_id = "S2_LOAN_CUST" # Default test cust
    if "balance" in query or "account" in query:
        intent = "account_inquiry"
    elif "loan" in query or "eligible" in query:
        intent = "loan_application"
    elif "fraud" in query or "suspicious" in query:
        intent = "fraud_report"
    else:
        intent = "general_inquiry"
        
    return {
        "intents": [intent],
        "customer_id": customer_id,
        "entities": {"target_product": "PROD_001"}
    }

async def router_node(state: BankingGraphState) -> Dict[str, Any]:
    """Determines which agents should be activated."""
    intents = state.get("intents", [])
    active_agents = []
    
    if "account_inquiry" in intents:
        active_agents.append("account_agent")
    if "loan_application" in intents:
        active_agents.extend(["loan_agent", "compliance_agent"])
    if "fraud_report" in intents or state.get("customer_id") == "S3_FRAUD_CUST":
        active_agents.append("fraud_agent")
        
    return {"active_agents": active_agents}

async def account_agent_node(state: BankingGraphState) -> Dict[str, Any]:
    agent = AccountAgent("AccountAgent", state)
    output = await agent.run()
    return {"agent_outputs": {"account_agent": output}}

async def loan_agent_node(state: BankingGraphState) -> Dict[str, Any]:
    agent = LoanAgent("LoanAgent", state)
    output = await agent.run()
    return {"agent_outputs": {"loan_agent": output}}

async def fraud_agent_node(state: BankingGraphState) -> Dict[str, Any]:
    agent = FraudAgent("FraudAgent", state)
    output = await agent.run()
    return {"agent_outputs": {"fraud_agent": output}}

async def compliance_agent_node(state: BankingGraphState) -> Dict[str, Any]:
    agent = ComplianceAgent("ComplianceAgent", state)
    output = await agent.run()
    return {"agent_outputs": {"compliance_agent": output}}

async def aggregator_node(state: BankingGraphState) -> Dict[str, Any]:
    outputs = state.get("agent_outputs", {})
    if not outputs:
        return {"final_response": "I'm sorry, I couldn't process your request."}
    
    agg_text = "Here is the summary of my findings:\n\n"
    for name, out in outputs.items():
        agg_text += f"- **{name}**: {out['summary']}\n"
        
    return {"final_response": agg_text}
