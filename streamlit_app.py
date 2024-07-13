import streamlit as st
import requests
from streamlit_geolocation import streamlit_geolocation

API_URL = "http://localhost:5000/generate_plan"  # Update this if your Flask API is hosted elsewhere

st.title("Rube Goldberg Planner 🎭")

st.write("Welcome to the craziest plan generator ever! 🚀 What's your goal, fam?")

# Get location using streamlit_geolocation
st.subheader("📍 Your Location")
location = streamlit_geolocation()

if location:
    lat = location.get('latitude')
    lon = location.get('longitude')
    accuracy = location.get('accuracy')
    
    if lat and lon:
        st.success(f"Yo, we found you! 🗺️ You're at {lat:.4f}, {lon:.4f} (accuracy: {accuracy:.2f} meters)")
        st.map(data={"lat": [lat], "lon": [lon]})
    else:
        st.warning("Hmm, we got some location data, but it's missing the good stuff. Try again?")
else:
    st.info("Waiting for your location... Make sure to allow location access if prompted!")

goal = st.text_input("Enter your goal:", "Make me more money!")

if st.button("Generate Plan"):
    with st.spinner("Cooking up some wild ideas..."):
        # If we have location, include it in the API request
        payload = {"goal": goal}
        if location and location.get('latitude') and location.get('longitude'):
            payload["location"] = {
                "lat": location['latitude'],
                "lon": location['longitude']
            }
        
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            plan = response.json()["plan"]
            
            st.success("Yo, check out this insane plan! 🤪")
            
            for i, step in enumerate(plan, 1):
                st.markdown(f"### Step {i}")
                st.write(step["text"])
                
                if "tool_calls" in step and step["tool_calls"]:
                    st.subheader("Tool Calls:")
                    for call in step["tool_calls"]:
                        st.write(f"**Tool:** {call['name']}")
                        st.json(call['parameters'])
                
                if "tool_results" in step:
                    st.subheader("Tool Results:")
                    for result in step["tool_results"]:
                        st.write(f"**Tool:** {result['call']['name']}")
                        st.write("Parameters:")
                        st.json(result['call']['parameters'])
                        st.write("Outputs:")
                        st.json(result['outputs'])
                
                st.markdown("---")
            
            st.balloons()
        else:
            st.error("Oops! Something went wrong. Try again, bestie!")

st.markdown("---")
st.write("Remember, these plans are just for fun! Don't try this at home, kids! 😜")

# Optionally, display raw location data for debugging
if st.checkbox("Show raw location data"):
    st.json(location)