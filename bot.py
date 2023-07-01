import time
from jinja2 import Environment, FileSystemLoader
import hashlib
import base64
import hmac
from dotenv import dotenv_values
import json
import aiohttp


CONFIG = dotenv_values(".env")
env = Environment(loader=FileSystemLoader("./"))
template = env.get_template("template.json")


def gen_sign(timestamp):
    s = f"{timestamp}\n{CONFIG['SECRET']}"
    hmac_code = hmac.new(s.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


async def send_card(meta):
    url = CONFIG["WEBHOOK"]
    timestamp = int(time.time())
    sign = gen_sign(timestamp)

    data = {
        "timestamp": str(timestamp),
        "sign": sign,
        "msg_type": "interactive",
        "card": json.loads(template.render(meta=meta)),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data) as resp:
            data = await resp.json()
            if data["code"] != 0:
                raise Exception(data["msg"])
