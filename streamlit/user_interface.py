import streamlit as st
import json
import os

st.image('logo2.png')
st.title("IOEAs Nutrition Advisor for Ghanaians with Sickle Cell Disease")


st.sidebar.title("Quantity Selector")

eaten_food_options = ['Hummus', 'Jollof Rice', 'Grilled Chicken', 'Fried Chicken', 'Aprapransa']
selected_eaten_options = st.multiselect('What You have eaten in the past 24 hours?', eaten_food_options)

desired_food_options = ['Firm Tofu', 'Jollof Rice', 'Grilled Chicken', 'Fried Chicken', 'Aprapransa']
selected_desired_options = st.multiselect('What are you planning to eat now?', desired_food_options)



stomach = {}
for food in selected_eaten_options:
        slider_label = f'Quantity in Grams for {food + ' eaten'}'
        amount = st.sidebar.slider(slider_label, 0, 10000)
        stomach[food] = amount

desired_foods = {}
for food in selected_desired_options:
        slider_label = f'Select Quantity in Grams for {food + ' desired'}'
        amount = st.sidebar.slider(slider_label, 0, 10000)
        desired_foods[food] = amount


user_sex = st.radio('What is your gender?',['Male','Female'])
user_age_group = st.selectbox('Pick your Age Group',['1-18','19-70', '70+'])
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