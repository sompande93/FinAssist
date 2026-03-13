from typing import List, Dict, Any
from neo4j import GraphDatabase

class KnowledgeGraphClient:
    """Neo4j Graph client implementation for traversing banking entity relationships using Cypher."""
    
    def __init__(self, driver):
        self.driver = driver

    def get_loan_emi_burden(self, customer_id: str) -> float:
        """Calculates the sum of all active loan EMIs for a customer."""
        query = """
        MATCH (c:Customer {id: $customer_id})-[:HAS_LOAN]->(l:Loan {status: 'active'})
        RETURN sum(l.emi) AS total_burden
        """
        with self.driver.session() as session:
            result = session.run(query, customer_id=customer_id)
            record = result.single()
            return record["total_burden"] if record and record["total_burden"] else 0.0

    def get_applicable_regulations(self, product_id: str) -> List[Dict[str, Any]]:
        """Returns all RBI / DPDP rules governing a specific product type."""
        query = """
        MATCH (p:Product {id: $product_id})-[:GOVERNED_BY]->(r:RegulationRule)
        RETURN r
        """
        with self.driver.session() as session:
            result = session.run(query, product_id=product_id)
            return [dict(record["r"]) for record in result]

    def get_inactive_accounts(self, customer_id: str, months_threshold: int = 6) -> List[Dict[str, Any]]:
        """Finds Account nodes owned by customer where last_txn_date is older than N months."""
        # Simple string comparison for mock logic
        # In real world, we'd use duration or date comparisons
        query = """
        MATCH (c:Customer {id: $customer_id})-[:HAS_ACCOUNT]->(a:Account)
        WHERE a.last_txn_date < '2024-09-01'
        RETURN a
        """
        with self.driver.session() as session:
            result = session.run(query, customer_id=customer_id)
            return [dict(record["a"]) for record in result]

    def get_fraud_network_links(self, payee_id: str) -> List[str]:
        """Fraud ring detection: returns list of customer IDs linked to identical payee."""
        query = """
        MATCH (payee_txn:Transaction {payee_id: $payee_id})<-[:HAS_TRANSACTION]-(a:Account)<-[:HAS_ACCOUNT]-(c:Customer)
        RETURN collect(DISTINCT c.id) AS linked_customers
        """
        with self.driver.session() as session:
            result = session.run(query, payee_id=payee_id)
            record = result.single()
            return record["linked_customers"] if record else []

    def get_product_eligibility_path(self, customer_id: str, product_id: str) -> Dict[str, Any]:
        """Checks target product conditions vs currently held products."""
        query = """
        MATCH (c:Customer {id: $customer_id}), (p:Product {id: $product_id})
        RETURN p.eligibility_criteria AS conditions
        """
        with self.driver.session() as session:
            result = session.run(query, customer_id=customer_id, product_id=product_id)
            record = result.single()
            return {
                "eligible": True,
                "conditions": record["conditions"] if record else ""
            }
