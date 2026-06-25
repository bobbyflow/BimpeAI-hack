#!/usr/bin/env python3
"""
BimpeAI hack-night control script.

Secrets:
  - Reads BIMPE_API_KEY from the environment.
  - Never writes the API key to disk.

Fast path:
  python scripts/bimpe_hack.py list-workflows --search invoice
  python scripts/bimpe_hack.py bootstrap --payment-link "https://buy.stripe.com/test_..."
  python scripts/bimpe_hack.py chat "I got your message. Can I pay tomorrow?"
  python scripts/bimpe_hack.py call +447700900123
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = os.getenv("BIMPE_BASE_URL", "https://api.bimpe.ai/api/v1/console").rstrip("/")
STATE_PATH = Path("bimpe_agent_state.json")


class BimpeError(RuntimeError):
    pass


def require_key() -> str:
    key = os.getenv("BIMPE_API_KEY", "").strip()
    if not key:
        raise BimpeError("Set BIMPE_API_KEY first. Example: $env:BIMPE_API_KEY='sk_...'.")
    if not key.startswith("sk_"):
        raise BimpeError("BIMPE_API_KEY should look like sk_...; event codes are not API keys.")
    return key


def session() -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "POST", "PATCH", "DELETE"]),
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


def request(method: str, path: str, *, body: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
    key = require_key()
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
        "X-Request-Id": f"bimpe-hack-{uuid.uuid4()}",
    }
    if method.upper() in {"POST", "PATCH", "PUT", "DELETE"}:
        headers["Content-Type"] = "application/json"
        headers["Idempotency-Key"] = f"bimpe-hack-{uuid.uuid4()}"

    r = session().request(method, url, headers=headers, json=body, params=params, timeout=30)
    try:
        payload = r.json()
    except Exception:
        payload = {"raw": r.text}
    if r.status_code >= 400:
        raise BimpeError(f"{method} {path} failed [{r.status_code}]: {json.dumps(payload, indent=2)}")
    return payload


def save_state(**updates: Any) -> dict[str, Any]:
    state: dict[str, Any] = {}
    if STATE_PATH.exists():
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    state.update({k: v for k, v in updates.items() if v is not None})
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return state


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        raise BimpeError("No bimpe_agent_state.json yet. Run bootstrap first or pass --agent-id.")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def compact_print(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def revenue_workflow_payload(payment_link: str) -> dict[str, Any]:
    today = "25 June 2026"
    system_prompt = f"""
You are Revenue Recovery Agent for Aperture Studios, a London photography studio.

Mission: recover overdue revenue without damaging the customer relationship.
Tone: concise, warm, professional UK English.
Date context: {today}.

Primary demo customer:
- Customer: Alex Morgan
- Invoice: INV-1042
- Amount: £220
- Status: 14 days overdue
- Service: corporate headshot session
- Payment link: {payment_link}
- Callback calendar: offer today 19:30, tomorrow 10:00, or tomorrow 15:00.

Rules:
1. First identify the customer and overdue invoice.
2. Offer exactly three paths: pay now, schedule a callback, or dispute/escalate.
3. Do not claim payment is complete unless an external payment tool confirms it.
4. If customer says wrong person, financial hardship, fraud, legal issue, anger, or dispute: apologise and escalate to finance@aperture.demo.
5. If customer asks for card/bank details, redirect them to the secure payment link.
6. Close every successful path with the next action and expected timing.
""".strip()

    return {
        "name": "Revenue Recovery Agent — Hack Night",
        "description": "WhatsApp/web/voice agent that recovers overdue invoices, sends payment links, books callbacks, and escalates disputes.",
        "category": "payments",
        "system_prompt": system_prompt,
        "tags": ["hack-night", "revenue-recovery", "invoice", "voice", "whatsapp"],
        "channels": ["webchat", "whatsapp", "telephony"],
        "integrations": ["stripe", "google_calendar"],
        "setup_time": 10,
        "setup_steps": [
            "Create or paste a Stripe test payment link.",
            "Use the test channel link for web/WhatsApp demo.",
            "Optionally place a test outbound call from the API.",
            "Show the conversation log and escalation rule in the demo.",
        ],
        "faq": [
            {
                "question": "What happens if the customer disputes the invoice?",
                "answer": "The agent apologises, captures the reason, and escalates to finance@aperture.demo without pressuring payment.",
            },
            {
                "question": "Can it confirm payment?",
                "answer": "Only after payment-tool confirmation; otherwise it says the link has been sent and the account will update after confirmation.",
            },
        ],
        "rules": [
            {
                "name": "Escalate sensitive cases",
                "trigger": "Customer disputes invoice, claims wrong recipient, mentions fraud/legal issue/hardship, or becomes angry.",
                "condition": "Any high-risk or relationship-sensitive payment case.",
                "response": "Acknowledge, stop collection pressure, summarise the issue, and escalate to finance@aperture.demo.",
                "action": "escalate_to_human",
                "enabled": True,
            }
        ],
        "flows": [
            {
                "name": "Overdue invoice recovery",
                "description": "Collect overdue payment or route to callback/escalation.",
                "category": "payments",
                "priority": 1,
                "is_active": True,
                "trigger_keywords": [
                    {"keyword": "invoice", "weight": "high"},
                    {"keyword": "overdue", "weight": "high"},
                    {"keyword": "payment", "weight": "high"},
                    {"keyword": "callback", "weight": "medium"},
                ],
                "conversation_steps": [
                    {
                        "type": "text_response",
                        "content": "Hi Alex — this is Aperture Studios. Invoice INV-1042 for £220 is 14 days overdue. Would you like to pay securely now, schedule a callback, or raise a query?",
                        "action": "present_recovery_options",
                        "followup": "If they choose pay, send the payment link. If callback, offer slots. If query/dispute, escalate.",
                    },
                    {
                        "type": "text_response",
                        "content": f"Secure payment link: {payment_link}. I’ll mark this as pending until payment confirmation comes through.",
                        "action": "send_payment_link",
                        "followup": "Ask if they need anything else or prefer a callback.",
                    },
                ],
            }
        ],
    }


def kb_content(payment_link: str) -> str:
    return f"""
