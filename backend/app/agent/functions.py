from __future__ import annotations

import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.tools import TOOLS
from core.config import SYSTEM_PROMPT ,GOOGLE_API_KEY
from core.database import SessionLocal
from services.client import get_or_create_client
from services.message import get_recent_messages_chronological, log_message
import time

class Generate_Response_Exception(Exception):
    pass


tool_map = {t.name: t for t in TOOLS}
def _execute_tool_call(call: dict) -> str:
    name = call["name"]
    args = call.get("args") or {}

    
    if name not in tool_map:
        return json.dumps({"error": f"unknown tool {name}"}, ensure_ascii=False)

    out = tool_map[name].invoke(args)
    return out if isinstance(out, str) else json.dumps(out, ensure_ascii=False)


def generate_response(sender_psid: str, text: str) -> str:
    db = SessionLocal()
    try:
        client = get_or_create_client(db=db, messenger_psid=sender_psid)

        history = get_recent_messages_chronological(db=db, client_id=client.id, limit=20)

        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        for m in history:
            if m.direction == "in":
                messages.append(HumanMessage(content=m.content or ""))
            elif m.direction == "out":
                messages.append(AIMessage(content=m.content or ""))

        messages.append(HumanMessage(content=text))


        for _ in range(4):
            # try calling the llm up to 3 times 
            iter = 0
            while iter<3:
                try:
                    ai_response = invoke_llm(messages)
                except Generate_Response_Exception as e:
                    print(e)
                    print("trying again in 1 sec")
                    time.sleep(1)
                    iter+=1
            if iter==3:
                raise Generate_Response_Exception("tool loop exceeded")


            tool_calls = getattr(ai_response, "tool_calls", None) or []
            if not tool_calls:
                content = getattr(ai_response, "content", "")

                if isinstance(content, str):
                    reply = content.strip()

                elif isinstance(content, list):
                    parts: list[str] = []
                    for c in content:
                        if isinstance(c, str):
                            parts.append(c)
                        elif isinstance(c, dict):
                            t = c.get("text")
                            if isinstance(t, str):
                                parts.append(t)
                        else:
                            t = getattr(c, "text", None)
                            if isinstance(t, str):
                                parts.append(t)
                    reply = "\n".join(p.strip() for p in parts if p and p.strip()).strip()

                elif isinstance(content, dict):
                    reply = str(content.get("text", "")).strip()

                else:
                    t = getattr(content, "text", None)
                    reply = str(t).strip() if isinstance(t, str) else ""


                log_message(db, client_id=client.id, direction="in", content=text)
                log_message(db, client_id=client.id, direction="out", content=reply)

                return reply

            messages.append(ai_response)

            for call in tool_calls:
                result = _execute_tool_call(call)
                messages.append(ToolMessage(content=result, tool_call_id=call["id"]))

        raise RuntimeError("tool loop exceeded")
    except Exception as e:
        print(e)
        return "Sorry, issue handeling response , will get back to you soon"
    finally:
        db.close()

def invoke_llm(messages: list[HumanMessage | AIMessage | SystemMessage]) :

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, api_key = GOOGLE_API_KEY).bind_tools(TOOLS)
    return llm(messages=messages).invoke()
