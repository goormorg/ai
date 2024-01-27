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
def read_root():
    result = ''

    stream = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "hello. tell me a introduce your self.",
            }
        ],
        model="gpt-3.5-turbo",
        stream=True,

    )

    for chunk in stream:
        result += chunk.choices[0].delta.content or ""

    print(result)
    return {
        "result": result
    }