import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

# ------------------ Retry Function ------------------
def safe_geocode(geolocator, query, retries=3):
    for i in range(retries):
        try:
            return geolocator.geocode(query, timeout=10)
        except GeocoderTimedOut:
            if i < retries - 1:
                continue
            else:
                return None

# ------------------ Streamlit Config ------------------
st.set_page_config(page_title="📍 Location Finder", page_icon="🌍", layout="centered")

st.title("📍 Location & Phone Tracker")
st.write("🏙 Enter a place name or phone number to get info!")

# ------------------ Place Input ------------------
place = st.text_input("Enter a location (e.g., Lagos, Nigeria):")

# ------------------ Phone Input ------------------
phone = st.text_input("📞 Enter a phone number with country code (e.g., +2348012345678):")

if place:
    try:
        geolocator = Nominatim(user_agent="location_app")
        location = safe_geocode(geolocator, place)

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

if phone:
    try:
        parsed_number = phonenumbers.parse(phone, None)

        # Get details
        country = geocoder.description_for_number(parsed_number, "en")
        sim_carrier = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)

        st.success("📱 Phone Number Info:")
        st.write(f"🌍 Country/Region: **{country}**")
        st.write(f"📡 Carrier: **{sim_carrier if sim_carrier else 'Unknown'}**")
        st.write(f"🕒 Timezone(s): **{', '.join(time_zones)}**")

        # Try to guess city by geocoding the country
        if country:
            geolocator = Nominatim(user_agent="phone_tracker")
            city_location = safe_geocode(geolocator, country)

            if city_location:
                st.write(f"🏙 Approx. City/Region: **{city_location.address}**")

                # Show map for phone location
                m = folium.Map(location=[city_location.latitude, city_location.longitude], zoom_start=5)
                folium.Marker([city_location.latitude, city_location.longitude],
                              popup=f"Phone Number: {phone}",
                              tooltip=country).add_to(m)

                st_folium(m, width=700, height=500)

    except Exception as e:
        st.error(f"⚠️ Could not parse number: {e}")
