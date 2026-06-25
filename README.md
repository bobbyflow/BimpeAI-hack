# 🛡️ Sentinel — Autonomous Fraud Verification Agent

**London Agentic AI Hack Night 2026 · Built on BimpeAI · Developer / API track**

> When a bank flags a suspicious card payment, **Sentinel calls the customer itself** —
> verifies the transaction, sees through scam-coaching, freezes the card, escalates to a
> human, and confirms over WhatsApp. **Fraud contained in under a minute, fully audited.**

Banks are great at *detecting* fraud. The gap is the 60 seconds *after* a flag — a human has
to phone the customer, and most calls don't connect in time. Sentinel is the autonomous
first-responder that closes that gap.

## ▶️ Try the live agent
**WhatsApp:** https://wa.me/442070975887?text=start%20P4Q3H5HH

Click → send the pre-filled message → chat with Sentinel live. Try saying
*"someone told me to move my money to a safe account"* and watch it shut the scam down.

## 🔴 What it does
1. The bank's monitor flags a card payment — **£486.72 at TechWorld Online, risk 92/100**.
2. **Sentinel phones the cardholder** (real outbound call) and verifies it.
3. On *"that wasn't me"*: reassures the customer (*"you won't be held responsible"*),
   **freezes the card**, escalates to a human specialist, and **sends a WhatsApp confirmation**
   with case reference `FRAUD-1042`.
4. **Scam-coaching detection:** if a scammer is coaching the victim to "move money to a safe
   account," Sentinel refuses and secures the account.
5. **Knows its lane:** off-scope requests (e.g. investment advice) are handed off to the
   advisory line — a *governed* agent, not a generic chatbot.
6. Every step is **logged and auditable**.

## 📊 The bank ledger (demo data)
Live transaction sheet:
**https://docs.google.com/spreadsheets/d/1tknIidKmwWcTcpj0fCXnKWEunVlpZGdX_tlTAT588AU/edit?gid=1217042048#gid=1217042048**

Also in [`demo/transactions.csv`](demo/transactions.csv). The flagged row flips
ACTIVE → FROZEN via [`scripts/mock_bank.py`](scripts/mock_bank.py) — a clean mock of a
card-management system plus an audit trail.

## 🧠 How it works
- **BimpeAI Console API** — workflow + agent + knowledge base + **outbound voice (telephony)**
  + WhatsApp + web chat.
- [`scripts/bimpe_hack.py`](scripts/bimpe_hack.py) — creates/deploys the agent and drives the
  demo (`bootstrap`, `call`, `chat`, `conversations`).
- [`scripts/mock_bank.py`](scripts/mock_bank.py) — mock card ledger + audit-trail JSON + the
  WhatsApp confirmation message.
- The transaction feed and card adapter are **mocked behind clean interfaces** — the
  conversation, the decision, the escalation, and the audit trail are real and live.
- **Deployable tomorrow:** swap the two mocks for a bank's transaction feed + card API.

Full build & demo plan: [`PLAN.md`](PLAN.md).

## 🚀 Run it
```bash
pip install -r requirements.txt
export BIMPE_API_KEY=sk_...                       # PowerShell: $env:BIMPE_API_KEY='sk_...'
python scripts/bimpe_hack.py bootstrap            # create + deploy the agent
python scripts/bimpe_hack.py call +447XXXXXXXXX   # outbound verification call
python scripts/mock_bank.py  freeze TXN-88419     # freeze the card + print audit trail
```

## 🏆 Why it wins
- **Creativity** — an agent that *outsmarts the scammer*, not just a fraud notifier.
- **Execution** — a real outbound call, live, end-to-end.
- **Business value** — card fraud is a £1bn+ problem; Sentinel contains it in seconds, and it's
  deployable now.
- **Presentation** — one tight, memorable arc: the phone rings, and the agent does the rest.

## 👥 Team
Bobby · Covi · Rohit

---
*Built in 90 minutes at the London Agentic AI Hack Night 2026, powered by BimpeAI.*
