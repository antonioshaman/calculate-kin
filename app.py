from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(
    title="Mayan Calendar API — Long Count + Tzolkin",
    description="Честный и традиционный расчёт Mayan Long Count и Tzolkin Kin.",
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

# Mayan Long Count стартует 11 августа 3114 BCE (GMT correlation)
MAYAN_EPOCH = datetime(-3113, 8, 11)  # в Python нет года 0, поэтому -3113

@app.get("/calculate-kin")
def calculate_kin(date: str = Query(..., description="Дата YYYY-MM-DD")):
    try:
        year, month, day = map(int, date.split("-"))
        date_obj = datetime(year, month, day)
    except:
        return JSONResponse(status_code=400, content={"error": "Формат даты: YYYY-MM-DD"})

    # Разница дней с эпохой
    delta_days = (date_obj - MAYAN_EPOCH).days

    # Long Count
    baktun = delta_days // 144000
    katun = (delta_days % 144000) // 7200
    tun = (delta_days % 7200) // 360
    uinal = (delta_days % 360) // 20
    kin_long = delta_days % 20

    long_count = f"{baktun}.{katun}.{tun}.{uinal}.{kin_long}"

    # Tzolkin
    kin = (delta_days % 260) + 1
    tone = ((kin - 1) % 13) + 1
    seal_index = ((kin - 1) % 20)
    seal_data = SEALS_FULL[seal_index]

    return {
        "LongCount": long_count,
        "Kin": kin,
        "Tone": tone,
        "SealNumber": seal_index + 1,
        "SealName": seal_data["name"],
        "SealFull": f"{seal_data['name']} — {seal_data['desc']}",
        "DeltaDays": delta_days
    }
