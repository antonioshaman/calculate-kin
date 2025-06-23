from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from jdcal import gcal2jd

app = FastAPI(
    title="Kin Calculator API — чистый JD",
    description="Честный и автономный расчёт Kin, Tone и Seal без парсинга сайтов.",
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

# Эталонный JD для 26.07.1853 = Kin 1
JD_REF = sum(gcal2jd(1853, 7, 26))

@app.get("/calculate-kin")
def calculate_kin(date: str = Query(..., description="Дата рождения YYYY-MM-DD")):
    try:
        year, month, day = map(int, date.split("-"))
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Формат даты должен быть YYYY-MM-DD"}
        )

    JD = sum(gcal2jd(year, month, day))
    delta = int(JD - JD_REF)

    kin = (delta % 260) + 1
    tone = ((kin - 1) % 13) + 1
    seal_index = ((kin - 1) % 20)
    seal_data = SEALS_FULL[seal_index]

    return {
        "Kin": kin,
        "Tone": tone,
        "SealNumber": seal_index + 1,
        "SealName": seal_data["name"],
        "SealFull": f"{seal_data['name']} — {seal_data['desc']}",
        "Delta": delta
    }
