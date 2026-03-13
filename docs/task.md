# FinCore Bank - Intelligent Banking Assistant Task List

- [x] **Phase 0: Pre-Design Decisions**
  - [x] Write Architecture Decision Record (ADR)
  - [x] Create repository structure (`src/`, `tests/`, `docs/`, `data/`)
  - [x] Set up Python environment & requirements

- [x] **Phase 1: Contracts**
  - [x] Define LangGraph State Schema (`state.py`)
  - [x] Define MCP Tool Schemas for all 4 servers
  - [x] Define Knowledge Graph Schema (`schema.py` and `queries.py` stubs)

- [ ] **Phase 2: Infrastructure**
  - [ ] Build LangGraph Skeleton
  - [x] Stand up 4 MCP Servers (core, credit, fraud, compliance)
  - [x] Implement Neo4j Client & Queries
  - [x] Seed Neo4j Knowledge Graph with Faker test data
  - [ ] Setup CI Pipeline & `pytest`

- [ ] **Phase 3: Agent Implementation**
  - [x] Implement `base_agent.py`
  - [x] Implement Account Agent
  - [/] Implement Loan Agent
  - [/] Implement Compliance Agent
  - [ ] Implement Real Router Logic (Deterministic)

- [ ] **Phase 4: Hard Problems**
  - [ ] Implement Fraud Agent and Human-in-the-Loop (HITL) Interrupt
  - [ ] Implement Parallel Agent Execution (Fan-out/Fan-in)
  - [ ] Implement Aggregator Quality & synthesis controls

- [ ] **Phase 5: Production Hardening & Submission**
  - [ ] Error Handling Audit & Injection
  - [ ] Latency Measurement & Audit Trail Verification
  - [ ] Write Documentation and API schemas
  - [ ] Prepare Demo Recording (15 min) and Deliverables
