from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from enum import Enum
import handler
import parser
import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TaskVerdict(Enum):
    ACCEPTED = 'accepted'
    TRIED = 'tried'
    EMPTY = 'empty'


@app.get("/profile/{id}", response_class=HTMLResponse)
async def get_profile(request: Request, id: int):
    tasks = handler.generate_json(177044, datetime.datetime.now())
    tasks_mock = {
            1001: {
                "number": 1001,
                "title": 'Задача 1001',
                "verdict": TaskVerdict.ACCEPTED
            },
            1293: {
                "number": 1293,
                "title": 'Задача 1293',
                "verdict": TaskVerdict.ACCEPTED
            },
            1298: {
                "number": 1298,
                "title": 'Задача 1298',
                "verdict": TaskVerdict.TRIED
            },
            1299: {
                "number": 1299,
                "title": 'Задача 1299',
                "verdict": TaskVerdict.EMPTY
            },
        }
    return templates.TemplateResponse("profile.html", {"request": request, "id": id, "tasks": tasks_mock.values()})
