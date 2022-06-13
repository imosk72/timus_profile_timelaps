import requests
import re
import datetime
import dateparser
from attempt import Attempt


def get_attempts_from_page(page):
    strings = [t[0] + t[1] for t in re.findall(r'<TR class=\"even\">(.*?)</TR>|<TR class=\"odd\">(.*?)</TR>', page)]
    attempts = list()
    for string in strings:
        attempt_id = re.findall(r'<TD class=\"id\"><A.*?>(.*?)</A></TD>', string)[0]
        time = re.findall(r'<TD class=\"date\"><NOBR>(.*?)</NOBR>', string)[0]
        date = re.findall(r'<TD class=\"date\"><NOBR>.*?</NOBR><BR><NOBR>(.*?)</NOBR>', string)[0]
        author = re.findall(r'<TD class=\"coder\"><A.*?>(.*?)</A></TD>', string)[0]
        task_number = re.findall(r'<TD class=\"problem\"><A.*?>(.*?)<SPAN', string)[0]
        verdict = re.findall(r'<TD class=\"verdict_.*?\">(.*?)</TD>', string)[0]
        if task_number.isdigit():
            attempts.append(Attempt(int(attempt_id), dateparser.parse(date + ' ' + time), author, int(task_number), verdict))
    return attempts


def parse_user_attempts(user_id):
    attempts = list()
    attempts += get_attempts_from_page(requests.get(f'https://acm.timus.ru/status.aspx?author={user_id}&locale=en&count=1000').text)
    while True:
        new_attempts = get_attempts_from_page(requests.get(f'https://acm.timus.ru/status.aspx?author={user_id}&locale=en&count=1000&from={attempts[-1].attempt_id - 1}').text)
        print(len(new_attempts))
        if len(new_attempts) == 0:
            break
        else:
            attempts += new_attempts

    print(len(attempts))
