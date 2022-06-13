import datetime


class Attempt:
    def __init__(self, attempt_id: int, date: datetime, author: str, task_number: int, verdict: str):
        self.attempt_id = attempt_id
        self.date = date
        self.author = author
        self.task_number = task_number
        self.verdict = verdict
