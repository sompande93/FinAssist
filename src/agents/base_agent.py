import abc
from typing import Any, Dict, List, Optional
from datetime import datetime
from ..graph.state import BankingGraphState, AgentOutput, MCPCallRecord

class BaseAgent(abc.ABC):
    """
    Abstract base class for all FinCore agents.
    Ensures consistent logging of MCP calls and KG queries into the shared state.
    """
    
    def __init__(self, name: str, state: BankingGraphState):
        self.name = name
        self.state = state

    @abc.abstractmethod
    async def run(self) -> AgentOutput:
        """Core logic of the agent."""
        pass

    def log_mcp_call(self, tool: str, params: Dict[str, Any], status: str, latency: float, error: Optional[str] = None):
        """Append-only logging for MCP tool calls."""
        record: MCPCallRecord = {
            "tool": tool,
            "params": params,
            "latency_ms": latency,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "error": error
        }
        # In actual implementation, this will be handled by the LangGraph state update
        # but the agent can prepare the record.
        self.state["mcp_calls_log"].append(record)

    def log_kg_query(self, query: str):
        """Append-only logging for KG queries."""
        self.state["kg_queries_log"].append(query)

    def handle_error(self, error: Exception) -> AgentOutput:
        """Ensures the agent returns gracefully instead of crashing the graph."""
        error_msg = f"Error in {self.name}: {str(error)}"
        self.state["errors"].append(error_msg)
        return {
            "agent_name": self.name,
            "status": "error",
            "data": {},
            "summary": "Internal processing error occurred.",
            "confidence": 0.0,
            "warnings": [error_msg]
        }
