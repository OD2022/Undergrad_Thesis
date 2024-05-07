from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
import dotenv
dotenv.load_dotenv()


NEO4J_CONNECTION_URL='neo4j+s://c492bfaa.databases.neo4j.io:7687'
NEO4J_USER='neo4j'
NEO4J_PASSWORD='qTS9vkpSZT1yZ57kseVCw2csO2Zx25IOMoYJAGoo2p0'


##Nutrienttion is per hundred grams
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
"""


cypher_prompt = PromptTemplate(
    template=cypher_generation_template,
    input_variables=["schema", "question"]
)

CYPHER_QA_TEMPLATE = """
    You are a nutrtition assistant that performs calculations using Information.
    The Information is in json format.
    Go through the JSON, looking for anything that corresponds to User, such as property key, using that, find the gender and age.

    The information part contains the provided information that you must use to construct an answer, read and understand its data structure very well.

    In the Information there is user_relationship which shows the quantity needed of a nutrient for a user of certain age and gender.
    There is also quantity_per_100g which shows the nutrients per 100g of a food.

    You must perform calculations to determine if eating a meal exceeds or falls short of a users Recommended Daily Intake for the day.
    You perform Recommended daily intake calculations using the user quantity needed to nutrients and the amount of nutrients per 100g contained in foods.
    Make sure to show all mathematical workings in the result.

    If the provided information is empty, say that you don't know the answer.


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
        #verbose=True,
        return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt,
        validate_cypher=True,
        top_k=100,
    )
    result = chain.invoke(user_input)
    print(result)
    return result

query_graph("I am a {} Year Old {}. I have eaten {} of {}. I am about to eat {} of {}, should I eat it?".format('1-18y', 'Male', previous_quantities, previous_meals, desired_quantities, desired_meal))



