from flask import Flask, request, Response
from flask_cors import CORS
import google.generativeai as genai
import os
import time

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

        print("🧠 Prompt sent to Gemini:\n", prompt)

        def generate():
            try:
                model = genai.GenerativeModel(model_name="gemini-2.5-pro")
                start = time.time()
                stream = model.generate_content(prompt, stream=True)
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text
                print("⏱ Gemini response time:", time.time() - start)
            except Exception as gen_error:
                print("❌ Gemini streaming error:", gen_error)
                yield "⚠️ AI request failed: switching to fallback mode.\n"
                try:
                    response = model.generate_content(prompt)
                    yield response.text
                except Exception as fallback_error:
                    print("❌ Gemini fallback error:", fallback_error)
                    yield f"Error generating response: {str(fallback_error)}"

        return Response(generate(), mimetype="text/plain")

    except Exception as e:
        print("❌ Flask error:", e)
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
