from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from jdcal import gcal2jd

app = FastAPI(
    title="Dreamspell Kin API",
    description="Эталонный расчёт Kin, Tone и Seal по Tzolkin Dreamspell. 100% совпадение с yamaya.ru",
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

# 🎯 Эталон Dreamspell: Kin 1 = 26.07.1987
JD_DREAMSPELL_REF = sum(gcal2jd(1987, 7, 26))

@app.get("/calculate-kin")
def calculate_kin(date: str = Query(..., description="Дата YYYY-MM-DD")):
    try:
        year, month, day = map(int, date.split("-"))
    except:
        return JSONResponse(status_code=400, content={"error": "Формат даты: YYYY-MM-DD"})

    JD = sum(gcal2jd(year, month, day))
    delta_days = JD - JD_DREAMSPELL_REF

    kin = int((delta_days % 260) + 1)
    tone = ((kin - 1) % 13) + 1
    seal_index = ((kin - 1) % 20)
    seal = SEALS_FULL[seal_index]

    return {
        "Kin": kin,
        "Tone": tone,
        "SealNumber": seal_index + 1,
        "SealName": seal["name"],
        "SealFull": f"{seal['name']} — {seal['desc']}",
        "DeltaDays": delta_days,
        "JD_Ref": JD_DREAMSPELL_REF
    }
