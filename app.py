from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import google.generativeai as genai
import os, json
from dotenv import load_dotenv
from models import db, UserRecord
from auth import hash_password, verify_password, create_jwt

# Load env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)

# Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# -------------------
# Initialize DB at startup (Flask 3.1+ safe)
# -------------------
with app.app_context():
    db.create_all()

# -------------------
# Health
# -------------------
@app.route("/", methods=["GET"])
def home():
    return "✅ CropAdvisor backend is running"

# -------------------
# Auth Endpoints
# -------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    required = ["name", "username", "email", "mobileNumber", "password", "confirmPassword"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if data["password"] != data["confirmPassword"]:
        return jsonify({"error": "Passwords do not match"}), 400

    if UserRecord.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409
    if UserRecord.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    user = UserRecord(
        name=data["name"],
        username=data["username"],
        email=data["email"],
        mobileNumber=data["mobileNumber"],
        password=hash_password(data["password"])
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registration successful"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = UserRecord.query.filter_by(username=username).first()
    if not user or not verify_password(password, user.password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_jwt(user.id, user.username)
    return jsonify({"token": token, "user": {"id": user.id, "name": user.name, "username": user.username}})

# -------------------
# AI Crop Advisor
# -------------------
@app.route("/ask", methods=["GET"])
def ask_info():
    return "✅ Use POST to submit farm data for crop recommendations"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json or {}

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
        model = genai.GenerativeModel("models/gemini-flash-lite-latest")
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            try:
                crops = json.loads(response.text)["crops"]

                html = "<html><head><style>body{font-family:Arial;padding:20px;}h2{color:#2E7D32;}.card{border:1px solid #ccc;border-radius:8px;padding:15px;margin:10px 0;box-shadow:2px 2px 5px rgba(0,0,0,0.1);}h3{margin:0 0 8px;color:#1565C0;}p{margin:0;color:#333;}</style></head><body><h2>🌾 Recommended Crops</h2>"
                for crop in crops:
                    html += f"<div class='card'><h3>{crop['name']}</h3><p>{crop['reason']}</p></div>"
                html += "</body></html>"

                return Response(html, mimetype="text/html")
            except Exception:
                return Response(response.text, mimetype="text/plain")
        else:
            return Response("⚠️ No text field in Gemini response", mimetype="text/plain")

    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500

# Local run
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
