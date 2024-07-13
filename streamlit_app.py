import streamlit as st
import requests

API_URL = "http://localhost:5000/generate_plan"  # Update this if your Flask API is hosted elsewhere

st.title("Rube Goldberg Planner 🎭")

st.write("Welcome to the craziest plan generator ever! 🚀 What's your goal, fam?")

goal = st.text_input("Enter your goal:", "Make me more money!")

if st.button("Generate Plan"):
    with st.spinner("Cooking up some wild ideas..."):
        response = requests.post(API_URL, json={"goal": goal})
        
        if response.status_code == 200:
            plan = response.json()["plan"]
            
            st.success("Yo, check out this insane plan! 🤪")
            
            for i, step in enumerate(plan, 1):
                st.markdown(f"### Step {i}")
                st.write(step)
                
            st.balloons()
        else:
            st.error("Oops! Something went wrong. Try again, bestie!")

st.markdown("---")
st.write("Remember, these plans are just for fun! Don't try this at home, kids! 😜")