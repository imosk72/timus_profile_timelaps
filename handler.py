import timus_parser
from taskVerdict import TaskVerdict


def generate_json(user_id, date, locale='en'):
    tasks = {}
    for task in timus_parser.parse_tasks(locale):
        tasks[task.number] = {}
        tasks[task.number]['number'] = task.number
        tasks[task.number]['title'] = task.name
        tasks[task.number]['verdict'] = TaskVerdict.EMPTY

    for attempt in timus_parser.parse_user_attempts(user_id):
        if attempt.date <= date:
            if attempt.verdict == 'accepted':
                tasks[attempt.task_number]['verdict'] = TaskVerdict.ACCEPTED
            elif tasks[attempt.task_number]['verdict'] != TaskVerdict.ACCEPTED:
                tasks[attempt.task_number]['verdict'] = TaskVerdict.TRIED
    return tasks

