#!/usr/bin/env python

"""
make_time.py

simple script that returns and HTML page with the current time
"""

import datetime


def make_time():
    time_str = datetime.datetime.now().isoformat()

    html = """
    <http>
    <body>
    <h2> The time is: </h2>
    <p> %s <p>
    </body>
    </http>
    """ % time_str

    return html
