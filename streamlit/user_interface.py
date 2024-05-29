import streamlit as st


st.image('logo2.png')
st.title("IOEAs Nutrition Advisor for Ghanaians with Sickle Cell Disease")


st.sidebar.title("Quantity Selector")



st.radio('Have you eaten in the last 24 hours?',['Yes','No'])
eaten_food_options = ['Jollof Rice', 'Grilled Chicken', 'Fried Chicken', 'Aprapransa']
selected_eaten_options = st.multiselect('What You have eaten in the past 24 hours?', eaten_food_options)

desired_food_options = ['Jollof Rice', 'Grilled Chicken', 'Fried Chicken', 'Aprapransa']
selected_desired_options = st.multiselect('What are you planning to eat now?', desired_food_options)

# Conditional appearance based on selection status
for food in selected_eaten_options:
    slider_label = f'Quantity in Grams for {food + ' eaten'}'
    amount = st.sidebar.slider(slider_label, 0, 10000)


for food in selected_desired_options:
    slider_label = f'Select Quantity in Grams for {food + 'desired'}'
    amount = st.sidebar.slider(slider_label, 0, 10000)


st.radio('What is your gender?',['Male','Female'])
st.selectbox('Pick your Age Group',['1-18','18-70', '70+'])
st.radio("Select the system providing your report", ['Detailed', 'Summary', 'Explanatory'])
st.button('Get Advice')




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