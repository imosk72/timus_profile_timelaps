from enum import Enum


class TaskVerdict(Enum):
    ACCEPTED = 'accepted'
    TRIED = 'tried'
    EMPTY = 'empty'
