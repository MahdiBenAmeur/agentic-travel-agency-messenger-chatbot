from __future__ import annotations

import os

import requests
from fastapi import APIRouter, Request, Response

VERIFY_TOKEN = "fasgbngdfgshgshfgdgzgxfn855"

router = APIRouter()


def extract_message_event(payload: dict) -> tuple[str, str] | None:
    if payload.get("object") != "page":
        return None

    entries = payload.get("entry") or []
    for entry in entries:
        messaging = entry.get("messaging") or []
        for ev in messaging:
            msg = ev.get("message") or {}
            text = msg.get("text")
            sender = (ev.get("sender") or {}).get("id")
            if sender and isinstance(text, str):
                return sender, text

    return None


def _post_to_messenger(payload: dict) -> None:
    token = os.getenv("PAGE_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("PAGE_ACCESS_TOKEN is missing")

    url = "https://graph.facebook.com/v20.0/me/messages"
    params = {"access_token": token}

    r = requests.post(url, params=params, json=payload, timeout=15)
    if not r.ok:
        raise RuntimeError(f"Messenger send failed: {r.status_code} {r.text}")

def send_mark_seen(*, recipient_psid: str) -> None:
    _post_to_messenger(
        {
            "recipient": {"id": recipient_psid},
            "sender_action": "mark_seen",
        }
    )


def send_typing_on(*, recipient_psid: str) -> None:
    _post_to_messenger(
        {
            "recipient": {"id": recipient_psid},
            "sender_action": "typing_on",
        }
    )


def send_typing_off(*, recipient_psid: str) -> None:
    _post_to_messenger(
        {
            "recipient": {"id": recipient_psid},
            "sender_action": "typing_off",
        }
    )


def send_text_message(*, recipient_psid: str, text: str) -> None:
    _post_to_messenger(
        {
            "recipient": {"id": recipient_psid},
            "message": {"text": text},
            "messaging_type": "RESPONSE",
        }
    )


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
    payload = await request.json()

    extracted = extract_message_event(payload)
    if not extracted:
        return Response(status_code=200)

    sender_psid, text = extracted
    send_mark_seen(recipient_psid=sender_psid)
    send_typing_on(recipient_psid=sender_psid)
    response = generate_response(sender_psid,text)
    send_text_message(recipient_psid=sender_psid, text=response)
    send_typing_off(recipient_psid=sender_psid)

    return Response(status_code=200)
