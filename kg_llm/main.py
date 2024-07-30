# from langchain_community.graphs import Neo4jGraph
# from langchain.chains import GraphCypherQAChain
# from langchain.prompts.prompt import PromptTemplate
# from langchain_openai import ChatOpenAI
import dotenv
import json
dotenv.load_dotenv()
import streamlit as st
# import os
import time
from neo4j import GraphDatabase
import openai
from openai import OpenAI


user_profile={}
user_stomach = {}
next_meal = {}

NEO4J_CONNECTION_URL='neo4j+s://c492bfaa.databases.neo4j.io:7687'
NEO4J_USER='neo4j'
NEO4J_PASSWORD='qTS9vkpSZT1yZ57kseVCw2csO2Zx25IOMoYJAGoo2p0'
driver = GraphDatabase.driver(NEO4J_CONNECTION_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))


nutrient_context = """
You are a nutrition assistant that performs calculations 
and gives advice with the data given to you.

Always write out the quantity needed per nutrient(RDI), so the user can cross check your results.
The recommended Daily intake for the nutrient should be based on the data given to you that tells you how much the user needs of a given nutrient.
Take note of all the nutrients found in each food.
To determine if eating a meal exceeds or falls short of a users 
need(RDI) of a nutrient, you must perform calculations 
with the quantity of food eaten and the quantity of food desired to eat.
If the quantity of a nutrient for a certain food is not given. Do not make up answers.
"""



compound_context = """You are a nutrition assistant that analyzes foods, their compounds and health effects.
The data contains the provided information that you must use to construct an answer, 
read and understand its data structure very well, it contains compounds and their health effects.
You must discuss the health effects found.
"""


def query_gpt_with_context(prompt, context):
    client = OpenAI()
    completion = client.chat.completions.create(
    temperature=0,
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": prompt}
    ])
    return completion.choices[0].message.content


def generate_and_run_query_nutrients(driver, age, gender, previous_meals, desired_meals):
    query = """
    MATCH (user:User)-[needs:NEEDS]->(nutrient:Nutrient)
    WHERE user.age_bracket = $age AND user.gender = $gender
    WITH user, collect({nutrient: nutrient, quantity_needed: needs.quantity_needed}) AS needed_nutrients

    MATCH (eaten_food:Food)-[contains:CONTAINS]->(eaten_food_nutrient:Nutrient)
    WHERE eaten_food.name IN $previous_meals
    WITH needed_nutrients, collect({eaten_food: eaten_food, nutrient: eaten_food_nutrient, quantity_per_100g: contains.quantity_per_100g}) AS previous_meal_nutrients

    MATCH (desired_food:Food)-[contains:CONTAINS]->(desired_food_nutrient:Nutrient)
    WHERE desired_food.name IN $desired_meal
    WITH needed_nutrients, previous_meal_nutrients, collect({desired_food: desired_food, nutrient: desired_food_nutrient, quantity_per_100g: contains.quantity_per_100g}) AS desired_meal_nutrients

    RETURN needed_nutrients, previous_meal_nutrients, desired_meal_nutrients;"""

    params = {
        "age": age,
        "gender" : gender,
        "previous_meals" : previous_meals,
        "desired_meal" : desired_meals
    }

    result_str = ""
    previous_meal_nutrients = []
    desired_meal_nutrients = []
    needed_nutrients = []

    with driver.session() as session:
        results = session.run(query, **params)
        
        for record in results:
            # Extract needed nutrients
            needed_nutrients = record.get('needed_nutrients', [])
            result_str += "Needed Nutrients:\n"
            for item in needed_nutrients:
                nutrient = item.get('nutrient', {})
                quantity_needed = item.get('quantity_needed', 'Unknown')
                result_str += f"- Nutrient: {nutrient.get('name', 'Unknown')}, Quantity Needed: {quantity_needed} \n"

            # Extract previous meal nutrients
            previous_meal_nutrients = record.get('previous_meal_nutrients', [])
            result_str += "\nPrevious Meal Nutrients:\n"
            for item in previous_meal_nutrients:
                eaten_food = item.get('eaten_food', {})
                nutrient = item.get('nutrient', {})
                quantity_per_100g = item.get('quantity_per_100g', 'Unknown')
                result_str += f"- Food: {eaten_food.get('name', 'Unknown')}, Nutrient: {nutrient.get('name', 'Unknown')}, Quantity per 100g: {quantity_per_100g} \n"

            # Extract desired meal nutrients
            desired_meal_nutrients = record.get('desired_meal_nutrients', [])
            result_str += "\nDesired Meal Nutrients:\n"
            for item in desired_meal_nutrients:
                desired_food = item.get('desired_food', {})
                nutrient = item.get('nutrient', {})
                quantity_per_100g = item.get('quantity_per_100g', 'Unknown')
                result_str += f"- Food: {desired_food.get('name', 'Unknown')}, Nutrient: {nutrient.get('name', 'Unknown')}, Quantity per 100g: {quantity_per_100g} \n"

    driver.close()
    return result_str




