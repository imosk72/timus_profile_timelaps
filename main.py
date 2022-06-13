from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from enum import Enum
from datetime import datetime
from provider import TaskProvider, AttemptProvider

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

task_provider = TaskProvider()
attempt_provider = AttemptProvider()


@app.get("/profile/{id}", response_class=HTMLResponse)
async def get_profile(request: Request, id: int, date: datetime = datetime.now()):
    tasks = task_provider.get_all()
    profile_tasks = attempt_provider.get_tasks_by_profile_id(tasks, id, date)
    return templates.TemplateResponse("profile.html", {"request": request, "id": id, "tasks": profile_tasks.values()})
