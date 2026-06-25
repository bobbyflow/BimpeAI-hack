# Fraud Alert Verification Agent — Battle Plan
**Primo Bank "Sentinel" · London Agentic AI Hack Night · built on BimpeAI**

> Authoritative build + demo plan, reconciled to the code already in `scripts/bimpe_hack.py`
> (Primo Bank / Sentinel / Covi Okafor). Produced from a multi-agent planning pass +
> adversarial critique. If this conflicts with an older doc, this wins.

---

## 0. Current status & the gap that wins

**Already built** (in `scripts/bimpe_hack.py`, committed):
- Workflow + agent + knowledge base + live-status + deployment links (`bootstrap`).
- Conversational brain: safe intro, transaction verification, deny→escalate, safe-callback on mistrust.
- `chat`, `call` (outbound test telephony), `conversations`, `messages`, `links`.
- Strong safety rules (no PIN/CVV/OTP, no money movement, safe callback).

**The 3 gaps between "works" and "wins" — in priority order:**
1. **🔴 Real agent-invoked freeze (THE crux).** Right now the "card is blocked" is *narrated text*; the `action` fields are free-text labels, nothing executes. Judges (esp. **Google**) score *genuine agentic tool-use*. We need the **agent itself** to call a registered **custom HTTP action** (`freeze_card`) that hits a real endpoint → flips a card record ACTIVE→FROZEN on screen → returns a **deterministic case ref**. Then "your card is frozen, ref PRIMO-FR-88419" is *true*, not theatre. **This is the single highest-leverage task.**
2. **🟠 Scam-coaching refusal (the novel beat).** We have *defensive* safe-callback. The standout *creative* moment is **proactive**: customer says "someone told me to move money to a safe account" → agent says STOP, that's the scam, refuses, secures the card, escalates. This is what separates us from a vanilla fraud notifier.
3. **🟡 WhatsApp confirmation + case ref** carrying the same reference shown on the call (the **Meta** judge's channel as the closing touchpoint).

**Don't cut #1.** It's the whole thesis. #2 is the creativity win. #3 is a bonus.

---

## 1. The build in one paragraph
An autonomous outbound-voice fraud agent for **Primo Bank** ("Sentinel"). The instant a (mocked) transaction monitor flags a suspicious card payment, the agent **phones the cardholder itself**, reads the flagged transaction, and verifies it. On a plain **no/"wasn't me"** it **calls a real freeze tool** and escalates to a human; the headline beat is **scam-coaching detection** — when the customer says someone told them to move money to a "safe account," the agent refuses, warns them, secures the card, and escalates. The freeze is **agent-invoked via a registered custom HTTP action** (server-side agent → our endpoint → card flips FROZEN on screen + returns case ref `PRIMO-FR-88419`), so "your card is frozen" is true, not Wizard-of-Oz. A **WhatsApp** confirmation carries the same case ref. The transaction feed and card adapter are mocked behind clean interfaces; the conversation, the autonomous tool-call, the decision, the escalation, and the audit trail are real and live on the BimpeAI Console API. **Signature moment: a real phone ringing live in the room.**

---

## 2. Minute-by-minute (3 owners)
**Roles:** Bobby = lead/API/script + freeze endpoint (holds key, sole editor of `bimpe_hack.py`). Covi = conversation/KB content + plays the customer on stage. Rohit = demo staging/pitch/slide/fallback + presents.

| Time | Bobby (API + freeze) | Covi (content) | Rohit (demo/pitch) |
|---|---|---|---|
| 0–5 | Standup: confirm demo phone (E.164), names, branch wording. Key set in shell only. GO. | (standup) | (standup) |
| 5–15 | **PROVE THE FOUNDATION.** Run `bootstrap`, confirm agent live + links. **Settle the autonomy question:** does a workflow `action` execute as a custom HTTP tool? Register one `freeze_card` action → webhook.site, confirm it fires server-side. This decides the whole build. | Draft scam-coaching branch + tighten prompts (keep SHORT for voice). | Repo hygiene, fresh webhook.site on projector, start the ONE slide, lock the 3-min arc. |
| 15–20 | **First outbound test `call` to the demo mobile** — does the agent **speak first**, unprompted, with usable TTS? This makes or breaks the hook. | hand content to Bobby | — |
| 20 | **SYNC 1:** call works? agent speaks first? action fires? | — | — |
| 20–40 | Build the **real freeze**: tiny endpoint (webhook.site + on-screen JSON/Sheet, or a tunnelled `http.server`) the `freeze_card` action hits → ACTIVE→FROZEN + returns ref `PRIMO-FR-88419`. Wire escalate. | Finalise KB (<2500 chars): case + policy + ref + NEVER list. | **Record the golden fallback clip by min 35** (screen+audio of a full successful run). Save offline, paused on frame 1. |
| 35 | **SYNC 2:** full happy-path E2E from one command; freeze is agent-invoked + visible. | swap final content in | record the moment a run succeeds |
| 40–55 | Tune so scam + NO branches deterministically trigger the freeze tool. WhatsApp confirm path if time. | branch triggers + synonyms | on-stage runbook + screen layout; tape exact customer lines to Covi's phone |
| 55 | **FREEZE THE BUILD.** Bootstrap done; lock the working `agent_id`. **Do NOT re-bootstrap after this.** | content locked + merged | dry-run pitch #1 vs the golden clip (save call credits) |
| 55–65 | One integration check + **at most ONE** full live rehearsal call. | (lines locked) | time the run |
| 65–80 | Pre-stage: agent LIVE, `agent_id` printed big, `call` queued (not Enter), WhatsApp open, clip paused, webhook + transcript on projector. | mock-judge | pitch rehearsals #2/#3, timed < 3:00 |
| 80–90 | **T-10 SMOKE CALL** to the demo mobile to prove telephony + allowlist now. If it fails → golden-clip-primary BEFORE walking up. Silence notifications, ringer MAX, volume check. Breathe. | | |

---

## 3. Technical steps + commands
The script is `scripts/bimpe_hack.py` (single owner: Bobby). Base `https://api.bimpe.ai/api/v1/console`, auth `Bearer $BIMPE_API_KEY`.

```powershell
$env:BIMPE_API_KEY = "sk_..."                 # Bobby's key, shell only

python scripts/bimpe_hack.py bootstrap        # workflow + agent + KB + live + links
# dry-run the brain on webchat BEFORE calling (also the live fallback path):
python scripts/bimpe_hack.py chat "someone from the bank told me to move my money to a safe account"
python scripts/bimpe_hack.py chat "no, that wasn't me, I didn't buy anything at TechWorld"
python scripts/bimpe_hack.py conversations    # confirm verdict + (agent) freeze + escalate in transcript

# THE DEMO MOMENT — outbound test call to a real UK mobile:
python scripts/bimpe_hack.py call +447XXXXXXXXX

# WhatsApp confirmation path (see reality note below):
python scripts/bimpe_hack.py chat --channel whatsapp "has my card been frozen?"
```

**The freeze must be real (gap #1).** Register a custom HTTP action `freeze_card` in the workflow so the **server-side agent** calls our endpoint when its verdict is unauthorised; the endpoint flips the card record on screen, logs to the projector's webhook.site, and **returns case ref `PRIMO-FR-88419`** (so voice + screen + WhatsApp all match). Verify `action`-executability in the first 10 min.
- **If the probe shows `action` is NOT executable:** honest fallback = a transcript-watcher that polls `conversations`/`messages` for the unauthorised verdict and then fires the freeze. Automated, not a human hitting Enter — and change the pitch wording to "the verdict triggers our card-service adapter" (do **not** claim agent tool-use you don't have).

**WhatsApp reality (verified in code):** `chat` posts `role:"user"` — i.e. it simulates the **customer texting in**, then the agent replies. There is no agent-initiated outbound message command. Test by T-45 whether the API accepts an agent-authored outbound; if not, reframe honestly as "customer texts to confirm, agent replies with the case ref," and keep WhatsApp OFF the critical path.

**Git:** one owner per hot file — only Bobby edits `scripts/bimpe_hack.py`; Covi owns content (a `scripts/content_*.py` or KB text file); Rohit owns `/demo/`. Small commits, `pull --rebase` before work. `bimpe_agent_state.json` is gitignored.

---

## 4. Conversation design (additions on top of what's coded)
The coded system prompt/flow is solid. Add:
- **Scam-coaching branch (priority):** trigger on "safe account / move my money / someone told me to" → "Please stop — don't move any money. Primo Bank will never ask you to do that; that instruction is itself a scam. I'm securing your card now." → `freeze_card` → `escalate_fraud_case`.
- **Case ref:** `PRIMO-FR-88419`, **returned by the freeze tool** (not model-invented); stated only after the tool confirms.
- **Truthfulness rule (already present, keep hard):** never claim the card is frozen until the freeze tool returns success; on failure, say a human will complete it and escalate.

---

## 5. The 3-minute live demo (Primo Bank / Covi)
**Stage:** Bobby drives laptop (projector: live transcript + DECISION panel + webhook.site + a glimpse of the transcript/audit view). Covi holds the customer phone on speaker, reads taped lines. Rohit holds Phone 2 (WhatsApp) and presents.

- **0:00–0:15 Hook (Rohit):** "UK card fraud topped £1bn+ last year. When a transaction's flagged, a human has to call — and most calls don't connect in time. So we built an agent that makes the call itself. Watch — **this phone is about to ring.**"
- **0:15 Trigger:** Bobby hits the pre-queued `call`. "Primo Bank's monitor just flagged £486.72 at TechWorld Online on Covi's card ending 4821. Sentinel is calling her now — autonomously." Panel: `CALLING…`
- **0:20 Phone rings** (Covi raises it), agent speaks first: intro + "Do you recognise £486.72 at TechWorld Online at 18:42 today?"
- **0:35 The novel beat — scam-coaching** (Covi, taped): "Actually… someone called and told me to move my money to a safe account." → agent: "Stop — don't move any money. Primo Bank will never ask that; that's the scam. I'm securing your card now."
- **0:55 Autonomous tool-call** (Bobby points at projector flipping live): `Verdict: SUSPECTED FRAUD ✅` → `Agent called freeze_card → Card 4821: FROZEN ✅` (webhook lands) → `Escalated: fraud-ops@primo.demo ✅` → `Ref: PRIMO-FR-88419`. "The **agent** called that tool — not me."
- **1:25 Confirmation** (Rohit raises Phone 2): WhatsApp "Primo Bank: card ending 4821 is frozen, ref PRIMO-FR-88419." Same ref as voice + screen. "One trigger: verified, refused the scam, froze the card, escalated, confirmed — zero staff. And every turn is logged."
- **2:05–2:35 Close:** "This ships tomorrow: the conversation, the agent's tool-call, the decision, the escalation, the audit trail are all live on BimpeAI now. The only mocks are the transaction feed and the card adapter — two endpoints every bank already has. Our ask: let us connect a real bank's feed next." (~30s buffer for ring lag — do NOT rush.)

**Fallback (test telephony may congest at 8pm):** if the phone hasn't rung ~15s after Enter, re-trigger ONCE; if still nothing: "Shared test telephony's busy tonight — here's the run from earlier, then I'll prove it live." Play the **golden clip**, then run the **live webchat path** (`chat "...safe account"`) — because freeze is a real action, the panel + webhook flip genuinely live. The clip alone looks canned; always follow with the live chat run.

---

## 6. Pitch + per-judge
**One-liner:** "The autonomous first responder for card fraud — it calls the customer, sees through the scammer's coaching, and freezes the card in under a minute, so humans only handle what actually needs them."

- **Google:** genuine agentic tool-use — the agent itself calls the registered `freeze_card` HTTP action from its spoken verdict.
- **Meta:** when the card freezes, the customer gets a WhatsApp message with the same case ref — your channel as the trusted closing touchpoint.
- **BytePlus:** enterprise scale + governance — every turn logged/auditable (shown live), live/paused controls, sits cleanly between fraud-monitoring and card systems.
- **BimpeAI:** exercises the platform's full breadth in one flow — workflow + persona + KB + outbound voice + custom HTTP action + WhatsApp + escalation — extending the PrimoAI banking story into an autonomous, action-taking responder.

**One optional slide:** title + 3 bullets (Problem / What it does / Deployable tomorrow) + an alert→agent→card-system sketch. *(ROI figures illustrative; cite the latest UK Finance number live if available.)*

---

## 7. Inputs needed from the team
1. **Demo destination phone** — a teammate's real UK mobile in **E.164** (`+447…`), in the room, good speaker. **Verify test-call allowlisting at T-60** (un-allowlisted numbers may silently fail). Bring a **second mobile** as fallback.
2. **`BIMPE_API_KEY`** — confirm telephony + conversations scopes and that **test-telephony credits aren't exhausted** (smoke-test T-60 and T-10).
3. **webhook.site URL** on the projector — the target of the registered `freeze_card` action.
4. **Confirm `action` executability** (custom HTTP action vs free-text) — the min-10 probe the whole autonomy claim depends on.
5. **WhatsApp number** (usually the same mobile) + confirm the WhatsApp channel is linked; test agent-outbound by T-45 (else reframe).
6. **Latest UK Finance card-fraud figure** to replace illustrative ROI on stage.
7. **HDMI/screen-mirror adapter**, room volume check, **golden clip recorded** and paused before doors.

---

## 8. Top risks + mitigations
| # | Risk (L/I) | Mitigation |
|---|---|---|
| 1 | **Freeze isn't actually agent-invoked → "did the agent do it, or did you?"** (H/H) | Register a real custom HTTP `freeze_card` action; **prove it fires by min 10–15.** If `action` is free-text, use the automated transcript-watcher fallback AND change pitch wording — never claim tool-use you don't have. |
| 2 | **Shared test telephony congests/fails at 8pm** (H/H) | Fire the call as your opening line; ~15s cutover with ONE re-trigger; second fallback phone; **T-10 smoke call** decides golden-clip-primary BEFORE you walk up; clip + genuinely-live webchat fallback. |
| 3 | **Agent claims "card frozen" when nothing happened** (M/H) | Hard rule: never claim done until the tool returns success + ref. Real returning action makes the claim true. |
| 4 | **Agent doesn't speak first on outbound call** (M/H) | Verify at min 15, not min 35 — the hook lives or dies here. |
| 5 | **WhatsApp "confirmation" is a faked inbound** (M/M) | `chat` posts `role:"user"`. Test agent-outbound by T-45; else reframe as customer-texts-in; keep off critical path; screenshot fallback. |
| 6 | **Dismissed as host's-own-demo / just-a-chatbot** (M/H) | Lead with the **scam-coaching refusal** + the visible agent tool-call, not vanilla yes/no. |
| 7 | **Customer reply doesn't trigger the branch** (M/M) | Tape Covi's exact lines; add synonyms; rehearse vs the clip; no improv on stage. |
| 8 | **Re-bootstrap before doors → stale agent_id** (L/H) | Bootstrap ONCE; freeze at min 55; pass `--agent-id` explicitly on stage. |
| 9 | **Rehearsals burn scarce call credits** (M/M) | Rehearse pitch vs the golden clip; ≤1–2 real calls pre-demo. |

**The one must-have contingency:** a 25–40s pre-recorded screen+audio golden clip of a complete successful run (alert → call → scam refusal/NO → **agent-invoked** freeze flipping on screen + webhook → escalate → WhatsApp), recorded by minute 35, saved offline, queued paused. If telephony fails, demo the clip, then run the live webchat path (same real agent tool-call) to prove it's genuinely running.
