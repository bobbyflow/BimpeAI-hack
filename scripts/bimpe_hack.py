#!/usr/bin/env python3
"""
BimpeAI Fraud Alert Verification Agent helper.

Purpose:
  Create/test a fraud-track BimpeAI agent from your own IDE/terminal.

Secrets:
  - Reads BIMPE_API_KEY from the environment.
  - Never writes the API key to disk.

Fast path:
  python scripts/bimpe_hack.py bootstrap
  python scripts/bimpe_hack.py links
  python scripts/bimpe_hack.py chat "Was this transaction really from my bank?"
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
        raise BimpeError("BIMPE_API_KEY should look like sk_...; event/team codes are not API keys.")
    return key


def http() -> requests.Session:
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


def api(method: str, path: str, *, body: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
    key = require_key()
    headers = {
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
        "X-Request-Id": f"fraud-hack-{uuid.uuid4()}",
    }
    if method.upper() in {"POST", "PATCH", "PUT", "DELETE"}:
        headers["Content-Type"] = "application/json"
        headers["Idempotency-Key"] = f"fraud-hack-{uuid.uuid4()}"

    r = http().request(method, f"{BASE_URL}{path}", headers=headers, json=body, params=params, timeout=30)
    try:
        payload = r.json()
    except Exception:
        payload = {"raw": r.text}
    if r.status_code >= 400:
        raise BimpeError(f"{method} {path} failed [{r.status_code}]: {json.dumps(payload, indent=2)}")
    return payload


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        raise BimpeError("No bimpe_agent_state.json yet. Run bootstrap first or pass --agent-id.")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(**updates: Any) -> dict[str, Any]:
    state: dict[str, Any] = {}
    if STATE_PATH.exists():
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    state.update({k: v for k, v in updates.items() if v is not None})
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return state


def resolve_agent_id(args: argparse.Namespace) -> str:
    return args.agent_id or load_state()["agent_id"]


def fraud_system_prompt() -> str:
    return """
You are Sentinel, the fraud verification voice agent for Aegis Bank's fraud team.
You called the customer because the bank's monitoring system flagged a card transaction.
You are a GOVERNED agent: you verify, decide, take one bounded action, escalate, and log — you are not a general chatbot.

Voice style: short, calm, bank-grade. One idea per turn, then wait. UK English. Max 2 sentences per turn.

Demo case:
- Customer first name: Maya (confirm identity by first name ONLY)
- Transaction ID: TXN-88419
- Merchant: TechWorld Online
- Amount: £486.72
- Time: 18:42 today, Europe/London
- Card: ending 4821 only (never say more digits)
- Risk score: 92/100 — currently on a temporary hold pending the customer's check
- Case reference (use only AFTER you confirm fraud): FRAUD-1042

Open (identity-safe): "Hello, this is Sentinel from Aegis Bank's fraud team. We've flagged a payment on your card and I'd like to check it with you. Am I speaking with Maya?" Then state the amount, merchant and card ending 4821, and ask: "Did you make that payment?"

Branches:
1) SCAM-COACHING (handle FIRST, highest priority): if the customer says someone told them to move money to a "safe account", or that another person/another call is guiding them, STOP them. Tell them Aegis Bank will NEVER ask them to move money and that instruction is itself a scam. Do not let them transfer anything. Freeze the card and escalate to a human specialist immediately.
2) NO / "wasn't me": confirm it is fraud, freeze the card, and escalate. Only say the card is "frozen" once that is done; give case reference FRAUD-1042; offer a WhatsApp confirmation.
3) YES / recognised: reassure, take no action, the hold can be released, close politely.
4) UNSURE / vulnerable / identity cannot be verified: no pressure; escalate to a human specialist.

When you freeze and escalate, confirm in this shape: "Your card ending 4821 is now frozen, your reference is FRAUD-1042, and a human fraud specialist will call you within the hour. I can send that to your WhatsApp."

