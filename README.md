# FinCore Intelligent Banking Assistant
## Intelligent Multi-Agent Banking System

This repository contains the implementation of the **FinCore Intelligent Banking Assistant**, a stateful multi-agent AI pipeline designed to handle complex banking queries across domain boundaries (Loan, Fraud, Account, and Compliance).

### 🏗 Architecture Overview
The system follows a **7-Layer Architecture** powered by **LangGraph**:
1.  **L1: Query Parser** - Intent and entity extraction.
2.  **L2: Router Node** - Deterministic routing logic.
3.  **L3: Specialist Agents** - Domain-specific reasoning (Account, Loan, Fraud, Compliance).
4.  **L4: MCP Tool Calls** - Clean data fetching through Model Context Protocol servers.
5.  **L5: Knowledge Graph** - Multi-hop relationship reasoning via **Neo4j**.
6.  **L6: Aggregator Node** - Grounded synthesis of multi-agent responses.
7.  **L7: State Checkpointer** - Conversation persistence and session memory.

### 📊 Current Progress
- [x] **Phase 0: Pre-Design** - ADR drafted, architecture diagrams finalized, scaffold created.
- [x] **Phase 1: Contracts** - State schema, MCP tool definitions, and KG schema locked.
- [x] **Phase 2: Infrastructure**
    - [x] **LangGraph Skeleton**: Multi-node pipeline ready.
    - [x] **MCP Servers**: Core Banking, Credit, Fraud, and Compliance mock servers implemented with FastMCP.
    - [x] **Knowledge Graph**: Neo4j Aura integration complete. Seeding script implemented with 700+ nodes (50 customers, 120 accounts, 40 loans).
    - [x] **Verification**: Traversal queries (S2, S3, S8 scenarios) verified against Aura.
- [/] **Phase 3: Agent Implementation**
    - [x] **Account Agent**: Fully implemented with MCP and KG connectivity.
    - [ ] **Loan/Fraud/Compliance Agents**: In development.

### 📂 Repository Structure
```text
src/
  graph/           ← LangGraph state.py, graph.py, and node stubs
  agents/          ← base_agent.py and domain specialist agents
  mcp_servers/     ← 4 typed FastMCP servers (Core, Credit, Fraud, Compliance)
  knowledge_graph/ ← schema.py, queries.py, and seed.py (for Neo4j Aura)
  prompts/         ← Domain-specific prompt templates
docs/              ← Architecture diagrams, API schemas, and implementation plan
tests/             ← Initial test scenarios (S1-S8)
```

### 🚀 Setup and Run
1.  **Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Configure `.env`**:
    Update the `NEO4J_*` variables in `.env` with your Aura credentials.
3.  **Seed Database** (Optional):
    ```bash
    python3 src/knowledge_graph/seed.py
    ```
4.  **Run Pipeline**:
    ```bash
    python3 main.py "What is my account balance?"
    ```

### 📋 Documentation & Brain Artifacts
Full implementation details and task checklists are available in:
- [Implementation Plan](docs/implementation_plan.md)
- [Architecture Diagram](docs/architecture_diagram.md)
- [Task Checklist](docs/task.md)
