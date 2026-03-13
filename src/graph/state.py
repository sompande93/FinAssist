from typing import TypedDict, List, Dict, Optional, Any, Literal
import operator
from typing_extensions import Annotated
from pydantic import BaseModel, Field

# valid intent types as an enum
IntentType = Literal[
    'account_query', 
    'loan_eligibility', 
    'fraud_report', 
    'compliance_query', 
    'product_upgrade', 
    'account_comparison'
]

class AgentOutput(TypedDict):
    agent_name: str
    status: Literal['success', 'error', 'partial']
    data: Dict[str, Any]
    summary: str
    confidence: float
    warnings: List[str]

class MCPCallRecord(TypedDict):
    tool: str
    params: Dict[str, Any]
    latency_ms: float
    timestamp: str
    status: Literal['success', 'error']
    error: Optional[str]

# The main Checkpointer State object
class BankingGraphState(TypedDict):
    query: str
    customer_id: Optional[str]
    session_id: str
    intent: List[IntentType]
    entities: Dict[str, Any]
    active_agents: List[str]
    risk_level: Literal['low', 'medium', 'high']
    requires_human: bool
    human_decision: Optional[Literal['approve', 'block', 'monitor']]
    
    # State Merge Strategy: Allow dict updates for agent keys rather than overwrite
    agent_outputs: Annotated[Dict[str, AgentOutput], operator.ior]
    
    # Append-only logs
    mcp_calls_log: Annotated[List[MCPCallRecord], operator.add]
    kg_queries_log: Annotated[List[str], operator.add]
    errors: Annotated[List[str], operator.add]
    
    final_response: str
    confidence: float

def make_initial_state(query: str, session_id: str) -> BankingGraphState:
    """Factory function to prevent shared mutable default states."""
    return {
        "query": query,
        "customer_id": None,
        "session_id": session_id,
        "intent": [],
        "entities": {},
        "active_agents": [],
        "risk_level": "low",
        "requires_human": False,
        "human_decision": None,
        "agent_outputs": {},
        "mcp_calls_log": [],
        "kg_queries_log": [],
        "errors": [],
        "final_response": "",
        "confidence": 0.0
    }

def validate_state(state: BankingGraphState):
    """Called at start of every node to enforce state sanity"""
    if "query" not in state or not state["query"]:
        raise ValueError("State missing query parameter.")
    if "session_id" not in state or not state["session_id"]:
        raise ValueError("State missing session_id parameter.")
