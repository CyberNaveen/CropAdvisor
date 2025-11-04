# 🌾 CropAdvisor Backend (AI + Auth)

Flask backend combining:
- User registration & login (with JWT)
- Crop recommendation AI (Gemini)

## Run locally
```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_api_key
export DATABASE_URL=postgresql+psycopg2://postgres:password@host:5432/postgres
export SECRET_KEY=super_secret_key
python app.py
