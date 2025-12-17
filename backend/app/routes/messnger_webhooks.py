from fastapi import APIRouter, Request, Response

VERIFY_TOKEN = "fasgbngdfgshgshfgdgzgxfn855"

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(request: Request):
    q = request.query_params
    mode = q.get("hub.mode")
    token = q.get("hub.verify_token")
    challenge = q.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN and challenge:
        return Response(content=challenge, media_type="text/plain", status_code=200)

    return Response(status_code=403)

@router.post("/webhook")
async def receive_webhook(request: Request):
    _ = await request.json()
    return Response(status_code=200)
