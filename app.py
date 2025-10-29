from flask import Flask, request, Response
from flask_cors import CORS
import google.generativeai as genai
import os

# 🔐 Optional: Load API key from environment
# from dotenv import load_dotenv
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 🔥 Direct API key setup
API_KEY = "AIzaSyCqS9615Ggp1g7CvXmbEO-T4L9wUs4e9hE"
genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json

    # 🧠 Format prompt using structured farmer inputs
    prompt = f"""
You are an agricultural advisor AI. Based on the following farm inputs, suggest the top 3 suitable crop types for the upcoming season in Tamil Nadu, India:

🌱 Soil & Land Characteristics:
- Soil Type: {data.get("soil_type", "Unknown")}
- Drainage Capacity: {data.get("drainage", "Unknown")}
- Area Available: {data.get("area", "Unknown")} acres
- Previous Crop History: {data.get("crop_history", "Unknown")}

📍 Location & Weather:
- Location: {data.get("location", "Unknown")}
- Weather: {data.get("weather", "Unknown")}

🌾 Crop & Resource Preferences:
- Irrigation: {data.get("irrigation", "Unknown")}
- Budget: {data.get("budget", "Unknown")}
- Preferred Crop Type: {data.get("preferred_crop", "Unknown")}
- Scheme Eligibility: {data.get("scheme", "Unknown")}

Please recommend 3 crops suitable for small to medium farms. Include brief reasoning for each.
"""

    def generate():
        model = genai.GenerativeModel("gemini-1.5-flash")
        stream = model.generate_content([prompt], stream=True)
        for chunk in stream:
            if chunk.text:
                yield chunk.text

    return Response(generate(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


