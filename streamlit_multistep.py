import streamlit as st
import requests
from streamlit_geolocation import streamlit_geolocation

API_URL = "http://localhost:5000"  # Update this if your Flask API is hosted elsewhere

st.title("Rube Goldberg Planner 🎭")

st.write("Welcome to the craziest plan generator ever! 🚀 What's your goal, fam?")

# Get location using streamlit_geolocation
st.subheader("📍 Your Location")
location = streamlit_geolocation()
st.session_state.action_steps = []
st.session_state.action_results = []

if location:
    st.session_state.lat = location.get('st.session_state.latitude')
    st.session_state.lon = location.get('st.session_state.longitude')
    st.session_state.accuracy = location.get('st.session_state.accuracy')
    
    if st.session_state.lat and st.session_state.lon:
        st.success(f"Yo, we found you! 🗺️ You're at {st.session_state.lat:.4f}, {st.session_state.lon:.4f} (accuracy: {st.session_state.accuracy:.2f} meters)")
        st.map(data={"st.session_state.lat": [st.session_state.lat], "st.session_state.lon": [st.session_state.lon]})
    else:
        st.warning("Hmm, we got some location data, but it's missing the good stuff. Try again?")
else:
    st.info("Waiting for your location... Make sure to allow location access if prompted!")

goal = st.text_input("Enter your goal:", "Make me more money!")

if st.button("Generate Plan"):
    with st.spinner("Cooking up some wild ideas..."):
        # If we have location, include it in the API request
        payload = {"goal": goal}
        if location and location.get('st.session_state.latitude') and location.get('st.session_state.longitude'):
            payload["location"] = {
                "st.session_state.lat": location['st.session_state.latitude'],
                "st.session_state.lon": location['st.session_state.longitude']
            }
        
        response = requests.post(f"http://127.0.0.1:5000/plan", json=payload)
        
        if response.status_code == 200:
            st.session_state.action_steps = response.json()["plan"]
            print(st.session_state.action_steps)
            
            st.success("Yo, check out this insane plan! 🤪")
            
            for i, step in enumerate(st.session_state.action_steps, 1):
                st.write(f"**Step {i}:** {step}")
                # num, action, acceptance = step.split(";")
                # st.markdown(f"### Step {i}")
                # st.write(f"**Action:** {action}")
                # st.write(f"**Acceptance Criteria:** {acceptance}")
                
                # if st.button("Complete Step"):
                #     response = requests.post(f"http://127.0.0.1:5000/execute_step", json={"step": step})
                    
                #     if response.status_code == 200:
                #         action = response.json()["results"]
                #         st.write(f"**Results:** {action}")
                # elif st.button("Skip Step"):
                #     break
                # else:
                #     break
                
                st.markdown("---")
            
            st.balloons()
        else:
            st.error("Oops! Something went wrong. Try again, bestie!")

if st.session_state.action_steps:
    for i, step in enumerate(st.session_state.action_steps, 1):
        num, action, acceptance = step.split(";")
        st.markdown(f"### Step {i}")
        st.write(f"**Action:** {action}")
        st.write(f"**Acceptance Criteria:** {acceptance}")
        if st.button(f"Execute Step {num}"):
            print(step)
            response = requests.post(f"http://127.0.0.1:5000/execute_step", json={"step": step})
            st.session_state.action_results.append(response.json()["results"])
        if st.session_state.action_results:
            if result := st.session_state.action_results[i - 1]:
                st.write(f"**Results:** {result}")

st.markdown("---")
st.write("Remember, these plans are just for fun! Don't try this at home, kids! 😜")

# Optionally, display raw location data for debugging
if st.checkbox("Show raw location data"):
    st.json(location)