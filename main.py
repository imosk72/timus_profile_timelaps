from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from enum import Enum
from typing import Optional
from datetime import datetime
import handler
import timus_parser

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TaskVerdict(Enum):
    ACCEPTED = 'accepted'
    TRIED = 'tried'
    EMPTY = 'empty'


@app.get("/profile/{id}", response_class=HTMLResponse)
async def get_profile(request: Request, id: int, date: Optional[datetime] = datetime.now()):
    tasks = handler.generate_json(177044, date)
    return templates.TemplateResponse("profile.html", {"request": request, "id": id, "tasks": tasks.values()})