Hard safety rules (never break):
- Never ask for or accept a full card number, CVV, PIN, password, one-time code, or banking login.
- Never ask the customer to move money, install anything, or share their screen/device.
- Use the partial card reference only.
- If the customer doubts this call is real, tell them to hang up and call the number on the back of their card or in the app.
- Never claim an action is done unless it has been done. Keep the call under 90 seconds unless escalating.
""".strip()


def fraud_workflow_payload() -> dict[str, Any]:
    return {
        "name": "Fraud Alert Verification Agent — Hack Night",
        "description": "Outbound voice/chat agent that verifies flagged card transactions, blocks suspected fraud, and escalates risky cases.",
        "category": "financial-services",
        "system_prompt": fraud_system_prompt(),
        "tags": ["hack-night", "fraud", "voice", "banking", "card-security"],
        "channels": ["telephony", "webchat", "whatsapp"],
        "integrations": [],
        "setup_time": 10,
        "setup_steps": [
            "Create the agent.",
            "Add the demo transaction as text knowledge.",
            "Use test webchat for dry-run.",
            "Place a test outbound call for the live demo if telephony is enabled.",
        ],
        "faq": [
            {
                "question": "What if the customer does not trust the call?",
                "answer": "The agent tells them to hang up and call the official number on their card or banking app.",
            },
            {
                "question": "What sensitive data can the agent ask for?",
                "answer": "No full card number, CVV, PIN, password, OTP, or banking credentials. Only safe verification and yes/no transaction recognition.",
            },
        ],
        "rules": [
            {
                "id": "rule_scam_coaching",
                "name": "Refuse safe-account scam",
                "trigger": "Customer says someone told them to move money to a safe account, or another person/call is guiding them.",
                "condition": "Authorised-push-payment / safe-account scam pattern.",
                "response": "Tell them to stop; Aegis Bank never asks customers to move money; freeze the card and escalate to a human specialist.",
                "action": "freeze_card",
                "enabled": True,
            },
            {
                "id": "rule_block_escalate",
                "name": "Block and escalate denied transaction",
                "trigger": "Customer says they do not recognise the flagged transaction.",
                "condition": "Transaction denied or identity uncertain.",
                "response": "Mark suspected fraud, freeze the card, give case reference FRAUD-1042, and escalate to a human fraud specialist.",
                "action": "freeze_card",
                "enabled": True,
            },
            {
                "id": "rule_safe_callback",
                "name": "Safe callback on legitimacy concerns",
                "trigger": "Customer asks whether this call/message is real.",
                "condition": "Customer expresses mistrust, phishing concern, or requests proof.",
                "response": "Advise them to hang up and call the official number on their card or banking app. Do not pressure them to continue.",
                "action": "safe_callback_guidance",
                "enabled": True,
            },
        ],
        "flows": [
            {
                "name": "Flagged transaction verification",
                "description": "Verify a high-risk card transaction and route to allow/block/escalate outcome.",
                "category": "fraud",
                "priority": 1,
                "is_active": True,
                "trigger_keywords": [
                    {"keyword": "fraud", "weight": "high"},
                    {"keyword": "transaction", "weight": "high"},
                    {"keyword": "card", "weight": "high"},
                    {"keyword": "block", "weight": "medium"},
                ],
                "conversation_steps": [
                    {
                        "type": "text_response",
                        "content": "Hello, this is Sentinel calling on behalf of Aegis Bank's fraud team. We are checking a card transaction ending 4821. We will never ask for your PIN, password, CVV, or one-time code.",
                        "action": "safe_intro",
                        "followup": "If the customer mistrusts the call, give safe callback guidance. Otherwise continue to transaction recognition.",
                    },
                    {
                        "type": "text_response",
                        "content": "Do you recognise a £486.72 transaction at TechWorld Online at 18:42 today? Please answer yes, no, or unsure.",
                        "action": "verify_transaction",
                        "followup": "Yes -> customer-confirmed. No -> suspected fraud and escalate. Unsure -> escalate.",
                    },
                ],
            }
        ],
    }


def fraud_knowledge() -> str:
    return """
DEMO DATA — Aegis Bank Fraud Alert

Customer: Maya Okafor (confirm by first name only)
Card reference: ending 4821 only
Case reference (after fraud confirmed): FRAUD-1042
Escalation queue: human fraud specialist — fraud-ops@aegisbank.demo

