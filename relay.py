from aiohttp import web
from parse import *
from bot import send_card
import argparse
import os


async def relay(request: web.Request):
    event = request.headers.get("X-GitHub-Event")
    data = await request.json()
    meta = None
    match event:
        case "push":
            meta = PushPayload(data)
        case "pull_request" | "issues":
            meta = InteractivePayload(event, data)
    print(meta)
    await send_card(meta, os.environ.get("WEBHOOK"), os.environ.get("SECRET"))
    return web.Response(text="OK")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    if os.environ.get("WEBHOOK") is None:
        from dotenv import load_dotenv

        if not load_dotenv(".env"):
            # TODO(gpl): error handling
            ...

    app = web.Application()
    app.add_routes([web.post("/relay", relay)])
    web.run_app(app, host="0.0.0.0", port=args.port)
