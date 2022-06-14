import requests
import re
import dateparser
from attempt import Attempt
from task import Task
from functools import lru_cache


def get_attempts_from_page(page):
    strings = [t[0] + t[1] for t in re.findall(r'<tr class=\"even\">(.*?)</tr>|<tr class=\"odd\">(.*?)</tr>', page.lower())]
    attempts = list()
    for string in strings:
        attempt_id = re.findall(r'<td class=\"id\"><a.*?>(.*?)</a></td>', string)[0]
        time = re.findall(r'<td class=\"date\"><nobr>(.*?)</nobr>', string)[0]
        date = re.findall(r'<td class=\"date\"><nobr>.*?</nobr><br><nobr>(.*?)</nobr>', string)[0]
        author = re.findall(r'<td class=\"coder\"><a.*?>(.*?)</a></td>', string)[0]
        task_number = re.findall(r'<td class=\"problem\"><a.*?>(.*?)<span', string)[0]
        verdict = re.findall(r'<td class=\"verdict_.*?\">(.*?)</td>', string)[0]
        if not task_number.isdigit():
            link = 'https://acm.timus.ru/' + re.findall(r'<td class=\"problem\"><a href=\"(.*?)\">', string)[0].replace('amp;', '')
            task_page = requests.get(link).text.lower()
            print(task_page)
            task_name = re.findall(r'to submit the solution for this problem go to the problem set: <a .*?><nobr>(.*?)</nobr>', task_page)[0]
            task_number = task_name.split('.')[0]

        attempts.append(Attempt(int(attempt_id), dateparser.parse(date + ' ' + time), author, int(task_number), verdict))

    return attempts


@lru_cache
def parse_user_attempts(user_id):
    attempts = list()
    attempts += get_attempts_from_page(requests.get(f'https://acm.timus.ru/status.aspx?author={user_id}&locale=en&count=1000').text)
    if not attempts:
        return []
    while True:
        new_attempts = get_attempts_from_page(requests.get(f'https://acm.timus.ru/status.aspx?author={user_id}&locale=en&count=1000&from={attempts[-1].id - 1}').text)
        if not new_attempts:
            break
        else:
            attempts += new_attempts
    return attempts


def parse_tasks(locale='en'):
    tasks = list()
    page = requests.get(f'https://acm.timus.ru/problemset.aspx?space=1&page=all&locale={locale}').text
    for tr in re.findall(r'<tr class=\"content\">(.*?)</tr>', page.lower())[1:]:
        [number, difficulty] = re.findall(r'<td>(\d+)</td>', tr)
        name = re.findall(r'<td class=\"name\"><a.*?>(.*?)</a></td>', tr)[0]
        tasks.append(Task(int(number), name, int(difficulty)))
    return tasks


