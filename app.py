from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from jdcal import gcal2jd  # julian day calc

app = FastAPI(
    title="Kin Calculator API — Точное совпадение с yamaya.ru",
    description="Считает Kin, Tone и Seal по Tzolkin на основе астрономического Julian Day.",
    version="1.0.0"
)

SEALS_FULL = [
    {'name': 'Красный Дракон', 'desc': 'рождение, питание, начало, материнство'},
    {'name': 'Белый Ветер', 'desc': 'дух, общение, вдохновение, истина'},
    {'name': 'Синяя Ночь', 'desc': 'сновидение, интуиция, изобилие, подсознание'},
    {'name': 'Жёлтое Семя', 'desc': 'рост, развитие, осознанность, цветение'},
    {'name': 'Красная Змея', 'desc': 'жизненная сила, инстинкт, сексуальность, выживание'},
    {'name': 'Белый Соединитель Миров', 'desc': 'сочувствие, порядок, равновесие, справедливость'},
    {'name': 'Синяя Рука', 'desc': 'исцеление, исполнение, знание, завершение'},
    {'name': 'Жёлтая Звезда', 'desc': 'красота, искусство, гармония, элегантность'},
    {'name': 'Красная Луна', 'desc': 'очищение, поток, универсальная вода, движение эмоций'},
    {'name': 'Белая Собака', 'desc': 'любовь, верность, сердце, преданность'},
    {'name': 'Синяя Обезьяна', 'desc': 'игра, магия, спонтанность, юмор'},
    {'name': 'Жёлтый Человек', 'desc': 'свобода воли, влияние, мудрость, зрелость'},
    {'name': 'Красный Небесный Странник', 'desc': 'пространство, исследование, пробуждение'},
    {'name': 'Белый Волшебник', 'desc': 'временная магия, очарование, открытость'},
    {'name': 'Синий Орёл', 'desc': 'видение, творчество, разум, проницательность'},
    {'name': 'Жёлтый Воин', 'desc': 'вопросы, интеллект, смелость, храбрость'},
    {'name': 'Красная Земля', 'desc': 'эволюция, синхронность, навигация'},
    {'name': 'Белое Зеркало', 'desc': 'отражение, порядок, бесконечность, истина'},
    {'name': 'Синяя Буря', 'desc': 'катализатор, самообновление, энергия, трансформация'},
    {'name': 'Жёлтое Солнце', 'desc': 'просветление, универсальный огонь, жизнь, любовь'}
]

# Фиксированная опорная дата: 26 июля 1853 — как в yamaya.ru
JD_REF = sum(gcal2jd(1853, 7, 26))  # Julian Day Number

@app.get("/calculate-kin")
def calculate_kin(date: str = Query(..., description="Дата рождения в формате YYYY-MM-DD")):
    try:
        birth_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Неверный формат даты. Используй YYYY-MM-DD."}
        )

    jd_birth = sum(gcal2jd(birth_date.year, birth_date.month, birth_date.day))
    delta_days = int(jd_birth - JD_REF)

    kin = ((delta_days % 260) + 1)
    tone = ((kin - 1) % 13) + 1
    seal_index = ((kin - 1) % 20)
    seal_data = SEALS_FULL[seal_index]
    seal_number = seal_index + 1
    seal_name = seal_data["name"]
    seal_full = f"{seal_name} — {seal_data['desc']}"

    return {
        "Kin": kin,
        "Tone": tone,
        "SealNumber": seal_number,
        "SealName": seal_name,
        "SealFull": seal_full,
        "Delta": delta_days
    }
