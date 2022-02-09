import os

import requests


WECOMCHAN_SENDKEY = os.environ["WECOMCHAN_SENDKEY"]


def send_wecomchan(msg):
    r = requests.post(
        "https://worker.wing2south.com/wecomchan/",
        json={
            "sendkey": WECOMCHAN_SENDKEY,
            "msg": msg,
        },
    )
    r.raise_for_status()
