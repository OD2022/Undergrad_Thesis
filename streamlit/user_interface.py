import streamlit as st
import json
import os


def execute_python_file(file_path):
   try:
      with open(file_path, 'r') as file:
         python_code = file.read()
         exec(python_code)
   except FileNotFoundError:
      print(f"Error: The file '{file_path}' does not exist.")


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
        amount = st.sidebar.slider(slider_label, 0, 10000)
        stomach[food] = amount

desired_foods = {}
for food in selected_desired_options:
        slider_label = f'Select Quantity in Grams for {food + ' desired'}'
        amount = st.sidebar.slider(slider_label, 0, 10000)
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

       result = execute_python_file("C:/Users/Ibukun-Oluwa/Desktop/Undergrad_Thesis/kg_llm/main.py") 
       txt = st.text_area(result)    
       st.write(txt)
  

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


