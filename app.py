from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI(
    title="Kin Proxy API (yamaya.ru парсер)",
    description="Парсит Kin, Tone и Seal напрямую с yamaya.ru для 100% совпадения.",
    version="1.0.0"
)

@app.get("/calculate-kin")
def calculate_kin(
    date: str = Query(..., description="Дата рождения в формате YYYY-MM-DD")
):
    try:
        year, month, day = date.split("-")
        day = int(day)
        month = int(month)
        year = int(year)
    except:
        return JSONResponse(
            status_code=400,
            content={"error": "Неверный формат даты. Используй YYYY-MM-DD."}
        )

    url = (
        f"https://yamaya.ru/maya/choosedate/"
        f"?action=setOwnDate&formday={day}&formmonth={month}&formyear={year}"
    )

    r = requests.get(url)
    if r.status_code != 200:
        return JSONResponse(
            status_code=500,
            content={"error": f"yamaya.ru не ответил. Код: {r.status_code}"}
        )

    soup = BeautifulSoup(r.text, "html.parser")

    # Найти блок с Кином
    try:
        text = soup.get_text()
        lines = text.splitlines()
        kin = None
        tone = None
        seal = None
        for line in lines:
            if line.strip().startswith("Кин:"):
                kin = line.strip().replace("Кин:", "").strip()
            if line.strip().startswith("Печать:"):
                seal = line.strip().replace("Печать:", "").strip()
            if line.strip().startswith("Тон:"):
                tone = line.strip().replace("Тон:", "").strip()

        if kin and seal and tone:
            return {
                "Kin": kin,
                "Seal": seal,
                "Tone": tone,
                "source": url
            }
        else:
            return JSONResponse(
                status_code=500,
                content={"error": "Не удалось распарсить ответ yamaya.ru"}
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
