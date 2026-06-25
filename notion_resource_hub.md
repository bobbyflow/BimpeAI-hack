# London Agentic AI Hack Night — Builder Resource Hub
  London Agentic AI Hack Night · 25 June 2026 · Civo Tech Junction, Old Street
  Hosted by AI Agents Academy · Powered by BimpeAI
---

#### Welcome, Builder
  You've been accepted to the London Agentic AI Hack Night. This page is your pre-event resource hub — everything you need to hit the ground running on June 25th.
  You'll have 90 minutes to build a working AI agent and demo it live to judges from Google, Meta, BimpeAI, and BytePlus. The workflows below are designed to be cloned and customised inside BimpeAI's platform in that window. Each deploys to voice (real UK phone numbers) and/or chat channels (WhatsApp, Web Chat, Instagram, Facebook Messenger).
  Browse. Pick a track. Pick a workflow. Clone it. Make it yours.
---

#### Choose Your Track
  There are two ways to build on the night. Pick whichever suits your skill set.

##### 🧱 Builder Track (No-Code)
  Use BimpeAI's Agent Builder — a visual, drag-and-connect playground. No coding required. Clone a workflow template from the Agent Library, customise the conversation flows, connect integrations, and deploy to a live channel. Best for product people, designers, founders, and anyone new to the platform.
  👉 Open Agent Builder [Open Agent Builder](https://bimpe.ai/product/builder)
  👉 Browse the Agent Library [Browse the Agent Library](https://bimpe.ai/agent-library)

##### 💻 Developer Track (API)
  Use BimpeAI's Console API to create and manage agents programmatically. Authenticate with your team API key, call REST endpoints to create agents, assign workflows, wire up integrations and channels, and define conversation flows and actions — all via code. Best for developers and engineers who want full control.
  Base URL: https://docs.bimpe.ai/ [https://docs.bimpe.ai/](https://docs.bimpe.ai/)
  Quick start:
  1. Get your API key: BimpeAI Dashboard → Settings → API Keys → Generate [BimpeAI Dashboard](https://app.bimpe.ai/)
  1. Authenticate: Authorization: Bearer sk_...
  1. List workflows: GET /api/v1/console/workflows
  1. Create an agent: POST /api/v1/console/agents (with name, system_prompt, agent_workflow_id)
  1. Wire up channels and integrations via the sub-resource endpoints
  1. Deploy to your preferred channels
  👉 Full API Reference [Full API Reference](https://docs.bimpe.ai/docs/api/)
---

#### What You'll Have Access To
  - Agent Builder — no-code playground to design and test workflows visually
  - Developer Console + API — REST API control plane for programmatic agent management
  - Free credits — platform credits to build and deploy on the night
  - UK phone numbers — connect voice agents to real, callable numbers
  - Multichannel deployment — ship to Direct call, WhatsApp, Web Chat, Instagram, Facebook Messenger, and Voice
  - Integrations — plug into Google Calendar, Stripe, CRMs, POS systems, and internal tools
---

#### 20 Workflows You Can Clone & Build
  Each workflow can be cloned from the Agent Library (Builder Track) or created via the API (Developer Track). Difficulty is rated for the 90-minute hack window. Integration callouts show which apps you'll need to connect.
---

##### 🛒 Retail & E-commerce
  1. General E-commerce Store Agent
  🟢 Beginner · Builder Track · WhatsApp · Web Chat · FB Messenger
  Full-service store agent: product browsing, inventory checks, order placement, and post-purchase support. Clone the template, connect your catalogue, and you have a working storefront.
> Integrations needed: Product catalogue (CSV upload or API), optional payment gateway
  2. Flash Sale & Promo Notification Agent
  🟢 Beginner · Builder Track · WhatsApp · Voice (Outbound)
  Push time-limited deals to a customer list and handle inbound order spikes from promo-driven traffic. Great for retail, D2C, and marketplace sellers.
> Integrations needed: Customer contact list, optional CRM connection
  3. Returns & Refund Processing Agent
  🟡 Intermediate · Either Track · WhatsApp · Web Chat
  Automate the post-purchase flow: return requests, eligibility checks, refund status updates, and replacement scheduling. Connects to order management via API.
> Integrations needed: Order management system (API), Stripe or payment gateway for refund processing
  4. Product Recommendation Agent
  🟡 Intermediate · Developer Track · Web Chat · WhatsApp
  Personalised product suggestions based on browsing context and stated preferences. Uses knowledge bases and conversation flows to match intent to catalogue.
> Integrations needed: Product catalogue (knowledge base upload), optional CRM for customer history
---

##### 🍽️ Food & Beverage
  5. Restaurant Ordering & Table Booking
  🟢 Beginner · Builder Track · WhatsApp · Web Chat
  Menu browsing, dietary filtering, table reservations, and takeout orders with intelligent upselling. Clone the restaurant template and swap in your menu.
> Integrations needed: Google Calendar (table availability), menu data (knowledge base upload)
  6. Food Delivery Dispatch Agent
  🟡 Intermediate · Either Track · WhatsApp
  End-to-end delivery workflow: order placement, driver coordination, real-time tracking updates, and delivery confirmation.
> Integrations needed: POS system, logistics/delivery API, Google Calendar
  7. Catering & Event Orders Agent
  🟡 Intermediate · Either Track · Web Chat · Voice (Inbound)
  Handle catering inquiries for corporate events and parties. Menu customisation, headcount-based pricing, dietary accommodations, and booking confirmation.
> Integrations needed: Google Calendar (availability), Stripe (deposits), menu/pricing data (knowledge base)
---

##### 🏨 Hospitality & Travel
  8. Hotel Reservation & Concierge
  🟢 Beginner · Builder Track · WhatsApp · Web Chat
  Room availability, booking, amenity questions, and local recommendations. Clone the hotel template and configure your room types and rates.
> Integrations needed: Room inventory/rates (knowledge base), Google Calendar (availability), optional Stripe
  9. Short-Stay Self Check-in Agent
  🟢 Beginner · Builder Track · WhatsApp
  Automate guest communications for Airbnb-style stays: check-in instructions, key codes, house rules, Wi-Fi details, and checkout reminders.
> Integrations needed: Property details (knowledge base upload) — no external APIs required
  10. Event Venue Inquiry Agent
  🟡 Intermediate · Either Track · Voice (Inbound) · Web Chat
  Field inquiries about venue availability, capacity, and pricing tiers. Qualifies leads and books viewings.
> Integrations needed: Google Calendar (booking viewings), venue details/pricing (knowledge base), optional CRM
---

##### 💼 Professional Services & Bookings
  11. Salon & Spa Booking Agent
  🟢 Beginner · Builder Track · WhatsApp · Instagram · Web Chat
  Appointment scheduling, stylist/therapist matching, service descriptions, and booking confirmation.
> Integrations needed: Google Calendar (availability + booking), service/staff data (knowledge base)
  12. Photography Session Booking
  🟢 Beginner · Builder Track · WhatsApp · Instagram · Web Chat
  Location selection, package browsing, session scheduling, and deposit collection.
> Integrations needed: Google Calendar (scheduling), Stripe (deposit collection), packages (knowledge base)
  13. Fitness & Wellness Class Booking
  🟡 Intermediate · Either Track · WhatsApp · Web Chat
  Class schedules, trainer profiles, membership tier handling, and pay-per-session checkout.
> Integrations needed: Google Calendar (class schedule), Stripe (payments), trainer/class data (knowledge base)
---

##### 🏦 Financial Services & Voice
  14. Fraud Alert Verification Agent
  🔴 Advanced · Developer Track · Voice (Outbound)
  Outbound voice agent that calls customers to confirm whether a flagged transaction was authorised. Handles verification flow, escalation to a human agent, and temporary card blocks. Inspired by BimpeAI's PrimoAI banking demo.
> Integrations needed: Transaction monitoring system (API), customer contact database, escalation email configuration
  15. Lost or Stolen Card Support
  🟡 Intermediate · Either Track · Voice (Inbound)
  Inbound voice agent for card loss reporting. Captures card details, initiates a block, logs the incident, and confirms replacement steps.
> Integrations needed: Card management API, incident logging system, escalation email
  16. Payment & Invoice Reminder Agent
  🟡 Intermediate · Developer Track · Voice (Outbound) · WhatsApp
  Automated outbound reminders for overdue invoices. Escalates through WhatsApp first, then voice call. Handles payment confirmation and receipt generation.
> Integrations needed: Invoice/billing system (API), Stripe (payment links), customer contact list
---

##### 🎧 Customer Support & Operations
  17. Marketplace Seller Support Agent
  🟡 Intermediate · Either Track · Web Chat
  Handle seller onboarding questions, listing issues, dispute resolution, and policy FAQs for e-commerce marketplaces.
> Integrations needed: Policy/FAQ documents (knowledge base upload), escalation email, optional CRM
  18. SaaS Helpdesk Agent
  🟡 Intermediate · Developer Track · Web Chat · WhatsApp
  First-line support for SaaS products: FAQ answers, ticket creation, status checks, and smart escalation routing based on issue type and customer tier.
> Integrations needed: Help docs/FAQ (knowledge base upload), ticketing system (API), escalation email
---

##### 💳 Payments & Checkout
  19. Booking with Stripe Payment
  🟡 Intermediate · Either Track · WhatsApp · Web Chat
  Calendar-aware booking flow with pay-before-book. Customers check available slots, select a time, pay, and receive confirmation — all in one conversation.
> Integrations needed: Google Calendar (availability), Stripe (payment processing)
  20. Subscription Management Agent
  🟡 Intermediate · Developer Track · Web Chat · Voice (Inbound)
  Handle plan upgrades, downgrades, cancellations, billing queries, and payment method updates. Useful for any subscription business.
> Integrations needed: Stripe (subscription management API), plan/pricing data (knowledge base), escalation email
---

#### How to Get Started on the Night
  1. Arrive by 5:30 PM — Meet fellow builders, and find your spot.
  1. 6:00 PM intro session — the BimpeAI team walks you through the platform, credits, and judging criteria.
  1. Pick your track — Builder (no-code) or Developer (API).
  1. Pick a workflow from this list (or bring your own idea).
  1. Clone it in the Agent Builder or create it via the API.
  1. Connect integrations — Google Calendar, Stripe, knowledge bases, or external APIs.
  1. Deploy to a channel — WhatsApp, Web Chat, or a live UK phone number.
  1. Demo at 8:00 PM — top builds get live feedback from judges.
---

#### Judging Criteria
  - Creativity — is the use case surprising, clever, or novel?
  - Execution — does the agent actually work end-to-end?
  - Business value — could a real business deploy this tomorrow?
  - Presentation — can you explain what you built and why it matters in 3 minutes?
---

#### Useful Links
  - BimpeAI Platform [BimpeAI Platform](https://bimpe.ai)
  - Agent Library (clone workflows) [Agent Library (clone workflows)](https://bimpe.ai/agent-library)
  - Agent Builder (no-code) [Agent Builder (no-code)](https://agent.bimpe.ai/)
  - Console API Docs [Console API Docs](https://docs.bimpe.ai/)
  - BimpeAI Dashboard (get API key) [BimpeAI Dashboard (get API key)](https://agent.bimpe.ai/)
  - Register on Luma [Register on Luma](https://luma.com/dnoe595m)
  - Remote Support [Remote Support](https://meet.google.com/zqk-wxqw-pyy)
  - Developer Loom Guide [Developer Loom Guide](https://www.loom.com/share/004b443e9fcb4ef4bcc5107678b7059b?start_download=true)
  - Usecases link [Usecases link](https://drive.google.com/drive/folders/1kVb_0pztVqyqF9tUkb37cc7w0EBZyd-a?usp=sharing)
---

#### Event Details
  📅 Date: Thursday, 25 June 2026
  🕐 Time: 5:30 PM – 9:00 PM
  📍 Location: Civo Tech Junction, First Floor, 32-37 Cowper St, London EC2A 4AW
---

#### Submit you Project here 
  Submission Form [Submission Form](https://buttered-planarian-d6e.notion.site/06aede5456264bef942d8d27d4fb6754?pvs=149)