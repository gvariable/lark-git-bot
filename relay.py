from aiohttp import web
from parse import *
from bot import send_card


async def relay(request: web.Request):
    event = request.headers.get("X-GitHub-Event")
    data = await request.json()
    meta = None
    match event:
        case "push":
            meta = PushPayload(data)
        case "pull_request" | "issues":
            meta = InteractivePayload(event, data)
    await send_card(meta)
    return web.Response(text="OK")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.post("/relay", relay)])
    web.run_app(app, host="0.0.0.0", port=8080)
