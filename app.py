from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# 🔐 Load Gemini API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "✅ CropAdvisor backend is running"

@app.route("/ask", methods=["GET"])
def ask_info():
    return "✅ Use POST to submit farm data for crop recommendations"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json or {}

        # 🧠 Build the structured prompt
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

Please recommend 3 crops suitable for small to medium farms. 
Return the result in JSON format like this:

{{
  "crops": [
    {{"name": "Crop1", "reason": "Reasoning..."}},
    {{"name": "Crop2", "reason": "Reasoning..."}},
    {{"name": "Crop3", "reason": "Reasoning..."}}
  ]
}}
"""

        print("🧠 Prompt sent to Gemini:\n", prompt)
model = genai.GenerativeModel("models/gemini-flash-lite-latest")

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        # ✅ Always return only the text field
        if hasattr(response, "text") and response.text:
            try:
                # Try to parse JSON if Gemini followed the format
                return jsonify(eval(response.text))
            except Exception:
                # Fallback: return plain text
                return Response(response.text, mimetype="text/plain")
        else:
            return Response("⚠️ No text field in Gemini response", mimetype="text/plain")

    except Exception as e:
        print("❌ Flask error:", e)
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    # Run locally
    app.run(debug=True, host="0.0.0.0", port=5000)
