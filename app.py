import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Crop Advisor", page_icon="🌾")
st.title("🌾 AI Crop Advisor for Tamil Nadu")

st.markdown("Fill in your farm details below to get crop recommendations:")

with st.expander("🌱 Soil & Land Characteristics"):
    soil_type = st.text_input("Soil Type")
    drainage = st.text_input("Drainage Capacity")
    area = st.text_input("Area Available (in acres)")
    crop_history = st.text_input("Previous Crop History")

with st.expander("📍 Location & Weather"):
    location = st.text_input("Location")
    weather = st.text_input("Weather")

with st.expander("🌾 Crop & Resource Preferences"):
    irrigation = st.selectbox("Irrigation", ["Canal", "Drip", "None"])
    budget = st.selectbox("Budget", ["Low", "Medium", "High"])
    preferred_crop = st.text_input("Preferred Crop Type")
    scheme = st.text_input("Scheme Eligibility")

if st.button("Generate Recommendations"):
    prompt = f"""
You are an agricultural advisor AI. Based on the following farm inputs, suggest the top 3 suitable crop types for the upcoming season in Tamil Nadu, India:

🌱 Soil & Land Characteristics:
- Soil Type: {soil_type or "Unknown"}
- Drainage Capacity: {drainage or "Unknown"}
- Area Available: {area or "Unknown"} acres
- Previous Crop History: {crop_history or "Unknown"}

📍 Location & Weather:
- Location: {location or "Unknown"}
- Weather: {weather or "Unknown"}

🌾 Crop & Resource Preferences:
- Irrigation: {irrigation}
- Budget: {budget}
- Preferred Crop Type: {preferred_crop or "Unknown"}
- Scheme Eligibility: {scheme or "Unknown"}

Please recommend 3 crops suitable for small to medium farms. Include brief reasoning for each.
"""

    try:
        model = genai.GenerativeModel(model_name="models/gemini-pro")
        response = model.generate_content(prompt)
        st.subheader("🌾 Recommended Crops")
        st.write(response.text)
    except Exception as e:
        st.error(f"❌ Error generating response: {str(e)}")
