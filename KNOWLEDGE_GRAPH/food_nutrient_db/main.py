from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI


import dotenv
dotenv.load_dotenv()


NEO4J_CONNECTION_URL='neo4j+s://c492bfaa.databases.neo4j.io:7687'
NEO4J_USER='neo4j'
NEO4J_PASSWORD='qTS9vkpSZT1yZ57kseVCw2csO2Zx25IOMoYJAGoo2p0'


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
Question: “I am a 37 Year Old Female with Sickle Cell Disease. I have eaten 10g of Wholegrain Rolled Oats today. 
I am about to eat 20g of Aprapransa, should I eat it?”

Answer: ```
MATCH (user:User)-[:NEEDS]->(nutrient:Nutrient)
WHERE user.age_bracket = "19-70+y" 
  AND user.gender = "Female" 
RETURN user, nutrient, user-[:NEEDS]->nutrient AS needsRelationship

UNION

MATCH (eaten_food:Food)-[:CONTAINS]->(eaten_nutrient:Nutrient),
      (about_to_eat_food:Food)-[:CONTAINS]->(about_to_eat_nutrient:Nutrient)
WHERE eaten_food.name = "Wholegrain Rolled Oats"
WITH eaten_food, eaten_nutrient
RETURN eaten_food.name AS eatenFoodName,
       eaten_nutrient.name AS eatenNutrientName

       
UNION

MATCH (eaten_food:Food)-[:CONTAINS]->(eaten_compound:Compound),
      (about_to_eat_food:Food)-[:CONTAINS]->(about_to_eat_compound:Compound)
WHERE eaten_food.name = "Wholegrain Rolled Oats"
WITH eaten_food, eaten_compound
RETURN eaten_food.name AS eatenFoodName,
       eaten_compound.name AS eatenCompoundName

UNION

MATCH (eaten_food:Food)-[:CONTAINS]->(eaten_nutrient:Nutrient),
      (about_to_eat_food:Food)-[:CONTAINS]->(about_to_eat_nutrient:Nutrient)
WHERE about_to_eat_food.name = "Aprapransa"
WITH about_to_eat_food, about_to_eat_nutrient
RETURN about_to_eat_food.name AS aboutToEatFoodName,
       about_to_eat_nutrient.name AS aboutToEatNutrientName

UNION

MATCH (eaten_food:Food)-[:CONTAINS]->(eaten_compound:Compound),
      (about_to_eat_food:Food)-[:CONTAINS]->(about_to_eat_compound:Compound)
WHERE about_to_eat_food.name = "Aprapransa"
WITH about_to_eat_food, about_to_eat_compound
RETURN about_to_eat_food.name AS aboutToEatFoodName,
       about_to_eat_compound.name AS aboutToEatCompoundName

```
Question: {question}
"""
cypher_prompt = PromptTemplate(
    template=cypher_generation_template,
    input_variables=["schema", "question"]
)

CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
If the provided information is empty, say that you don't know the answer.
Final answer should be easily readable and structured.
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
        return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt,
        validate_cypher=True,
        top_k=100,
    )
    result = chain.invoke(user_input)
    print(result)
    return result

query_graph(" I am a 37 Year Old Female with Sickle Cell Disease. I have eaten 10g of Wholegrain Rolled Oats today. I am about to eat 20g of Aprapransa, should I eat it?")



