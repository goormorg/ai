from typing import Union
from fastapi import FastAPI
import os
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



client = OpenAI(
    api_key= os.environ["OPENAI_API_KEY"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get")
def read_root(gender: str, age: str, weight: str, muscle: str, goal: str):
    result = ''

    stream = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": """성별, 나이, 몸무게, 키, 골격근량, 목표를 입력하면, 너는 아침, 점심, 저녁에 해당하는 메뉴를 {{ 아침: 메뉴 배열, 점심: 메뉴 배열, 저녁: 메뉴 배열 }} JSON 형식으로 추천해줘.

성별={gender}, 나이={age}, 몸무게={weight}, 골격근량={muscle}, 목표={goal}""".format(gender=gender,age=age,weight=weight,muscle=muscle,goal=goal),
            }
        ],
        model="gpt-3.5-turbo",
        stream=True,

    )

    for chunk in stream:
        result += chunk.choices[0].delta.content or ""

    return {
        "result": result
    }


@app.get("/get/more")
def read_root(gender: str, age: str, weight: str, muscle: str, goal: str):
    result = ''

    stream = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": """성별, 나이, 몸무게, 키, 골격근량, 목표를 입력하면, 너는 아침, 점심, 저녁에 해당하는 메뉴와 각 메뉴에 해당하는 영양소를 {{ 아침: {{ 메뉴: 메뉴배열, 영양소: {{ 칼로리, 탄수화물, 단백질, 지방, 당류, 포화지방, 나트륨, 칼슘 }} }}, 점심: {{ 메뉴: 메뉴배열, 영양소: {{ 칼로리, 탄수화물, 단백질, 지방, 당류, 포화지방, 나트륨, 칼슘 }} }}, 저녁: {{ 메뉴: 메뉴배열, 영양소: {{ 칼로리, 탄수화물, 단백질, 지방, 당류, 포화지방, 나트륨, 칼슘 }} }} }} JSON 형식으로 추천해줘.

성별={gender}, 나이={age}, 몸무게={weight}, 골격근량={muscle}, 목표={goal}""".format(gender=gender,age=age,weight=weight,muscle=muscle,goal=goal),
            }
        ],
        model="gpt-3.5-turbo",
        stream=True,

    )

    for chunk in stream:
        result += chunk.choices[0].delta.content or ""

    return {
        "result": result
    }