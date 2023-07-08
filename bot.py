import time
from jinja2 import Environment, FileSystemLoader
import hashlib
import base64
import hmac
import json
import aiohttp


env = Environment(loader=FileSystemLoader("./"))
template = env.get_template("template.json")


def gen_sign(secret, timestamp):
    s = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(s.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


async def send_card(meta, webhook, secret):
    # TODO(gpl): handle another case if secret is not provided
    timestamp = int(time.time())
    sign = gen_sign(timestamp, secret)

    data = {
        "timestamp": str(timestamp),
        "sign": sign,
        "msg_type": "interactive",
        "card": json.loads(template.render(meta=meta), strict=False),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=webhook, json=data) as resp:
            data = await resp.json()
            if data["code"] != 0:
                raise Exception(data["msg"])
