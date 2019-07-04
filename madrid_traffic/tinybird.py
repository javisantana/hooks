
import csv
from io import StringIO
import requests
from datetime import datetime, date
from enum import Enum
from uuid import UUID

class Datasource:

    def __init__(self, datasource_name, token):
        if not token:
            raise ValueError("token must be valid tinybird token")
        self.token = token
        self.datasource_name = datasource_name
        self.rows = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.flush()

    def __iadd__(self, rows):
        self.rows.append(row)
        return self

    def __lshift__(self, row):
        self.rows.append(row)
        return self

    def header(self, header):
        self.header = header

    def flush(self):
        r = requests.post(
            'https://api.tinybird.co/v0/datasources?mode=append&name=' + self.datasource_name,
            data=csv_from_python_object([self.header] + self.rows),
            headers={
                'Authorization': 'Bearer ' + self.token
            },
            verify=False
        )
        if r.status_code != 200:
            raise Exception(r.json()['error'])

def object_to_csv_string(item):
    if item is None:
        return '\\N'

    elif isinstance(item, datetime):
        return "%s" % item.strftime('%Y-%m-%d %H:%M:%S')

    elif isinstance(item, date):
        return "%s" % item.strftime('%Y-%m-%d')

    elif isinstance(item, list):
        return "[%s]" % ', '.join(text_type(object_to_csv_string(x)) for x in item)

    elif isinstance(item, tuple):
        return "(%s)" % ', '.join(text_type(object_to_csv_string(x)) for x in item)

    elif isinstance(item, Enum):
        return escape_param(item.value)

    elif isinstance(item, UUID):
        return "%s" % str(item)
    else:
        return item
    """
    elif isinstance(item, string_types):
        return "'%s'" % ''.join(escape_chars_map.get(c, c) for c in item)
    """

def csv_from_python_object(rows):
    """
    generates csv from a list of python objects
    >>> csv_from_python_object([[datetime(2018, 9, 7, 23, 50), date(2019, 9, 7), 'tes"t', 123.0, None, 3]])
    '2018-09-07 23:50:00,2019-09-07,"tes""t",123.0,\\\\N,3\\r\\n'
    """
    csv_chunk = StringIO()
    w = csv.writer(csv_chunk, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerows([map(object_to_csv_string, x) for x in rows])
    return csv_chunk.getvalue()
