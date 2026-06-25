#!/usr/bin/env python3
"""Aegis Bank mock card ledger + fraud audit trail (DEMO ONLY).

No external deps, no network. Gives a visible card ledger and a clean audit-trail
JSON for the live demo, so "the agent froze the card" has something real on screen.
This is a clean MOCK of a card-management system — not real banking infrastructure.

Usage:
  python scripts/mock_bank.py ledger              # show all transactions + card status
  python scripts/mock_bank.py freeze TXN-88419    # confirm fraud, freeze card, print audit + WhatsApp
  python scripts/mock_bank.py whatsapp            # print the WhatsApp confirmation message
  python scripts/mock_bank.py reset               # reset to demo start state
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:  # Windows consoles default to cp1252; force UTF-8 so emoji and £ print
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

LEDGER_PATH = Path("bank_ledger.json")
CASE_ID = "FRAUD-1042"
CARD = "4821"
CUSTOMER = "Covi Okafor"

DEMO_STATE = {
    "bank": "Aegis Bank",
    "customer": CUSTOMER,
    "card_last4": CARD,
    "card_status": "active",
    "transactions": [
        {"id": "TXN-88419", "merchant": "TechWorld Online", "amount_gbp": 486.72, "time": "18:42 today", "risk_score": 92, "status": "flagged"},
        {"id": "TXN-88410", "merchant": "Pret A Manger", "amount_gbp": 4.20, "time": "08:12 today", "risk_score": 2, "status": "cleared"},
        {"id": "TXN-88402", "merchant": "Tesco Superstore", "amount_gbp": 62.50, "time": "yesterday 17:30", "risk_score": 3, "status": "cleared"},
        {"id": "TXN-88395", "merchant": "Spotify", "amount_gbp": 9.99, "time": "recurring", "risk_score": 1, "status": "cleared"},
    ],
}


def load() -> dict:
    if LEDGER_PATH.exists():
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return json.loads(json.dumps(DEMO_STATE))


def save(state: dict) -> None:
    LEDGER_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def whatsapp_message() -> str:
    return (
        f"✅ Aegis Bank fraud alert: your card ending {CARD} has been frozen. "
        f"Case ID {CASE_ID}. A human fraud specialist will call you within the hour. "
        f"You don't need to do anything else."
    )


def cmd_ledger() -> int:
    s = load()
    print(f"{s['bank']} | card ending {s['card_last4']} ({s['customer']}) | STATUS: {s['card_status'].upper()}")
    print("-" * 72)
    for t in s["transactions"]:
        print(f"  {t['id']}  {t['merchant']:<18} GBP {t['amount_gbp']:>8.2f}  {t['time']:<14} risk {t['risk_score']:>3}  [{t['status']}]")
    return 0


def cmd_freeze(txn_id: str) -> int:
    s = load()
    txn = next((t for t in s["transactions"] if t["id"] == txn_id), None)
    if not txn:
        print(f"Unknown transaction {txn_id}", file=sys.stderr)
        return 1
    s["card_status"] = "frozen"
    txn["status"] = "fraud_confirmed"
    save(s)

    audit = {
        "transaction_id": txn_id,
        "customer": s["customer"],
        "merchant": txn["merchant"],
        "amount_gbp": txn["amount_gbp"],
        "risk_score": txn["risk_score"],
        "decision": "fraud_confirmed",
        "card_status": "frozen",
        "case_id": CASE_ID,
        "escalated": True,
        "escalation_queue": "human_fraud_specialist",
        "channel": "voice",
    }
    print("AUDIT TRAIL")
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    print("\nWHATSAPP CONFIRMATION")
    print(whatsapp_message())
    return 0


def cmd_whatsapp() -> int:
    print(whatsapp_message())
    return 0


def cmd_reset() -> int:
    save(json.loads(json.dumps(DEMO_STATE)))
    print("Ledger reset to demo start state.")
    return 0


def main() -> int:
    args = sys.argv[1:]
    cmd = args[0] if args else "ledger"
    if cmd == "ledger":
        return cmd_ledger()
    if cmd == "freeze":
        return cmd_freeze(args[1] if len(args) > 1 else "TXN-88419")
    if cmd == "whatsapp":
        return cmd_whatsapp()
    if cmd == "reset":
        return cmd_reset()
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
