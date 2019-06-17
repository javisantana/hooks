

import requests
import json
import sys
import itertools


def hook(tinyb_token, telegram_bot, telegram_channel):
    Q = """
    with 
    (
        select uniq(user_id) unique_users_yesterday from tracker where toDate(timestamp) > yesterday()
    ) as unique_users_yesterday,
    (
        select uniq(user_id) unique_users_yesterday from tracker where toDate(timestamp) < yesterday()
    ) as unique_users_all_time,
    (
        select count() a from tracker where toDate(timestamp) > yesterday() and attr3 = 'Run with error'
    ) as run_with_error,
    (
        select count() a from tracker where toDate(timestamp) > yesterday() and attr2 = 'Query'
    ) as total_queries,
    (
        select count() a from tracker where toDate(timestamp) < yesterday() and attr3 = 'Run with error'
    ) as run_with_error_at,
    (
        select count() a from tracker where toDate(timestamp) < yesterday() and attr2 = 'Query'
    ) as total_queries_at
    select 
        unique_users_yesterday users__unique_users_yesterday,
        unique_users_all_time users__unique_users_all_time,
        run_with_error query__run_with_error,
        total_queries  query__total_queries,
        run_with_error_at query__run_with_error_all_time,
        total_queries_at query__total_queries_all_time
    FORMAT JSON"""
    r = requests.get(f"https://api.tinybird.co/v0/sql?q={Q}&token={tinyb_token}", verify=False).json()
    report_data = r['data'][0]
    time = r['statistics']['elapsed']

    # generate the report
    text = []
    text.append(f"{'** TINYBIRD DAILY **':^35}")
    text.append('\n')
    for group, items in itertools.groupby([x.split('__') + [report_data[x]] for x in report_data.keys()], key=lambda x: x[0]):
        group = group.upper()
        text.append(f"{group:^35}")
        #text.append('\n')
        for g, name, value in items:
            name = name.replace('_', ' ')
            pad = '.' * (35 - len(name) - len(str(value)) - 2)
            text.append(f"{name} {pad} {value}")
        text.append('\n')
    end = f"END ({time:f}ms)"
    text.append(f"{end:^35}")

    #send to telegram
    html_text = '<pre>'  + '\n'.join(text) + '</pre>'
    requests.get(f'https://api.telegram.org/bot{telegram_bot}/sendMessage?chat_id={telegram_channel}&text={html_text}&parse_mode=HTML')


TINYB_TOKEN = sys.argv[1]
TELEGRAM_BOT = sys.argv[2]
TELEGRAM_CHANNEL = sys.argv[3]
hook(TINYB_TOKEN, TELEGRAM_BOT, TELEGRAM_CHANNEL)





