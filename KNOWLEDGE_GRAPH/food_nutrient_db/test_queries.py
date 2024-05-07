from neo4j import GraphDatabase
NEO4J_CONNECTION_URL='neo4j+s://c492bfaa.databases.neo4j.io:7687'
NEO4J_USER='neo4j'
NEO4J_PASSWORD='qTS9vkpSZT1yZ57kseVCw2csO2Zx25IOMoYJAGoo2p0'
driver = GraphDatabase.driver(NEO4J_CONNECTION_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

previous_meals = ['Hummus']


query = """
MATCH (n:Food)
WHERE n.name IN $previous_meals
RETURN n
"""

# Assuming `driver` is your Neo4j driver instance
with driver.session() as session:
    result = session.run(query, previous_meals=previous_meals)
    for record in result:
        print(record)