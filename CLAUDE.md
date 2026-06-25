# Agent Onboarding — BimpeAI Fraud Alert Verification Agent

You are helping a 3-person team **win** the London Agentic AI Hack Night (25 Jun 2026),
Developer/API track. Read this fully before acting. Match the existing code style.

## Mission
Build an **outbound voice agent** (BimpeAI Console API, Python) that:
1. Calls a customer about a flagged card transaction (transaction feed is **mocked**).
2. Verifies whether they authorised it.
3. On "no": freezes the card (**mocked** action), escalates to a human fraud agent, and
   sends a **WhatsApp** confirmation.

Judged on: Creativity, Execution (works end-to-end), Business Value (deployable tomorrow),
Presentation (3 min). The winning moment is **a real phone ringing live in the room**.

## Where the ground truth lives
- API reference (offline): `bimpe_api_endpoint_notes.txt`, plus `bimpe_*.txt`.
- Hackathon spec + 20 example workflows: `notion_resource_hub.md`.
- Working CLI to reuse: `scripts/bimpe_hack.py` (request/session/retry/state helpers).
  It currently bootstraps an invoice agent; it's being repurposed to fraud.
- Authoritative build + demo plan: `PLAN.md` (read it once it exists).

## API essentials
- Base: `https://api.bimpe.ai/api/v1/console`  ·  Auth: `Bearer $BIMPE_API_KEY`
- Endpoints you'll use: `POST /workflows`, `POST /agents`, `POST /agents/{id}/knowledge_bases`,
  `PATCH /agents/{id}/live-status`, `GET /agents/{id}/deployment/agent-test-code`,
  `POST /agents/{id}/conversations/messages`, `POST /agents/{id}/calls` (`is_test_call=true`).
- First-party integrations: stripe, google_calendar, google_sheets, paystack, bumpa; plus
  custom HTTP API actions and MCP servers.

## Run it
```bash
pip install -r requirements.txt
export BIMPE_API_KEY=sk_...        # PowerShell:  $env:BIMPE_API_KEY='sk_...'
python scripts/bimpe_hack.py list-workflows     # read-only smoke test
```

## Rules — do not violate
- **NEVER hardcode or commit the API key.** Env var only. It's a shared team secret.
- **Don't break** `scripts/bimpe_hack.py`'s working commands — extend, don't blindly rewrite.
- **Outbound voice = test telephony** (`is_test_call=true`). Do NOT rely on inbound voice;
  it needs a provisioned UK number we won't have in time.
- Card-block + transaction feed are **mocked**. Never claim a real block/payment happened.
- Make **small, frequent commits** with clear messages so 3 people + their agents don't collide.

## Coordinate with the human lead (Bobby) before
Placing real outbound calls, setting an agent `live`, or changing shared demo data.
