import os, sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv("Neo4j-4c6a6dbb-Created-2026-09-18.txt")
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", 'neo4j')

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
driver.verify_connectivity()
print("Conectado!")

def q(query, **params):
    records, summary, keys = driver.execute_query(query, params)
    for r in records:
        print(r.data())
    c = summary.counters
    if c.contains_updates:
        print(f"nós criados: {c.nodes_created}, removidos: {c.nodes_deleted}, "
              f"relacionamentos criados: {c.relationships_created}")
    return records

q("MATCH (n) DETACH DELETE n")
q("MATCH (n) RETURN count(n) AS total")

q("CREATE (:Dog:Animal {som: 'AuAuu', comida: 'racao'})")
q("MATCH (n) RETURN labels(n), properties(n)")
q("MATCH (n) DETACH DELETE n")

driver.close()