Flagged transaction (high risk):
- TXN-88419 | TechWorld Online | £486.72 | 18:42 today | risk 92/100 | status: temporary hold

Recent normal transactions (context, not flagged):
- TXN-88410 | Pret A Manger | £4.20 | 08:12 today
- TXN-88402 | Tesco Superstore | £62.50 | yesterday 17:30
- TXN-88395 | Spotify | £9.99 | recurring

Outcome policy:
- Recognised by customer: mark customer-confirmed; the hold can be released.
- Not recognised: mark suspected fraud; freeze the card; give reference FRAUD-1042; escalate.
- Safe-account / "move your money" coaching: refuse, freeze, escalate (this is a scam).
- Unsure / vulnerable / identity unverified: escalate.
- Customer doubts legitimacy: advise safe callback using the official card/app number.

Forbidden requests:
Never ask for CVV, PIN, full card number, password, one-time code, screen sharing, remote access, or money movement.
""".strip()


def create_workflow() -> dict[str, Any]:
    payload = fraud_workflow_payload()
    try:
        return api("POST", "/workflows", body=payload)["data"]
    except BimpeError as e:
        print(f"Full workflow payload failed; retrying minimal workflow. Details:\n{e}", file=sys.stderr)
        minimal = {
            "name": payload["name"],
            "description": payload["description"],
            "category": payload["category"],
            "system_prompt": payload["system_prompt"],
        }
        return api("POST", "/workflows", body=minimal)["data"]


def cmd_list_workflows(args: argparse.Namespace) -> None:
    params: dict[str, Any] = {"limit": args.limit, "scope": args.scope}
    if args.search:
        params["search"] = args.search
    data = api("GET", "/workflows", params=params)
    for row in data.get("data", []):
        print(f"{row.get('id')} | {row.get('name')} | {row.get('category')} | owner={row.get('is_owner')}")
    if args.json:
        print_json(data)


def cmd_bootstrap(args: argparse.Namespace) -> None:
    workflow_id = args.workflow_id
    if workflow_id:
        workflow = api("GET", f"/workflows/{workflow_id}")["data"]
    else:
        print("Creating Fraud Alert Verification workflow...")
        workflow = create_workflow()
        workflow_id = workflow["id"]
    print(f"Workflow: {workflow_id} — {workflow.get('name')}")

    agent = api(
        "POST",
        "/agents",
        body={
            "workflow_id": workflow_id,
            "name": args.agent_name,
            "description": "Hack-night fraud alert verification agent for outbound voice/chat demo.",
        },
    )["data"]
    agent_id = agent["id"]
    print(f"Agent: {agent_id} — {agent.get('name')}")

    try:
        api(
            "PATCH",
            f"/agents/{agent_id}",
            body={
                "persona": "professional",
                "timezone": "Europe/London",
                "business_name": "Aegis Bank Fraud Operations",
                "business_address": "32-37 Cowper St, London EC2A 4AW",
                "business_email": "fraud-ops@aegisbank.demo",
                "business_description": "Fraud operations team verifying high-risk card transactions through safe AI voice workflows.",
                "escalation_email": "fraud-ops@aegisbank.demo",
            },
        )
    except BimpeError as e:
        print(f"Non-blocking: agent profile patch failed:\n{e}", file=sys.stderr)

    try:
        kb = api(
            "POST",
            f"/agents/{agent_id}/knowledge_bases",
            body={
                "type": "text",
                "name": "Demo flagged transaction and safety policy",
                "description": "Single-case demo dataset for fraud alert verification.",
                "content": fraud_knowledge(),
            },
        )["data"]
        print(f"Knowledge base: {kb.get('id')} — {kb.get('name')}")
    except BimpeError as e:
        print(f"Non-blocking: knowledge base creation failed:\n{e}", file=sys.stderr)

    try:
        api("PATCH", f"/agents/{agent_id}/live-status", body={"status": "live", "status_reason": "Hack-night fraud demo ready"})
    except BimpeError as e:
        print(f"Non-blocking: live-status update failed:\n{e}", file=sys.stderr)

    links = {}
    try:
        links = api("GET", f"/agents/{agent_id}/deployment/agent-test-code")["data"]
        print("Deployment/test links:")
        print_json(links)
    except BimpeError as e:
        print(f"Non-blocking: test-code retrieval failed:\n{e}", file=sys.stderr)

    state = save_state(agent_id=agent_id, workflow_id=workflow_id, deployment=links)
    print(f"Saved state: {STATE_PATH.resolve()}")
    print_json(state)


def cmd_links(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    data = api("GET", f"/agents/{agent_id}/deployment/agent-test-code")["data"]
    save_state(agent_id=agent_id, deployment=data)
    print_json(data)


def cmd_chat(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    data = api(
        "POST",
        f"/agents/{agent_id}/conversations/messages",
        body={
            "message": args.message,
            "role": "user",
            "channel_type": args.channel,
            "channel_user_id": args.user_id,
            "channel_username": args.username,
            "is_test_channel": True,
        },
    )
    print_json(data)


def cmd_conversations(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    data = api("GET", f"/agents/{agent_id}/conversations", params={"limit": args.limit, "is_test_channel": True, "sort": "-updated_at"})
    print_json(data)


def cmd_messages(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    data = api("GET", f"/agents/{agent_id}/conversations/{args.conversation_id}/messages", params={"limit": args.limit})
    print_json(data)


def cmd_call(args: argparse.Namespace) -> None:
    agent_id = resolve_agent_id(args)
    data = api("POST", f"/agents/{agent_id}/calls", body={"destination": args.destination, "is_test_call": args.test})
    print_json(data)


def cmd_phone_numbers(args: argparse.Namespace) -> None:
    print_json(api("GET", "/phone-numbers", params={"limit": args.limit}))


def cmd_request_number(args: argparse.Namespace) -> None:
    state = STATE_PATH.exists() and load_state() or {}
    body: dict[str, Any] = {
        "business_name": "Primo Bank Fraud Operations",
        "intended_use": "Hack-night demo: inbound/outbound AI voice agent for safe fraud alert verification.",
        "region": args.region,
        "agent_count": 1,
        "outbound_minutes": args.outbound_minutes,
    }
    if state.get("agent_id"):
        body["submitted_by_agent_id"] = state["agent_id"]
    print_json(api("POST", "/phone-numbers/request", body=body))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="BimpeAI fraud-track API helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("list-workflows")
    w.add_argument("--search", default="fraud")
    w.add_argument("--scope", default="accessible", choices=["accessible", "owned", "public"])
    w.add_argument("--limit", type=int, default=30)
    w.add_argument("--json", action="store_true")
    w.set_defaults(func=cmd_list_workflows)

    b = sub.add_parser("bootstrap")
    b.add_argument("--workflow-id", help="Use an existing public fraud workflow instead of creating one.")
    b.add_argument("--agent-name", default=f"Fraud Alert Verification Agent {time.strftime('%H%M')}")
    b.set_defaults(func=cmd_bootstrap)

    links = sub.add_parser("links")
    links.add_argument("--agent-id")
    links.set_defaults(func=cmd_links)

    chat = sub.add_parser("chat")
    chat.add_argument("message")
    chat.add_argument("--agent-id")
    chat.add_argument("--channel", default="webchat", choices=["webchat", "whatsapp", "telephony"])
    chat.add_argument("--user-id", default=str(uuid.uuid4()))
    chat.add_argument("--username", default="Maya Okafor")
    chat.set_defaults(func=cmd_chat)

    conv = sub.add_parser("conversations")
    conv.add_argument("--agent-id")
    conv.add_argument("--limit", type=int, default=10)
    conv.set_defaults(func=cmd_conversations)

    msg = sub.add_parser("messages")
    msg.add_argument("conversation_id")
    msg.add_argument("--agent-id")
    msg.add_argument("--limit", type=int, default=20)
    msg.set_defaults(func=cmd_messages)

    call = sub.add_parser("call")
    call.add_argument("destination", help="E.164 number, e.g. +447700900123")
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
