# Demo Script

Owner: covifranklin

> ⚠️ **PIVOT (25 Jun):** The build is now the **Fraud Alert Verification** voice agent,
> not invoice recovery. See `CLAUDE.md` for the mission and `PLAN.md` for the full
> build + demo plan (incoming). The invoice story below is kept only for reference.

## 60-second story (NEW — fraud)

A bank's monitoring system flags a suspicious card transaction. Our agent **calls the
customer**, asks if they made it, and on "no" it **freezes the card**, **escalates to a
human**, and **sends a WhatsApp confirmation** — containing fraud in seconds, not hours.

## 60-second story (OLD — invoice, reference only)

We built a BimpeAI revenue recovery agent for a small business. It contacts a customer about an overdue invoice, gives safe options, sends a payment link, schedules a callback, or escalates sensitive cases.

## Happy path

1. Customer asks about overdue invoice.
2. Agent identifies invoice and amount.
3. Agent offers: pay now, callback, or dispute.
4. Customer chooses pay now.
5. Agent sends secure payment link and sets expectation that payment is pending confirmation.

## Fallback if API/live demo fails

Show the script command, explain the intended API call, then read the expected response from this file. Keep it calm: "The live service is the only external dependency; our flow, prompts, and integration code are ready."

## Demo line

"The important part is not just sending reminders. It is collecting revenue while preserving customer trust through escalation rules and safe payment handling."
