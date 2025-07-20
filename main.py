from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")), delimiter=";")

        df.columns = [col.strip().lower() for col in df.columns]

        if 'category' not in df.columns or 'amount' not in df.columns:
            return JSONResponse(content={"error": "Missing required columns."}, status_code=400)

        df['category'] = df['category'].astype(str).str.strip().str.lower()
        df['amount'] = df['amount'].astype(str).str.replace(r"[^\d\.\-]", "", regex=True).replace("", "0").astype(float)

        total_food_expense = df[df['category'] == 'food']['amount'].sum()

        return {
            "answer": round(total_food_expense, 2),
            "email": "your_email@domain.com",  # Change to your real email
            "exam": "tds-2025-05-roe"
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
