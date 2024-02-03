from fastapi import FastAPI
from question import Question
# from serializer import QuestionJSONEncoder
import json

app = FastAPI()


def to_json(q: Question):
    def rec(q: Question):
        obj = {
            "question": q.question,
            "is_atomic": q.is_atomic(),
            "answer": q.answer,
            "subquestions": [rec(sq) for sq in q.subqs]
        }
        return obj
    return rec(q)


@app.get("/query/{query}")
async def answer(query):
    q = Question(query)
    q.get_answer()
    return to_json(q)


