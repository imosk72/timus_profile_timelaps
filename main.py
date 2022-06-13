import parser

if __name__ == '__main__':
    for attempt in parser.parse_user_attempts(221703):
        print(attempt.id, attempt.date, attempt.author, attempt.task_number, attempt.verdict)
