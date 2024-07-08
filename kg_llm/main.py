from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
import dotenv
import json
dotenv.load_dotenv()
import streamlit as st
import os

user_profile={}
user_stomach = {}
next_meal = {}

NEO4J_CONNECTION_URL='neo4j+s://c492bfaa.databases.neo4j.io:7687'
NEO4J_USER='neo4j'
NEO4J_PASSWORD='qTS9vkpSZT1yZ57kseVCw2csO2Zx25IOMoYJAGoo2p0'


##Nutrient is per hundred grams
age = '19-70y'
gender = 'Female'
previous_meals = ['Hummus','Aprapransa']
previous_quantities = [10, 200]
desired_meal = ['Firm Tofu', 'Jollof Rice']
desired_quantities = [20, 30]


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
Question: "I am a $age Year Old $gender with Sickle Cell Disease. I have eaten $previous_quantities of $previous_meals respectively. I am about to eat $desired_quantity of $desired_meal respectively, how would this affect my nutrient intake?".

Answer: ```
MATCH (user:User)-[user_relationship:NEEDS]->(nutrient:Nutrient)
WHERE user.age_bracket = $age AND user.gender = $gender

MATCH (eaten_food:Food)-[eaten_food_relationship:CONTAINS]->(eaten_food_nutrient:Nutrient)
WHERE eaten_food.name IN $previous_meals

MATCH (desired_food:Food)-[desired_food_relationship:CONTAINS]->(desired_food_nutrient:Nutrient)
WHERE desired_food.name IN $desired_meal
RETURN user, nutrient, user_relationship.quantity_needed, eaten_food_relationship.quantity_per_100g, eaten_food_nutrient, desired_food_nutrient, desired_food_relationship.quantity_per_100g;
```
Question: {question}

"""


cypher_generation_template2 = """
You are an expert Neo4j Cypher translator who converts English to Cypher based on the Neo4j Schema provided, following the instructions below:
1. Generate Cypher query compatible ONLY for Neo4j Version 5
2. Do not use EXISTS, SIZE, HAVING, CONTAINS, keywords in the cypher. Use alias when using the WITH keyword
3. Use only Nodes and relationships mentioned in the schema
4. Always do a case-insensitive and fuzzy search for any properties related search. 
5. Never use relationships that are not mentioned in the given schema
6. When asked about anything, Match the properties using non-case-insensitive matching 

schema: {schema}

Examples:
Question: "I am a $age Year Old $gender with Sickle Cell Disease. I have eaten $previous_quantities of $previous_meals respectively. I am about to eat $desired_quantity of $desired_meal respectively. What are the compounds and health effects?"

Answer: ```

MATCH (eaten_food:Food)-[:CONTAINS_COMPOUND]->(eaten_food_compound:Compound)-[:HAS_EFFECT]->(eaten_food_health_effect:HealthEffect)
WHERE eaten_food.name IN $previous_meals

MATCH (desired_food:Food)-[:CONTAINS_COMPOUND]->(desired_food_compound:Compound)-[:HAS_EFFECT]->(desired_food_health_effect:HealthEffect)
WHERE desired_food.name IN $desired_meal

RETURN eaten_food, eaten_food_compound, eaten_food_health_effect, desired_food, desired_food_compound, desired_food_health_effect;

```
Question: {question}

"""

cypher_prompt = PromptTemplate(
    template=cypher_generation_template,
    input_variables=["schema", "question"]
)

cypher_prompt2 = PromptTemplate(
    template=cypher_generation_template2,
    input_variables=["schema", "question"]
)

CYPHER_QA_TEMPLATE = """

You are a nutrtition assistant that performs calculations and gives advice using Information.
The Information is in JSON format.

The JSON contains the provided information that you must use to construct an answer, read and understand the jsob data structure very well.
Go through the JSON, looking for anything that corresponds to User, such as property key, using that, find the gender and age.
Go through the JSON, finding all data where the key is eaten_food_nutrient and desired_food_nutrient.

Take note of all the nutrients found in each food, using the eaten_food_nutrient and desired_food_nutrient keys.
For every nutrient in the food, there is quantity_per_100g which shows the nutrients per 100g of that nutrient in the food.

In the JSON there is user_relationship.quantity_needed which shows the quantity needed of different nutrients for a user of certain age and gender, this is their Recommended Daily Intake.
To determine if eating a meal exceeds or falls short of a users Recommended Daily Intake of a nutrient, you must perform calculations using user_relationship.quantity_needed, eaten_food_relationship.quantity_per_100g and desired_food_relationship.quantity_per_100g
Make sure to show all mathematical workings, then advice the user based on findings.

If the provided information is empty, say that you don't know the answer.


Information:
{context}
Question: {question}
Helpful Answer:
"""


CYPHER_QA_TEMPLATE2= """
You are a nutrtition assistant that analyzes foods, their compounds and health effects.
The JSON contains the provided information that you must use to construct an answer, read and understand its data structure very well.
You must discuss the health effects found in the foods, 
using the values of the keys eaten_foods_health_effects, desired_foods_health_effect.
If the provided information is empty, say that the foods currently do not have information about their compounds.

