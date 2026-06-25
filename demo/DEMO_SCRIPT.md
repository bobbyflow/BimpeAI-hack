# Demo Script

Owner: covifranklin

## 60-second story

A bank's monitoring system flags a suspicious card transaction. Our agent **calls the
customer**, asks if they made it, and on "no" it **keeps the card blocked**, **escalates to a
human**, and **sends a WhatsApp confirmation** — containing fraud in seconds, not hours.

## Happy path

1. Agent calls the customer about a flagged transaction.
2. Agent gives the safety disclaimer: it will never ask for PIN, CVV, password, or one-time code.
3. Agent asks whether the customer recognises the transaction.
4. Customer says "no".
5. Agent marks suspected fraud, keeps the card blocked, escalates to a human specialist, and confirms next steps.

## Trust/safety path

If the customer asks "how do I know this is real?", the agent tells them to hang up and call the official number on the back of their card or in the banking app.

## Fallback if API/live demo fails

Show the script command, explain the intended API call, then read the expected response from this file. Keep it calm: "The live service is the only external dependency; our flow, prompts, and integration code are ready."

## Demo line

"The important part is not just making a call. It is reducing fraud loss while preserving customer trust through safe verification, no sensitive credential collection, and immediate escalation."
