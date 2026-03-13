# FinCore Intelligent Banking Assistant - Detailed Architecture Diagram

This diagram represents the flow of data and state transitions through the 7 layers of the system.

## Success Metrics & Constraints
- **Latency**: p90 < 4 seconds end-to-end
- **Accuracy**: Zero hallucinations, responses grounded strictly in retrieved data
- **Auditability**: 100% logging of all MCP calls (`mcp_calls_log`) and KG queries (`kg_queries_log`)
- **Compliance**: Adherence to RBI + DPDP Act guidelines

## Architecture Diagram (Mermaid)

```mermaid
stateDiagram-v2
    classDef metrics fill:#fffde7,stroke:#fbc02d,stroke-width:2px;
    classDef state fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    classDef agent fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px;
    classDef data_source fill:#fff3e0,stroke:#ff9800,stroke-width:2px;
    classDef human fill:#fce4ec,stroke:#e91e63,stroke-width:2px;

    [*] --> Raw_Query: User Input
    
    state "Layer 1: Query Parser\n- Extract intent & entities\n- Initialize Session ID\n- Extract Customer ID" as L1
    Raw_Query --> L1

    state "Layer 7: Checkpointer / Shared State Schema\n[Single Source of Truth]\n- query: str\n- intent: List[str]\n- active_agents: List[str]\n- risk_level: 'low'|'medium'|'high'\n- agent_outputs: Dict\n- mcp_calls_log: List\n- kg_queries_log: List\n- errors: List\n- final_response: str" as SharedState
    L1 --> SharedState: Write (Parsed Entities, Intent)
    
    state "Layer 2: Router Node\n(Deterministic Logic, No LLM)\n- Evaluates intent & risk_level" as Router
    SharedState --> Router: Read (Intent, Risk Level)
    Router --> SharedState: Write (active_agents list)

    state "Layer 3: Parallel Agent Execution" as L3 {
        state "Account Agent\n- Inherits base_agent.py" as AA
        state "Loan Agent\n- Inherits base_agent.py" as LA
        state "Fraud Agent\n- Inherits base_agent.py" as FA
        state "Compliance Agent\n- Inherits base_agent.py" as CA
    }

    Router --> AA: Route (if account_query)
    Router --> LA: Route (if loan_eligibility)
    Router --> FA: Route (if fraud_report or risk='high')
    Router --> CA: Route (if compliance_query)

    state "Layer 4: MCP Servers (Flat Data)" as L4 {
        state "core_banking_mcp\n(get_account_summary, get_transactions)" as CoreMCP
        state "credit_mcp\n(get_credit_profile, check_loan_eligibility)" as CreditMCP
        state "fraud_mcp\n(score_transaction_risk, flag_transaction)" as FraudMCP
        state "compliance_mcp\n(get_rbi_rules, check_product_eligibility)" as CompMCP
    }

    state "Layer 5: Knowledge Graph\n(Neo4j / NetworkX)" as L5 {
        state "Multi-Hop Reasoning\n- get_loan_emi_burden()\n- get_applicable_regulations()\n- get_fraud_network_links()" as KG_Queries
    }

    %% Agent Data Access
    AA --> CoreMCP: Typed Tool Call
    AA --> KG_Queries: Graph Traversal
    
    LA --> CreditMCP: Typed Tool Call
    LA --> KG_Queries: Graph Traversal
    
    FA --> FraudMCP: Typed Tool Call
    FA --> KG_Queries: Graph Traversal
    
    CA --> CompMCP: Typed Tool Call
    CA --> KG_Queries: Graph Traversal

    %% Logging mechanism (built into base_agent.py)
    CoreMCP --> SharedState: Write (mcp_calls_log)
    CreditMCP --> SharedState: Write (mcp_calls_log)
    FraudMCP --> SharedState: Write (mcp_calls_log)
    CompMCP --> SharedState: Write (mcp_calls_log)
    
    KG_Queries --> SharedState: Write (kg_queries_log)

    %% Human Interrupt Logic
    state "Human In The Loop (HITL)\n- Triggered if risk > 0.7\n- Wait for review\n- Graph paused" as HITL
    FA --> HITL: Risk > 0.7
    HITL --> SharedState: Write (human_decision: 'approve'/'block')
    
    %% Output Writing
    AA --> SharedState: Write (agent_outputs['account'])
    LA --> SharedState: Write (agent_outputs['loan'])
    FA --> SharedState: Write (agent_outputs['fraud'])
    CA --> SharedState: Write (agent_outputs['compliance'])

    state "Layer 6: Aggregator Node\n- Reads all agent_outputs\n- Resolves conflicts\n- Cites sources\n- Strict zero-hallucination" as Aggregator
    SharedState --> Aggregator: Read (All agent_outputs)
    
    Aggregator --> SharedState: Write (final_response, confidence)

    SharedState --> [*]: Return final_response to User

    %% Styling Application
    class SharedState state
    class L1,Router,Aggregator agent
    class AA,LA,FA,CA agent
    class CoreMCP,CreditMCP,FraudMCP,CompMCP data_source
    class KG_Queries data_source
    class HITL human
```
