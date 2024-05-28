import streamlit as st

st.title("A Nutririon Advisor for Sickle Cell Disease")
st.sidebar.title("Eliza Cares")
st.sidebar.image('logo.png')

st.radio('I have eaten today',['Yes','No'])
st.radio('Pick your gender',['Male','Female'])
st.selectbox('Pick your Age Group',['1-18','18-70', '70+'])
st.multiselect('choose a planet',['Jupiter', 'Mars', 'neptune'])
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.slider('Pick a number', 0,50)


st.progress(10)
st.button('Submit')