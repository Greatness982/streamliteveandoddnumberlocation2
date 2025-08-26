import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# ------------------ Streamlit Config ------------------
st.set_page_config(page_title="📍 Location Finder", page_icon="🌍", layout="centered")

st.title("📍 Location Finder")
st.write("Enter a place name and see it on the map!")

# ------------------ Input ------------------
place = st.text_input("Enter a location (e.g., Lagos, Nigeria):")

if place:
    try:
        # Geocode location
        geolocator = Nominatim(user_agent="location_app")
        location = geolocator.geocode(place)

        if location:
            st.success(f"✅ Found: {location.address}")
            st.write(f"🌍 Coordinates: **{location.latitude}, {location.longitude}**")

            # Show map
            m = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)
            folium.Marker([location.latitude, location.longitude], popup=place, tooltip="Target Location").add_to(m)

            st_folium(m, width=700, height=500)

        else:
            st.error("❌ Location not found. Try again!")

    except Exception as e:
        st.error(f"Error: {e}")
