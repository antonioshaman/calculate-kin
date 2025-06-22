from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(
    title="Kin Calculator API",
    description="Определяет точный Kin, Tone и Seal по Майянскому Цолькин для заданной даты.",
    version="1.0.0"
)

# Опорная дата для Цолькин
REFERENCE_DATE = datetime.strptime("26.07.2022", "%d.%m.%Y")

@app.get("/calculate-kin")
def calculate_kin(date: str = Query(..., description="Дата рождения в формате YYYY-MM-DD")):
    try:
        birth_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Неверный формат даты. Используй YYYY-MM-DD."}
        )
    delta_days = (birth_date - REFERENCE_DATE).days
    kin = ((delta_days % 260 + 260) % 260) + 1
    tone = ((kin - 1) % 13) + 1
    seal = ((kin - 1) % 20) + 1
    return {"Kin": kin, "Tone": tone, "Seal": seal, "Delta": delta_days}