Information:
{context}
Question: {question}
Helpful Answer:"""


qa_prompt = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)

qa_prompt_2 = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE2
)

def query_graph(my_cypher_prompt, my_qa_prompt, my_query):
    graph = Neo4jGraph(url=NEO4J_CONNECTION_URL, username=NEO4J_USER, password=NEO4J_PASSWORD)
    graph.refresh_schema()
    chain = GraphCypherQAChain.from_llm(
        cypher_llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
        qa_llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
        graph=graph,
        verbose=True,
        #return_intermediate_steps=True,
        cypher_prompt=my_cypher_prompt,
        qa_prompt=my_qa_prompt,
        validate_cypher=True,
        top_k=100,
    )
   
    with open('user_profile.json', 'r') as file:
        # Load JSON data from the file
            user_profile = json.load(file)

    with open('user_stomach.json', 'r') as file:
        # Load JSON data from the file
            user_stomach = json.load(file)

    with open('next_meal.json', 'r') as file:
        # Load JSON data from the file
            next_meal = json.load(file)

    quantity_eaten = []
    food_eaten = []
    quantity_to_eat = []
    food_to_eat = []

    for food in user_stomach:
        quantity_eaten.append(user_stomach[food])
        food_eaten.append(food)
        
    for food in next_meal:
        quantity_to_eat.append(next_meal[food])
        food_to_eat.append(food)


    nutrient_query = "I am a {}y Year Old {}. with Sickle Cell Disease. I have eaten {}g of {} respectively. I am about to eat {}g of {} respectively. How would this affect my nutrient intake?".format(user_profile['age'], user_profile['sex'], quantity_eaten, food_eaten, quantity_to_eat, food_to_eat)
    compound_query = "I am a {}y Year Old {}. with Sickle Cell Disease. I have eaten {}g of {} respectively. I am about to eat {}g of {} respectively. What are the compounds and health effects?".format(user_profile['age'], user_profile['sex'], quantity_eaten, food_eaten, quantity_to_eat, food_to_eat)
    
    if my_query == 'nutrient':
       result = chain.invoke(nutrient_query)
    elif my_query == 'compound':
       result = chain.invoke(compound_query)
    return result


##Streamlit user interface
st.image('logo2.png')
st.title("Helena Cares: \n A Nutrition Advisor for Ghanaians with Sickle Cell Disease")
st.markdown('#')

st.sidebar.title("Quantity Selector")

eaten_food_options = ['Tom Brown', 'Shitto', 'Hummus', 'Jollof Rice', 'Grilled Chicken', 'Fried Chicken', 'Aprapransa', 'Muesli (Almond)',
                      'Wholegrain Rolled Oats', 'Almond Milk', 'Soy Milk', 'Firm Tofu', 'Aprapransa', 'Yam with kontomire stew', 'Yam with garden egg stew', 'Plantain with kontomire stew', 'Plantain with garden egg stew', 'Fufu with light soup', 'Fufu with palm-nut soup', 'Fufu with groundnut soup', 'Konkonte with palm-nut soup', 'Konkonte with groundnut soup', 'Akple with okro soup', 'Kooko with bread', 'Kenkey with fried fish and pepper', 'Plain rice and stew', 'Omo tuo with palm-nut soup', 'Omo tuo with groundnut soup', 'Waakye with stew', 'Hausa Kooko with bread and akara', 'Tuo zaafi', 'Beans with fried plantain'
                      ]
selected_eaten_options = st.multiselect('What You have eaten in the past 24 hours?', eaten_food_options)

desired_food_options = ['Tom Brown', 'Shitto', 'Hummus', 'Jollof Rice', 'Grilled Chicken', 'Fried Chicken', 'Aprapransa', 'Muesli (Almond)',
                      'Wholegrain Rolled Oats', 'Almond Milk', 'Soy Milk', 'Firm Tofu', 'Aprapransa', 'Yam with kontomire stew', 'Yam with garden egg stew', 'Plantain with kontomire stew', 'Plantain with garden egg stew', 'Fufu with light soup', 'Fufu with palm-nut soup', 'Fufu with groundnut soup', 'Konkonte with palm-nut soup', 'Konkonte with groundnut soup', 'Akple with okro soup', 'Kooko with bread', 'Kenkey with fried fish and pepper', 'Plain rice and stew', 'Omo tuo with palm-nut soup', 'Omo tuo with groundnut soup', 'Waakye with stew', 'Hausa Kooko with bread and akara', 'Tuo zaafi', 'Beans with fried plantain'
                      ]
selected_desired_options = st.multiselect('What are you planning to eat now?', desired_food_options)



stomach = {}
for food in selected_eaten_options:
        slider_label = f'Quantity in Grams for {food + ' eaten'}'
        amount = st.sidebar.slider(slider_label, 0, 1000)
        stomach[food] = amount

desired_foods = {}
for food in selected_desired_options:
        slider_label = f'Select Quantity in Grams for {food + ' desired'}'
        amount = st.sidebar.slider(slider_label, 0, 1000)
        desired_foods[food] = amount


user_sex = st.radio('What is your gender?',['Male','Female'])
user_age_group = st.selectbox('Pick your Age Group',['1-18','19-70', '70+', 'Pregnancy', 'Lactation'])
user_weight = st.text_input('What is your weight in kilograms?')
user_height = st.text_input('What is your height in meters?')
submitted = st.button("Get Advice")

if submitted:
       user_info = {}
       user_info['age'] = user_age_group
       user_info['sex'] = user_sex
       user_info['weight'] = user_weight
       user_info['height'] = user_height
       st.write(stomach, desired_foods)

       with open('user_profile.json', 'w') as fp:
            json.dump(user_info, fp)

       with open('user_stomach.json', 'w') as fp:
            json.dump(stomach, fp)
        
       with open('next_meal.json', 'w') as fp:
            json.dump(desired_foods, fp)
      
       nutrient_result = query_graph(cypher_prompt, qa_prompt, 'nutrient')
       container = st.container(border=True)
       container.write(nutrient_result)

       container2 = st.container(border=True)
       compound_result = query_graph(cypher_prompt2, qa_prompt_2, 'compound')
       container2.write(compound_result)

st.markdown(
    f"""
    <style>
        img {{
            border-radius: 80%;
            overflow: hidden;
            width: 200px;
            height: 200px;
           
        }}
    </style>
    """,
    unsafe_allow_html=True
) 


