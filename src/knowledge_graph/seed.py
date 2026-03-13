import os
import random
import uuid
from faker import Faker
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

fake = Faker('en_IN')
SEED = 42
fake.seed_instance(SEED)
random.seed(SEED)

NUM_CUSTOMERS = 50
NUM_ACCOUNTS = 120
NUM_LOANS = 40
NUM_PRODUCTS = 15
NUM_RULES = 8

def clear_db(session):
    session.run("MATCH (n) DETACH DELETE n")

def seed_data(session):
    print("Clearing database...")
    clear_db(session)
    
    print("Seeding Knowledge Graph with Neo4j...")
    
    # --- Customers ---
    customers = []
    test_customers = [
        {"id": "S2_LOAN_CUST", "name": "Test Customer for Loan EMI Burden", "credit_score": 750},
        {"id": "S3_FRAUD_CUST", "name": "Test Customer for Fraud Ring", "credit_score": 600},
        {"id": "S5_UPGRADE_CUST", "name": "Test Customer for Product Upgrade", "credit_score": 800},
        {"id": "S8_INACTIVE_CUST", "name": "Test Customer for Inactive Accounts", "credit_score": 700}
    ]
    
    for tc in test_customers:
        session.run("""
            CREATE (c:Customer {id: $id, name: $name, pan: $pan, credit_score: $score, kyc_status: 'verified', segment: 'retail'})
        """, id=tc["id"], name=tc["name"], pan=fake.bothify(text='?????####?').upper(), score=tc["credit_score"])
        customers.append(tc["id"])

    for i in range(NUM_CUSTOMERS - len(test_customers)):
        c_id = f"CUST_{i:03d}"
        session.run("""
            CREATE (c:Customer {id: $id, name: $name, pan: $pan, credit_score: $score, kyc_status: $kyc, segment: $segment})
        """, id=c_id, name=fake.name(), pan=fake.bothify(text='?????####?').upper(), 
            score=random.randint(500, 850), kyc=random.choice(['verified', 'pending']), 
            segment=random.choice(['retail', 'msme']))
        customers.append(c_id)

    # --- Accounts ---
    accounts = []
    # S8 Inactive
    session.run("""
        MATCH (c:Customer {id: 'S8_INACTIVE_CUST'})
        CREATE (c)-[:HAS_ACCOUNT]->(a:Account {id: 'ACC_INACTIVE_001', type: 'savings', balance: 5000.0, status: 'inactive', last_txn_date: '2024-01-10'})
    """)
    accounts.append('ACC_INACTIVE_001')

    for i in range(NUM_ACCOUNTS - 1):
        a_id = f"ACC_{i:03d}"
        owner_id = random.choice(customers)
        status = random.choices(['active', 'inactive'], weights=[0.8, 0.2])[0]
        last_txn = fake.date_between(start_date='-1y', end_date='today').isoformat()
        session.run("""
            MATCH (c:Customer {id: $owner_id})
            CREATE (c)-[:HAS_ACCOUNT]->(a:Account {id: $id, type: $type, balance: $balance, status: $status, last_txn_date: $last_txn})
        """, owner_id=owner_id, id=a_id, type=random.choice(['savings', 'current']), 
            balance=round(random.uniform(100, 100000), 2), status=status, last_txn=last_txn)
        accounts.append(a_id)

    # --- Loans ---
    # S2 Burden
    session.run("""
        MATCH (c:Customer {id: 'S2_LOAN_CUST'})
        CREATE (c)-[:HAS_LOAN]->(:Loan {id: 'LN_S2_1', type: 'car', amount: 1000000, emi: 25000, outstanding: 800000, status: 'active'})
        CREATE (c)-[:HAS_LOAN]->(:Loan {id: 'LN_S2_2', type: 'personal', amount: 500000, emi: 15000, outstanding: 400000, status: 'active'})
    """)

    for i in range(NUM_LOANS - 2):
        l_id = f"LN_{i:03d}"
        owner_id = random.choice(customers)
        amt = round(random.uniform(50000, 2000000), 2)
        session.run("""
            MATCH (c:Customer {id: $owner_id})
            CREATE (c)-[:HAS_LOAN]->(:Loan {id: $id, type: $type, amount: $amount, emi: $emi, outstanding: $outstanding, status: $status})
        """, owner_id=owner_id, id=l_id, type=random.choice(['home', 'personal']), amount=amt, 
            emi=round(amt * 0.015, 2), outstanding=round(amt * 0.8, 2), status='active')

    # --- Rules ---
    rules = []
    for i in range(NUM_RULES):
        r_id = f"REG_{i:03d}"
        session.run("""
            CREATE (r:RegulationRule {id: $id, source: $source, description: $desc, effective_date: '2024-01-01'})
        """, id=r_id, source=random.choice(['RBI', 'DPDP']), desc=f"Rule {i}")
        rules.append(r_id)

    # --- Products ---
    for i in range(NUM_PRODUCTS):
        p_id = f"PROD_{i:03d}"
        session.run("""
            CREATE (p:Product {id: $id, name: $name, category: $cat, min_balance: $min, eligibility_criteria: 'Standard'})
        """, id=p_id, name=f"Product {i}", cat="savings", min=random.choice([0, 5000]))
        # governed_by
        session.run("""
            MATCH (p:Product {id: $p_id}), (r:RegulationRule {id: $r_id})
            CREATE (p)-[:GOVERNED_BY]->(r)
        """, p_id=p_id, r_id=random.choice(rules))

    # Link upgrade
    session.run("MATCH (c:Customer {id: 'S5_UPGRADE_CUST'}), (p:Product {id: 'PROD_001'}) CREATE (c)-[:HOLDS_PRODUCT]->(p)")

    # --- Transactions & Fraud ring ---
    # S3 Fraud
    session.run("""
        MATCH (c:Customer {id: 'S3_FRAUD_CUST'})
        CREATE (c)-[:HAS_ACCOUNT]->(a:Account {id: 'ACC_FRAUD_001', type: 'savings', balance: 1000.0, status: 'active'})
        CREATE (a)-[:HAS_TRANSACTION]->(t:Transaction {id: 'S3_TXN', amount: 45000, timestamp: '2024-03-12T10:00:00', payee_id: 'UNKNOWN_PAYEE', risk_score: 0.85})
        CREATE (t)-[:FLAGGED_BY]->(:RiskFlag {id: 'FLAG_S3', type: 'suspicious', severity: 'high'})
    """)
    
    # Fraud ring links
    for other in random.sample(customers, 3):
        if other != 'S3_FRAUD_CUST':
            session.run("""
                MATCH (c1:Customer {id: 'S3_FRAUD_CUST'}), (c2:Customer {id: $other})
                CREATE (c1)-[:LINKED_TO {reason: 'shared_device'}]->(c2)
            """, other=other)

    print("Seeding complete.")

if __name__ == "__main__":
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session(database=database) as session:
            seed_data(session)
        driver.close()
    except Exception as e:
        print(f"Failed to seed Neo4j: {e}")

