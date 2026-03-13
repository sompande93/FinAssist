from langgraph.graph import StateGraph, END
from typing import Literal

from .state import BankingGraphState, validate_state
from .nodes.stubs import (
    query_parser_node,
    router_node,
    account_agent_node,
    loan_agent_node,
    fraud_agent_node,
    compliance_agent_node,
    aggregator_node
)

def route_agents(state: BankingGraphState) -> list[str]:
    """Returns the list of agent edges to take based on active_agents in state."""
    # This maps string names in 'active_agents' to the graph node names
    return state.get("active_agents", [])

def build_graph() -> StateGraph:
    """Constructs the core 7-layer LangGraph StateGraph."""
    
    # 1. Initialize StateGraph
    workflow = StateGraph(BankingGraphState)

    # 2. Add all Nodes
    workflow.add_node("query_parser", query_parser_node)
    workflow.add_node("router", router_node)
    
    # L3 Agents
    workflow.add_node("account_agent", account_agent_node)
    workflow.add_node("loan_agent", loan_agent_node)
    workflow.add_node("fraud_agent", fraud_agent_node)
    workflow.add_node("compliance_agent", compliance_agent_node)
    
    workflow.add_node("aggregator", aggregator_node)

    # 3. Define the main flow
    workflow.set_entry_point("query_parser")
    workflow.add_edge("query_parser", "router")

    # The router acts as a conditional distribution node, fanning out based on state
    workflow.add_conditional_edges(
        "router",
        route_agents,
        {
            "account_agent": "account_agent",
            "loan_agent": "loan_agent",
            "fraud_agent": "fraud_agent",
            "compliance_agent": "compliance_agent"
        }
    )

    # Fan-in: all agents converge at the aggregator
    workflow.add_edge("account_agent", "aggregator")
    workflow.add_edge("loan_agent", "aggregator")
    workflow.add_edge("fraud_agent", "aggregator")
    workflow.add_edge("compliance_agent", "aggregator")

    # End
    workflow.add_edge("aggregator", END)

    return workflow
