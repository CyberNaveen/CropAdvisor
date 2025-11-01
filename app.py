from flask import Flask, request, Response
from flask_cors import CORS
from google import genai
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "✅ CropAdvisor backend is running"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        prompt = f"""
        You are an agricultural advisor AI...
        (your full prompt here)
        """

        response = client.models.generate_content(
            model="gemini-1.5-flash",   # or "gemini-2.5-pro"
            contents=prompt
        )

        return Response(response.text, mimetype="text/plain")

    except Exception as e:
        print("❌ Flask error:", e)
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
