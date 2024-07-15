import streamlit as st
import anthropic
from streamlit_geolocation import streamlit_geolocation



# i am hungary and want to eat food at the michelin star restaurant in NYC but i'm broke.
# i'm single and ready to mingle. find me the love of my life.


# Initialize the Anthropic client
client = anthropic.Anthropic(
    api_key="anthropic-api-key"
)

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

if st.button("Generate Crazy Plan"):
    if goal:
        # Define the system message (preamble)
        PREAMBLE = """
        Come up with a crazy, weird, not practical plan to make it possible. **Eventually it has to be a succesful.**
        The plan has to resemble a Rube Goldberg machine, where response of anoe thing leads to another weird and crazy thing.
        Only list steps. Assume you have tools like: calling someone, booking a cab, money transfer, Google search,
        and anything else you can think of.

        Context: 
        - i'm shubham, my phone number of 551-229-7528
        - i'm in meatpacking district, NYC. 
        - it's sunny after noon. 
        - i'm at betaworks, working on a hackathon.


        Note: 
        1. Always output 4 things: step, tool, args, response, result. See example output format below. 
        2. tool, args, response are in a code block. tool is a python function name, args are the arguments, response HAS to be a JSON value.
        3. step and result are in a normal text.
        4. Note the to add all the new lines, and backticks and follow the example format as bwlow.

        <example>

        **Step 1: I'm finding the nearest most expensive restaurant**
        
        ```python
        tool: find_restaurant
        args: {'location': 'NYC', 'cuisine': 'italian'}
        response: [{
            'restaurant': "Il's Pizza",
            'price' : '$$$$'
        }]
        ```
        **Result: I found the restaurant "Il's Pizza" with a price of $$$.**
        
        ---
        
        Step 2.  ...

        Step 3.  ...

        .
        .
        .
        
        Step N: ...

        </example>
        """

        # Generate the plan using Claude
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024*4,
            system=PREAMBLE,
            messages=[
                {"role": "user", "content": goal}
            ]
        )


        # Display the generated plan
        st.subheader("Your Crazy Plan:")
        st.write(message.content[0].text)
    else:
        st.warning("Please enter a goal first!")

st.markdown("---")
st.write("Remember, these plans are just for fun! Don't try this at home, kids! 😜")
