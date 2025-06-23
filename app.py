import asyncio
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright

app = FastAPI(
    title="Kin Proxy — через реальный браузер Playwright",
    description="Открывает yamaya.ru как человек, заполняет форму, ждёт расчёт и возвращает JSON.",
    version="1.0.0"
)

@app.get("/calculate-kin")
async def calculate_kin(date: str = Query(..., description="Дата YYYY-MM-DD")):
    try:
        year, month, day = date.split("-")
    except:
        return JSONResponse(status_code=400, content={"error": "Неверный формат YYYY-MM-DD"})

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://yamaya.ru/maya/choosedate/")

        # Заполняем форму как человек
        await page.fill('input[name="formday"]', day)
        await page.fill('input[name="formmonth"]', month)
        await page.fill('input[name="formyear"]', year)

        # Нажимаем submit
        await page.click('input[type="submit"]')

        await page.wait_for_timeout(1000)  # дать серверу обработать

        text = await page.content()

        await browser.close()

    # Парсим Kin, Tone, Seal из HTML
    soup = BeautifulSoup(text, "html.parser")
    all_text = soup.get_text(separator="\n")
    kin = tone = seal = None
    for line in all_text.splitlines():
        if line.strip().startswith("Кин:"):
            kin = line.replace("Кин:", "").strip()
        elif line.strip().startswith("Тон:"):
            tone = line.replace("Тон:", "").strip()
        elif line.strip().startswith("Печать:"):
            seal = line.replace("Печать:", "").strip()

    if kin and tone and seal:
        return {"Kin": kin, "Tone": tone, "Seal": seal}
    else:
        return {"error": "Не удалось распарсить", "debug": all_text[:500]}
