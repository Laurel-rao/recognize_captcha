import time
import uuid
from random import random

import requests


def download():
    resp = requests.get("https://app.huawei.com/escpportal/servlet/identifying", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"})
    data = resp.content
    with open("./huawei_image/%s.jpg" % uuid.uuid4().hex, "wb") as ff:
        ff.write(data)


if __name__ == '__main__':
    step = 1
    while True:
        time.sleep(random() * 15)
        try:
            download()
        except Exception as e:
            print("Error %s" % e)
        else:
            print("Success %s " % step)
            step += 1
        if step > 10000:
            break