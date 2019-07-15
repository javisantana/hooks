

import requests
import json
import sys
import itertools


def hook(tinyb_token, telegram_bot, telegram_channel):
    r = requests.get(f"https://api.tinybird.co/v0/pipes/telegram_bot_daily.json?token={tinyb_token}").json()
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





