import json
import os
from neo4j import GraphDatabase

# Define Neo4j connection parameters
neo4j_url = 'neo4j+s://c492bfaa.databases.neo4j.io:7687'
neo4j_user = 'neo4j'
neo4j_password = 'qTS9vkpSZT1yZ57kseVCw2csO2Zx25IOMoYJAGoo2p0'

driver = GraphDatabase.driver(neo4j_url, auth=(neo4j_user, neo4j_password))

current_directory = os.getcwd()
with open(os.path.join(current_directory, 'recommended_daily_allowance.json'), "r") as nutrient_file:
    rdi_data = json.load(nutrient_file)

with open(os.path.join(current_directory, 'foods.json'), "r") as food_file:
    food_data = json.load(food_file)

with open(os.path.join(current_directory, 'compounds.json'), 'r') as file:
    compounds_data = json.load(file)

with open(os.path.join(current_directory, 'health_effects.json'), 'r') as file:
    health_effects_data = json.load(file)

with open(os.path.join(current_directory, 'compound_health_effects.json'), 'r') as file:
    compound_health_effects_data = json.load(file)


# List of known nutrients
known_nutrients = [
    "protein", "fat", "saturated-fat", "zinc", "calcium", "manganese" "carbohydrate", "sugars", "dietary-fibre",
    "sodium", "potassium", "calcium", "magnesium", "phosphorus", 
    "iron", "zinc", "copper", "manganese", "selenium", "iodine",
    "vitaminA", "vitaminC", "vitaminD", "vitaminE", "vitaminK",
    "thiamine", "riboflavin", "niacin", "vitaminB6", "folate", "vitaminB12",
    "biotin", "pantothenic-acid", "choline",
    "glutamine", "arginine", "energy"
]


# for item in compound_health_effects_data:
#     compound_id = item['compound_id']
#     health_effect_id = item['health_effect_id']
#     compound_name = next((c['name'] for c in compounds_data if c['id'] == compound_id), "Compound name not available")
#     health_effect_description = next((h['description'] for h in health_effects_data if h['id'] == health_effect_id), "Description not available")
#     print(f"Compound ID: {compound_id}, Compound Name: {compound_name}, Health Effect ID: {health_effect_id}, Health Effect Description: {health_effect_description}")


#Generate and run Cypher queries for food items
with driver.session() as session:
    
    # ##Creating compound entity
    # for compound in compounds_data:
    #     compound_id = compound['id']
    #     compound_name = compound['name']
        
    #     # Cypher query to create a compound node with id and name attributes
    #     query = (
    #         "MERGE (c:Compound {id: $compound_id, name: $compound_name})"
    #     )
    #     session.run(query, compound_id=compound_id, compound_name=compound_name)


    ##Creating health effect entity
    # for health_effect in health_effects_data:
    #     session.run(
    #         """
    #         MERGE (h:HealthEffect {id: $id})
    #         ON CREATE SET h.description = $description
    #         ON MATCH SET h.description = $description
    #         """,
    #         id=health_effect['id'],
    #         description=health_effect['description']
    #     )


    # # Create relationships between compounds and health effects
    # for item in compound_health_effects_data:
    #     session.run(
    #         """
    #         MATCH (c:Compound {id: $compound_id})
    #         MATCH (h:HealthEffect {id: $health_effect_id})
    #         MERGE (c)-[:HAS_EFFECT]->(h)
    #         """,
    #         compound_id=item['compound_id'],
    #         health_effect_id=item['health_effect_id']
    #     )


    # Generate Cypher queries for user and nutrient relationships
    # for nutrient, nutrient_data in rdi_data["DietaryReferenceIntakes"]["NutrientsSuggestedForNutritionManagementOfSCD"].items():
    #     for gender, age_data in nutrient_data.items():
    #         for age_bracket, quantity in age_data.items():
    #             user_query = f'MERGE (u:User {{gender: "{gender}", age_bracket: "{age_bracket}"}})'
    #             nutrient_query = f'MERGE (n:Nutrient {{name: "{nutrient}"}})'
    #             relationship_query = f'MERGE (u)-[:NEEDS {{quantity_needed: {quantity}}}]->(n)'
    #             query = user_query + '\n' + nutrient_query + '\n' + relationship_query
    #             # Execute Cypher query
    #             session.run(query)


    for food_item in food_data:
        food_name = food_item.get("name", "")
        nutrition_per_100g = food_item.get("nutrition-per-100g", {})
        compounds = food_item.get("compounds", [])

        for compound in compounds:
            query = (
                f'MATCH (f:Food {{name: "{food_name}"}}) '
                f'MATCH (c:Compound {{name: "{compound}"}}) '
                'MERGE (f)-[:CONTAINS_COMPOUND]->(c)'
            )
            # Run the query
            session.run(query)

        if nutrition_per_100g:
            for key, value in nutrition_per_100g.items():
                if key.lower() in known_nutrients:
                    # Create Cypher query to create food node and merge with existing nutrient node
                    query = (
                        f'MERGE (f:Food {{name: "{food_name}"}}) '
                        f'MERGE (n:Nutrient {{name: "{key.lower()}"}}) '
                        f'MERGE (f)-[:CONTAINS {{quantity_per_100g: {value}}}]->(n)'
                    )
                    # Run the query
                    session.run(query)
                    
print("done")
driver.close()
