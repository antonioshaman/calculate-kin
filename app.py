from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI(
    title="Kin Proxy API — yamaya.ru bulletproof POST",
    description="Эмулирует форму yamaya.ru POST для гарантированного расчёта.",
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

    base_url = "https://yamaya.ru/maya/choosedate/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Referer": base_url
    }

    s = requests.Session()
    s.headers.update(headers)

    # 1️⃣ Первый GET — получить форму и куки
    r1 = s.get(base_url)
    if r1.status_code != 200:
        return JSONResponse(
            status_code=500,
            content={"error": f"yamaya.ru не ответил (GET). Код: {r1.status_code}"}
        )

    # 2️⃣ Отправляем реальный POST как форма
    payload = {
        "action": "setOwnDate",
        "formday": day,
        "formmonth": month,
        "formyear": year,
        "submit": "OK"
    }

    r2 = s.post(base_url, data=payload)
    if r2.status_code != 200:
        return JSONResponse(
            status_code=500,
            content={"error": f"yamaya.ru не ответил (POST). Код: {r2.status_code}"}
        )

    r2.encoding = "windows-1251"

    soup = BeautifulSoup(r2.text, "html.parser")

    try:
        text = soup.get_text(separator="\n").strip()
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        kin = None
        tone = None
        seal = None

        for line in lines:
            if line.startswith("Кин:"):
                kin = line.replace("Кин:", "").strip()
            elif line.startswith("Тон:"):
                tone = line.replace("Тон:", "").strip()
            elif line.startswith("Печать:"):
                seal = line.replace("Печать:", "").strip()

        if kin and tone and seal:
            return {
                "Kin": kin,
                "Tone": tone,
                "Seal": seal,
                "source": r2.url
            }
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Не удалось распарсить результат. Найдено: Kin={kin}, Tone={tone}, Seal={seal}",
                    "debug_html_sample": text[:800]
                }
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Ошибка парсинга: {str(e)}"}
        )
