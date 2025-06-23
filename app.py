from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI(
    title="Kin Proxy API — парсер yamaya.ru (bulletproof)",
    description="Делает два запроса: получает сессию и парсит всё по паттерну, без привязки к CSS.",
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
    params = {
        "action": "setOwnDate",
        "formday": day,
        "formmonth": month,
        "formyear": year
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Referer": "https://yamaya.ru/maya/choosedate/"
    }

    s = requests.Session()
    s.headers.update(headers)

    # Инициализируем сессию для PHPSESSID
    s.get(base_url)

    # Второй запрос с куками
    r = s.get(base_url, params=params)
    if r.status_code != 200:
        return JSONResponse(
            status_code=500,
            content={"error": f"yamaya.ru не ответил. Код: {r.status_code}"}
        )

    soup = BeautifulSoup(r.text, "html.parser")

    try:
        # Новый способ: найти весь текст, где есть "Кин:"
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
                "source": r.url
            }
        else:
            # Debug: покажи первые 800 символов всего HTML
            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Не удалось распарсить результат. Найдено: Kin={kin}, Tone={tone}, Seal={seal}",
                    "debug_html_sample": r.text[:800]
                }
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Ошибка парсинга: {str(e)}"}
        )
