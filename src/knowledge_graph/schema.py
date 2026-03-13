from typing import List, Optional
from pydantic import BaseModel

# Entity Node schemas
class Customer(BaseModel):
    id: str
    name: str
    pan: str
    credit_score: int
    kyc_status: str
    segment: str  # e.g., 'retail', 'msme', 'wealth'

class Account(BaseModel):
    id: str
    customer_id: str
    type: str # 'savings', 'current', 'fd'
    balance: float
    status: str # 'active', 'inactive', 'frozen'
    last_txn_date: str

class Transaction(BaseModel):
    id: str
    account_id: str
    amount: float
    timestamp: str
    payee_id: str
    channel: str # 'upi', 'neft', 'rtgs'
    risk_score: float

class Loan(BaseModel):
    id: str
    customer_id: str
    type: str # 'home', 'personal', 'car', 'msme'
    amount: float
    emi: float
    outstanding: float
    status: str # 'active', 'closed'

class Product(BaseModel):
    id: str
    name: str
    category: str
    min_balance: float
    eligibility_criteria: str

class RegulationRule(BaseModel):
    id: str
    source: str # 'RBI', 'DPDP'
    description: str
    effective_date: str

class RiskFlag(BaseModel):
    id: str
    type: str
    severity: str # 'low', 'medium', 'high', 'critical'
    flagged_date: str

# Relationship Schema definition
"""
Graph Relationship Cardinalities:
(Customer) -[HAS_ACCOUNT]-> (Account)            [1 : N]
(Customer) -[HAS_LOAN]-> (Loan)                  [1 : N]
(Account)  -[HAS_TRANSACTION]-> (Transaction)    [1 : N]
(Customer) -[HOLDS_PRODUCT]-> (Product)          [1 : N]
(Loan)     -[GOVERNED_BY]-> (RegulationRule)     [N : N]
(Transaction) -[FLAGGED_BY]-> (RiskFlag)         [1 : 1]
(Customer) -[LINKED_TO {reason}]-> (Customer)    [N : M]
"""
