from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
import dotenv
import json
dotenv.load_dotenv()


NEO4J_CONNECTION_URL='neo4j+s://c492bfaa.databases.neo4j.io:7687'
NEO4J_USER='neo4j'
NEO4J_PASSWORD='qTS9vkpSZT1yZ57kseVCw2csO2Zx25IOMoYJAGoo2p0'


##Nutrient is per hundred grams
age = '19-70y'
gender = 'Female'
previous_meals = 'Hummus'
previous_quantities = '10g'
desired_meal = 'Firm Tofu'
desired_quantities = '20g'


# Cypher generation prompt
cypher_generation_template = """
You are an expert Neo4j Cypher translator who converts English to Cypher based on the Neo4j Schema provided, following the instructions below:
1. Generate Cypher query compatible ONLY for Neo4j Version 5
2. Do not use EXISTS, SIZE, HAVING, CONTAINS, keywords in the cypher. Use alias when using the WITH keyword
3. Use only Nodes and relationships mentioned in the schema
4. Always do a case-insensitive and fuzzy search for any properties related search. 
5. Never use relationships that are not mentioned in the given schema
6. When asked about anything, Match the properties using non-case-insensitive matching 

schema: {schema}

Examples:
Question: "I am a $age Year Old $gender with Sickle Cell Disease. I have eaten $previous_quantities of $previous_meals. I am about to eat $desired_quantity of $desired_meal, should I go ahead?".

Answer: ```
MATCH (user:User)-[user_relationship:NEEDS]->(nutrient:Nutrient)
WHERE user.age_bracket = $age AND user.gender = $gender

MATCH (eaten_food:Food)-[eaten_food_relationship:CONTAINS]->(eaten_food_nutrient:Nutrient)
WHERE eaten_food.name = $previous_meals

MATCH (eaten_food:Food)-[:CONTAINS_COMPOUND]->(eaten_food_compound:Compound)
WHERE eaten_food.name = $previous_meals
MATCH (eaten_food_compound)-[:HAS_EFFECT]->(eaten_food_health_effect:HealthEffect)

MATCH (desired_food:Food)-[desired_food_relationship:CONTAINS]->(desired_food_nutrient:Nutrient)
WHERE desired_food.name = $desired_meal

MATCH (desired_food:Food)-[:CONTAINS_COMPOUND]->(desired_food_compound:Compound)
WHERE desired_food.name = $desired_meal
MATCH (desired_food_compound)-[:HAS_EFFECT]->(desired_food_health_effect:HealthEffect)
RETURN user, nutrient, user_relationship.quantity_needed, eaten_food_relationship.quantity_per_100g, eaten_food_nutrient, desired_food_nutrient, desired_food_relationship.quantity_per_100g;
```
Question: {question}


Question: "I am a $age Year Old $gender with Sickle Cell Disease. I have eaten $previous_quantities of $previous_meals. I am about to eat $desired_quantity of $desired_meal, What compounds are found in these foods and how might it affect me?".
Answer: ```
MATCH (eaten_food:Food)-[:CONTAINS_COMPOUND]->(eaten_food_compound:Compound)
WHERE eaten_food.name = $previous_meals
MATCH (eaten_food_compound)-[:HAS_EFFECT]->(eaten_food_health_effect:HealthEffect)

MATCH (desired_food:Food)-[:CONTAINS_COMPOUND]->(desired_food_compound:Compound)
WHERE desired_food.name = $desired_meal
MATCH (desired_food_compound)-[:HAS_EFFECT]->(desired_food_health_effect:HealthEffect)
RETURN user, nutrient, user_relationship.quantity_needed, eaten_food_relationship.quantity_per_100g, eaten_food_nutrient, desired_food_nutrient, desired_food_relationship.quantity_per_100g;
```
"""


cypher_prompt = PromptTemplate(
    template=cypher_generation_template,
    input_variables=["schema", "question"]
)

CYPHER_QA_TEMPLATE = """

You are a nutrtition assistant that performs calculations using Information.
The Information is in JSON format.


The JSON contains the provided information that you must use to construct an answer, read and understand its data structure very well.
Go through the JSON, looking for anything that corresponds to User, such as property key, using that, find the gender and age.
Go through the JSON, finding all data where the key is eaten_food_nutrient, desired_food_nutrient, eaten_food_compound and desired_food_compound.
Take note of all the nutrients found in each food, using the eaten_food_nutrient and desired_food_nutrient keys.
In the JSON there is user_relationship which shows the quantity needed of different nutrients for a user of certain age and gender, this is their Recommended Daily Intake.
For every nutrient in the food, there is quantity_per_100g which shows the nutrients per 100g of that nutrient in the food.

If the user is asking about eating a meal, for all the nutrients found in each food, you must perform calculations to determine if eating a meal exceeds or falls short of a users Recommended Daily Intake of all nutrients, based on what they've already eaten.
Make sure to show all mathematical workings.

If the user is enquiring about compounds, you discuss the compounds found in the foods.

If the provided information is empty, say that you don't know the answer. If there is no information about nutrients, use the information provided about compounds.


Information:
{context}
Question: {question}
Helpful Answer:"""

qa_prompt = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)


def query_graph(user_input):
    graph = Neo4jGraph(url=NEO4J_CONNECTION_URL, username=NEO4J_USER, password=NEO4J_PASSWORD)
    graph.refresh_schema()
    chain = GraphCypherQAChain.from_llm(
        cypher_llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
        qa_llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
        graph=graph,
        verbose=True,
        #return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt,
        validate_cypher=True,
        top_k=100,
    )
    result = chain.invoke(user_input)
    
    with open('report.txt', 'w') as file:  
        json.dump(result, file)  
    return result





with open('user_profile.json', 'r') as file:
    # Load JSON data from the file
    user_profile = json.load(file)

with open('user_stomach.json', 'r') as file:
    # Load JSON data from the file
    user_stomach = json.load(file)

with open('next_meal.json', 'r') as file:
    # Load JSON data from the file
    next_meal = json.load(file)


first_key, first_value = next(iter(user_stomach.items()))
second_key, second_value = next(iter(next_meal.items()))
query_graph("I am a {}y Year Old {}. with Sickle Cell Disease. I have eaten {}g of {}. I am about to eat {}g of {}, Tell me about the compounds in these foods?".format(user_profile['age'], user_profile['sex'], first_value, first_key, second_value, second_key))