def generate_and_run_query_compounds(driver, previous_meals, desired_meals):
    query = """
    MATCH (eaten_food:Food)-[:CONTAINS_COMPOUND]->(eaten_food_compound:Compound)-[:HAS_EFFECT]->(eaten_food_health_effect:HealthEffect)
    WHERE eaten_food.name IN $previous_meals
    WITH collect({eaten_food: eaten_food, compound: eaten_food_compound, health_effect: eaten_food_health_effect}) AS previous_meal_effects

    MATCH (desired_food:Food)-[:CONTAINS_COMPOUND]->(desired_food_compound:Compound)-[:HAS_EFFECT]->(desired_food_health_effect:HealthEffect)
    WHERE desired_food.name IN $desired_meal
    WITH previous_meal_effects, collect({desired_food: desired_food, compound: desired_food_compound, health_effect: desired_food_health_effect}) AS desired_meal_effects

    RETURN previous_meal_effects, desired_meal_effects;"""

    params = {
        "previous_meals" : previous_meals,
        "desired_meal" : desired_meals
    }
    

    result_str = ""    
    with driver.session() as session:
        results = session.run(query, **params)
        for record in results:
            result_str = ""

            # Extract previous meal effects
            previous_meal_effects = record.get('previous_meal_effects', [])
            result_str += "Previous Meal Effects:\n"
            
            #if previous_meal_effects:
            for effect in previous_meal_effects:
                    eaten_food = effect.get('eaten_food', {})
                    health_effect = effect.get('health_effect', {})
                    compound = effect.get('compound', {})

                    if eaten_food:
                        result_str += f"- Eaten Food: {eaten_food.get('name', 'Unknown')} (ID: {eaten_food.get('element_id', 'Unknown')})\n"
                        
                        # Extract and show health effects related to eaten food
                        eaten_food_health_effects = eaten_food.get('health_effects', [])
                        if eaten_food_health_effects:
                            result_str += "  - Health Effects for Eaten Food:\n"
                            for health_effect in eaten_food_health_effects:
                                result_str += f"    * Health Effect: {health_effect.get('description', 'Unknown')} (ID: {health_effect.get('element_id', 'Unknown')})\n"
                    
                    if health_effect:
                        result_str += f"  - Health Effect: {health_effect.get('description', 'Unknown')} (ID: {health_effect.get('element_id', 'Unknown')})\n"
                    if compound:
                        result_str += f"  - Compound: {compound.get('name', 'Unknown')} (ID: {compound.get('element_id', 'Unknown')})\n"

            else:
                result_str += "  No previous meal effects available.\n"

            # Extract desired meal effects
            desired_meal_effects = record.get('desired_meal_effects', [])
            result_str += "\nDesired Meal Effects:\n"
            
            if desired_meal_effects:
                for effect in desired_meal_effects:
                    desired_food = effect.get('desired_food', {})
                    health_effect = effect.get('health_effect', {})
                    compound = effect.get('compound', {})

                    if desired_food:
                        result_str += f"- Desired Food: {desired_food.get('name', 'Unknown')} (ID: {desired_food.get('element_id', 'Unknown')})\n"
                        
                        # Extract and show health effects related to desired food
                        desired_food_health_effects = desired_food.get('health_effects', [])
                        if desired_food_health_effects:
                            result_str += "  - Health Effects for Desired Food:\n"
                            for health_effect in desired_food_health_effects:
                                result_str += f"    * Health Effect: {health_effect.get('description', 'Unknown')} (ID: {health_effect.get('element_id', 'Unknown')})\n"
                    
                    if health_effect:
                        result_str += f"  - Health Effect: {health_effect.get('description', 'Unknown')} (ID: {health_effect.get('element_id', 'Unknown')})\n"
                    if compound:
                        result_str += f"  - Compound: {compound.get('name', 'Unknown')} (ID: {compound.get('element_id', 'Unknown')})\n"

            else:
                result_str += "  No desired meal effects available.\n"


    
    driver.close()
    print(result_str)
    return result_str


