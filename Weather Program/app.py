import streamlit as st
import requests
import datetime

# OpenWeatherMap API Key (Replace with your API Key)
API_KEY = "4ba83ce9f9b03a86495a48af1e598986"
BASE_URL = "http://api.openweathermap.org/data/2.5/"

def get_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    return response

# Streamlit UI
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("🌤️ Weather Dashboard")
city = st.text_input("Enter City Name:", "Karachi")

if st.button("Get Weather"):
    weather_data = get_weather(city)
    if weather_data.get("cod") != 200:
        st.error("City not found! Please try again.")
    else:
        st.subheader(f"Current Weather in {city}")
        st.write(f"🌡️ Temperature: {weather_data['main']['temp']}°C")
        st.write(f"💧 Humidity: {weather_data['main']['humidity']}%")
        st.write(f"💨 Wind Speed: {weather_data['wind']['speed']} m/s")
