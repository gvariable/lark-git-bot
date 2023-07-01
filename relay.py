from aiohttp import web
from parse import *
from bot import send_card


async def relay(request: web.Request):
    event = request.headers.get("X-GitHub-Event")
    meta = None
    match event:
        case "push":
            meta = PushPayload(request.json())
        case "pull_request" | "issues":
            meta = InteractivePayload(request.json())
    send_card(meta)
    return web.Response(text="OK")


async def main():
    app = web.Application()
    app.add_routes([web.post("/relay", relay)])
    await web.run_app(app, host="0.0.0.0", port=8080)
