# FinCore MCP Tool Schemas (Contract 2)

## 1. core_banking_mcp
Used by the Account Agent to read current balances and ledgers.

### `get_account_summary`
- **Input:** `{ "customer_id": "str" }`
- **Output:** `List[Account]` (List of accounts containing balance, type, status, last_txn_date)
- **Errors:** `customer_not_found`, `auth_error`

### `get_transactions`
- **Input:** `{ "account_id": "str", "limit": "int" }`
- **Output:** `List[Transaction]` (Sorted by date DESC)
- **Errors:** `account_not_found`, `auth_error`

### `get_all_accounts`
- **Input:** `{ "customer_id": "str" }`
- **Output:** `List[Account]` (Includes inactive accounts)
- **Errors:** `customer_not_found`

---

## 2. credit_mcp
Used by the Loan Agent to handle lending qualification checks.

### `get_credit_profile`
- **Input:** `{ "customer_id": "str" }`
- **Output:** `CreditProfile` (Score, history months, default count)
- **Errors:** `customer_not_found`, `bureau_error`

### `get_emi_schedule`
- **Input:** `{ "customer_id": "str" }`
- **Output:** `List[EMI]` (Active EMIs with amounts and due dates)
- **Errors:** `customer_not_found`

### `check_loan_eligibility`
- **Input:** `{ "customer_id": "str", "amount": "float", "type": "str" }`
- **Output:** `EligibilityResult` (eligible: bool, reason, max_amount, interest_rate)
- **Errors:** `customer_not_found`

---

## 3. fraud_mcp
Used by the Fraud Agent to detect risks.

### `score_transaction_risk`
- **Input:** `{ "txn_id": "str", "amount": "float", "payee_id": "str" }`
- **Output:** `RiskScore` (score: 0.0-1.0, flag_list)
- **Errors:** `txn_not_found`, `payee_unknown`

### `get_customer_alerts`
- **Input:** `{ "customer_id": "str" }`
- **Output:** `List[Alert]` (Active fraud alerts with severity)
- **Errors:** `customer_not_found`

### `flag_transaction`
- **Input:** `{ "txn_id": "str", "reason": "str" }`
- **Output:** `FlagResult` (case_id, escalation_flag)
- **Errors:** `txn_not_found`

---

## 4. compliance_mcp
Used by the Compliance Agent to navigate Indian banking logic.

### `get_rbi_rules`
- **Input:** `{ "category": "str" }`
- **Output:** `List[Rule]` (Regulation text with effective dates)
- **Errors:** `category_not_found`

### `get_loan_requirements`
- **Input:** `{ "loan_type": "str" }`
- **Output:** `List[Requirement]`
- **Errors:** `loan_type_not_found`

### `check_product_eligibility`
- **Input:** `{ "customer_id": "str", "product_id": "str" }`
- **Output:** `Result` (eligibility: bool, reasoning)
- **Errors:** `customer_not_found`, `product_not_found`
