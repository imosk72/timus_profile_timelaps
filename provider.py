from timus_parser import parse_tasks, parse_user_attempts
from task_verdict import TaskVerdict
from copy import deepcopy


class TaskProvider:

    def __init__(self):
        self.tasks = None

    def get_all(self, locale='en'):
        if self.tasks is None:
            tasks = {}
            for task in sorted(parse_tasks(locale), key=lambda task: task.difficulty):
                tasks[task.number] = {}
                tasks[task.number]['number'] = task.number
                tasks[task.number]['title'] = task.name
                tasks[task.number]['verdict'] = TaskVerdict.EMPTY
            self.tasks = tasks
        return self.tasks


class AttemptProvider:

    def get_tasks_by_profile_id(self, tasks, profile_id, date):
        profile_tasks = deepcopy(tasks)
        for attempt in parse_user_attempts(profile_id):
            if attempt.date <= date:
                if attempt.verdict == 'accepted':
                    profile_tasks[attempt.task_number]['verdict'] = TaskVerdict.ACCEPTED
                elif profile_tasks[attempt.task_number]['verdict'] != TaskVerdict.ACCEPTED:
                    profile_tasks[attempt.task_number]['verdict'] = TaskVerdict.TRIED
        return profile_tasks