DEMO DATA — Aperture Studios Revenue Recovery

Customer: Alex Morgan
Phone: use the demo participant phone number
Email: alex@example.demo
Invoice: INV-1042
Amount: £220
Service: corporate headshot session
Due date: 11 June 2026
Current date: 25 June 2026
Status: 14 days overdue
Payment link: {payment_link}

Approved callback slots:
- Today 19:30 Europe/London
- Tomorrow 10:00 Europe/London
- Tomorrow 15:00 Europe/London

Escalation email: finance@aperture.demo

Demo success condition:
The agent should either send the payment link, book a callback slot, or escalate a dispute.
""".strip()


def create_workflow(payment_link: str) -> dict[str, Any]:
    payload = revenue_workflow_payload(payment_link)
    try:
        return request("POST", "/workflows", body=payload)["data"]
    except BimpeError as e:
        print(f"Full workflow payload failed; retrying minimal workflow. Details:\n{e}", file=sys.stderr)
        minimal = {
            "name": payload["name"],
            "description": payload["description"],
            "category": payload["category"],
            "system_prompt": payload["system_prompt"],
        }
        return request("POST", "/workflows", body=minimal)["data"]


def cmd_list_workflows(args: argparse.Namespace) -> None:
    params = {"limit": args.limit, "scope": args.scope}
    if args.search:
        params["search"] = args.search
    data = request("GET", "/workflows", params=params)
    rows = data.get("data", [])
    for row in rows:
        print(f"{row.get('id')} | {row.get('name')} | {row.get('category')} | owner={row.get('is_owner')}")
    if args.json:
        compact_print(data)


def cmd_bootstrap(args: argparse.Namespace) -> None:
    payment_link = args.payment_link
    workflow_id = args.workflow_id

    if not workflow_id:
        print("Creating Revenue Recovery workflow...")
        workflow = create_workflow(payment_link)
        workflow_id = workflow["id"]
    else:
        workflow = request("GET", f"/workflows/{workflow_id}")["data"]

    print(f"Workflow: {workflow_id} — {workflow.get('name')}")

    agent_body = {
        "workflow_id": workflow_id,
        "name": args.agent_name,
        "description": "Hack-night demo agent: overdue invoice recovery across webchat/WhatsApp/voice.",
    }
    agent = request("POST", "/agents", body=agent_body)["data"]
    agent_id = agent["id"]
    print(f"Agent: {agent_id} — {agent.get('name')}")

    patch = {
        "persona": "friendly",
        "timezone": "Europe/London",
        "business_name": "Aperture Studios",
        "business_address": "32-37 Cowper St, London EC2A 4AW",
        "business_email": "finance@aperture.demo",
        "business_description": "Photography studio using AI to recover overdue invoices politely via chat and voice.",
        "escalation_email": "finance@aperture.demo",
    }
    try:
        request("PATCH", f"/agents/{agent_id}", body=patch)
    except BimpeError as e:
        print(f"Non-blocking: agent profile patch failed:\n{e}", file=sys.stderr)

    try:
        kb = request(
            "POST",
            f"/agents/{agent_id}/knowledge_bases",
            body={
                "type": "text",
                "name": "Demo invoice + escalation policy",
                "description": "Single-customer demo dataset for hack-night revenue recovery.",
                "content": kb_content(payment_link),
            },
        )["data"]
        print(f"Knowledge base: {kb.get('id')} — {kb.get('name')}")
    except BimpeError as e:
        print(f"Non-blocking: knowledge base creation failed:\n{e}", file=sys.stderr)

    try:
        request("PATCH", f"/agents/{agent_id}/live-status", body={"status": "live", "status_reason": "Hack-night demo ready"})
    except BimpeError as e:
        print(f"Non-blocking: live-status update failed:\n{e}", file=sys.stderr)

    links = {}
    try:
        links = request("GET", f"/agents/{agent_id}/deployment/agent-test-code")["data"]
        print("Deployment/test links:")
        compact_print(links)
    except BimpeError as e:
        print(f"Non-blocking: test-code retrieval failed:\n{e}", file=sys.stderr)

    state = save_state(agent_id=agent_id, workflow_id=workflow_id, payment_link=payment_link, deployment=links)
    print(f"Saved state: {STATE_PATH.resolve()}")
    compact_print(state)


def resolve_agent_id(args: argparse.Namespace) -> str:
    if args.agent_id:
        return args.agent_id
    return load_state()["agent_id"]


def cmd_get_links(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    data = request("GET", f"/agents/{agent_id}/deployment/agent-test-code")["data"]
    save_state(agent_id=agent_id, deployment=data)
    compact_print(data)


def cmd_chat(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    body = {
        "message": args.message,
        "role": "user",
        "channel_type": args.channel,
        "channel_user_id": args.user_id,
        "channel_username": args.username,
        "is_test_channel": True,
    }
    msg = request("POST", f"/agents/{agent_id}/conversations/messages", body=body)["data"]
    print("Sent message:")
    compact_print(msg)
    print("\nNow run: python scripts/bimpe_hack.py conversations")


def cmd_conversations(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    params = {"limit": args.limit, "is_test_channel": True, "sort": "-updated_at"}
    data = request("GET", f"/agents/{agent_id}/conversations", params=params)
    compact_print(data)


def cmd_messages(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    conversation_id = args.conversation_id
    data = request("GET", f"/agents/{agent_id}/conversations/{conversation_id}/messages", params={"limit": args.limit})
    compact_print(data)


def cmd_call(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    body = {"destination": args.destination, "is_test_call": args.test}
    data = request("POST", f"/agents/{agent_id}/calls", body=body)
    compact_print(data)


def cmd_phone_numbers(args: argparse.Namespace) -> None:
    data = request("GET", "/phone-numbers", params={"limit": args.limit})
    compact_print(data)


def cmd_request_number(args: argparse.Namespace) -> None:
    body = {
        "business_name": "Aperture Studios",
        "intended_use": "Hack-night demo: inbound and outbound AI voice agent for overdue invoice recovery.",
        "region": args.region,
        "agent_count": 1,
        "outbound_minutes": args.outbound_minutes,
    }
    state = STATE_PATH.exists() and load_state() or {}
    if state.get("agent_id"):
        body["submitted_by_agent_id"] = state["agent_id"]
    data = request("POST", "/phone-numbers/request", body=body)
    compact_print(data)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="BimpeAI hack-night API helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("list-workflows")
    w.add_argument("--search", default="")
    w.add_argument("--scope", default="accessible", choices=["accessible", "owned", "public"])
    w.add_argument("--limit", type=int, default=30)
    w.add_argument("--json", action="store_true")
    w.set_defaults(func=cmd_list_workflows)

    b = sub.add_parser("bootstrap")
    b.add_argument("--workflow-id", help="Use an existing/cloned workflow instead of creating one.")
    b.add_argument("--payment-link", default="https://buy.stripe.com/test_demo_payment_link")
    b.add_argument("--agent-name", default=f"Revenue Recovery Agent {time.strftime('%H%M')}")
    b.set_defaults(func=cmd_bootstrap)

    gl = sub.add_parser("links")
    gl.add_argument("--agent-id")
    gl.set_defaults(func=cmd_get_links)

    c = sub.add_parser("chat")
    c.add_argument("message")
    c.add_argument("--agent-id")
    c.add_argument("--channel", default="webchat", choices=["webchat", "whatsapp", "telephony"])
    c.add_argument("--user-id", default=str(uuid.uuid4()))
    c.add_argument("--username", default="Alex Morgan")
    c.set_defaults(func=cmd_chat)

    conv = sub.add_parser("conversations")
    conv.add_argument("--agent-id")
    conv.add_argument("--limit", type=int, default=10)
    conv.set_defaults(func=cmd_conversations)

    m = sub.add_parser("messages")
    m.add_argument("conversation_id")
    m.add_argument("--agent-id")
    m.add_argument("--limit", type=int, default=20)
    m.set_defaults(func=cmd_messages)

    call = sub.add_parser("call")
    call.add_argument("destination", help="E.164 phone number, e.g. +447700900123")
    call.add_argument("--agent-id")
    call.add_argument("--live", dest="test", action="store_false", help="Use live telephony; requires configured live channel.")
    call.set_defaults(test=True, func=cmd_call)

    pn = sub.add_parser("phone-numbers")
    pn.add_argument("--limit", type=int, default=20)
    pn.set_defaults(func=cmd_phone_numbers)

    rn = sub.add_parser("request-number")
    rn.add_argument("--region", default="uk", choices=["us", "uk", "eu", "ng"])
    rn.add_argument("--outbound-minutes", type=int, default=100)
    rn.set_defaults(func=cmd_request_number)

    return p


def main() -> int:
    args = build_parser().parse_args()
    try:
        args.func(args)
        return 0
    except BimpeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
