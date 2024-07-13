import streamlit as st
import streamlit.components.v1 as components

def get_geolocation():
    geolocation_html = """
    <script>
    const sendGeolocation = (lat, lon) => {
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: JSON.stringify({lat: lat, lon: lon})
        }, "*");
    };

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => sendGeolocation(position.coords.latitude, position.coords.longitude),
            (error) => sendGeolocation(null, null),
            {enableHighAccuracy: true, timeout: 5000, maximumAge: 0}
        );
    } else {
        sendGeolocation(null, null);
    }
    </script>
    """
    
    component_value = components.html(geolocation_html, height=0)
    return component_value

def get_location():
    if 'location' not in st.session_state:
        st.session_state.location = get_geolocation()
    
    return st.session_state.location

if __name__ == "__main__":
    st.title("Geolocation Test")
    location = get_location()
    if location:
        st.write(f"Your location: {location}")
    else:
        st.write("Waiting for location...")