def get_results():
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

    nutrient_result = generate_and_run_query_nutrients(driver, user_profile['age'], user_profile['sex'], food_eaten, food_to_eat)
    compound_result = generate_and_run_query_compounds(driver, food_eaten, food_to_eat)
       
    formatted_eaten = ["{}g of {}".format(amount, food) for food, amount in zip(food_eaten, quantity_eaten)]
    formatted_planned = ["{}g of {}".format(amount, food) for food, amount in zip(food_to_eat, quantity_to_eat)]

    eaten_str = ", ".join(formatted_eaten)
    planned_str = ", ".join(formatted_planned)
       
    nutrient_prompt = "If I eat what I desire to eat, have I met or exceeded or am I behind in my nutrient intakes for these nutrients for the day? I have eaten {} and plan to eat {} respectively.".format(eaten_str, planned_str)
    nutrient_response = query_gpt_with_context(nutrient_result + nutrient_prompt, nutrient_context)

    compound_prompt = "How will the compounds in these foods I have eaten or plan to eat affect my health"
    compound_response = query_gpt_with_context(compound_prompt + compound_result, compound_context)

    return nutrient_response, compound_response






##Streamlit user interface
st.image('logo2.png')
st.title("Helena Cares: \n A Nutrition Advisor for Ghanaians with Sickle Cell Disease")
st.markdown('#')

st.sidebar.title("Quantity Selector")

eaten_food_options = ['Tom Brown', 'Shitto', 'Hummus', 'Jollof Rice', 'Aprapransa', 'Muesli (Almond)',
                      'Wholegrain Rolled Oats', 'Almond Milk', 'Soy Milk', 'Firm Tofu', 'Aprapransa', 'Yam with kontomire stew', 'Yam with garden egg stew', 'Plantain with kontomire stew', 'Plantain with garden egg stew', 'Fufu with light soup', 'Fufu with palm-nut soup', 'Fufu with groundnut soup', 'Konkonte with palm-nut soup', 'Konkonte with groundnut soup', 'Akple with okro soup', 'Kooko with bread', 'Kenkey with fried fish and pepper', 'Plain rice and stew', 'Omo tuo with palm-nut soup', 'Omo tuo with groundnut soup', 'Waakye with stew', 'Hausa Kooko with bread and akara', 'Tuo zaafi', 'Beans with fried plantain'
                      ]
selected_eaten_options = st.multiselect('What You have eaten in the past 24 hours?', eaten_food_options)

desired_food_options = ['Tom Brown', 'Shitto', 'Hummus', 'Jollof Rice', 'Aprapransa', 'Muesli (Almond)',
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
user_age_group = st.selectbox('Pick your Age Group',["1-3y",
            "4-8y",
            "9-13y",
            "14-18y",
            "19-50y",
            "51-69y",
            "70+y", 'Pregnancy', 'Lactation'])
user_weight = st.text_input('What is your weight in kilograms?')
user_height = st.text_input('What is your height in meters?')
submitted = st.button("Get Advice")

if submitted:
       user_info = {}
       user_info['age'] = user_age_group
       user_info['sex'] = user_sex
       user_info['weight'] = user_weight
       user_info['height'] = user_height
       #st.write(stomach, desired_foods)

       with open('user_profile.json', 'w') as fp:
            json.dump(user_info, fp)

       with open('user_stomach.json', 'w') as fp:
            json.dump(stomach, fp)
        
       with open('next_meal.json', 'w') as fp:
            json.dump(desired_foods, fp)
      

       ###Querying for nutrients
       n_start_time = time.time()
       nutrient_data = get_results()[0]
       nutrient_time = (time.time() - n_start_time)

       #print("--- %s seconds ---" % (time.time() - n_start_time))
       container = st.container(border=True)
       container.write(nutrient_data)            

       ###Querying for compounds
       c_start_time = time.time()
       compound_result = get_results()[1]
       comp_time = (time.time() - c_start_time)

       #print("--- %s seconds ---" % (time.time() - c_start_time))
       container2 = st.container(border=True)
       container2.write(compound_result)
       container3 = st.container(border=True)
       container3.write(nutrient_time + comp_time)




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


