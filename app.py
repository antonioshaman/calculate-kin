from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI(
    title="Kin Proxy API (yamaya.ru парсер)",
    description="Парсит Kin, Tone и Seal напрямую с yamaya.ru с реальным User-Agent.",
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

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return JSONResponse(
            status_code=500,
            content={"error": f"yamaya.ru не ответил. Код: {r.status_code}"}
        )

    soup = BeautifulSoup(r.text, "html.parser")

    # Визуально проверено: контент лежит внутри <div class="pageContent">
    try:
        main_div = soup.find("div", {"class": "pageContent"})
        if not main_div:
            return JSONResponse(
                status_code=500,
                content={"error": "Не найден блок с результатом (pageContent) на yamaya.ru"}
            )

        text = main_div.get_text(separator="\n").strip()
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
                "source": url
            }
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Не удалось распарсить результат. Найдено: Kin={kin}, Tone={tone}, Seal={seal}",
                    "debug_html_sample": text[:500]  # чтобы ты видел кусок HTML!
                }
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Ошибка парсинга: {str(e)}"}
        )
