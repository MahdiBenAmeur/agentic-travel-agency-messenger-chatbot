# Agentic Travel Agency Messenger Chatbot

## Project overview
This project is a Facebook Messenger chatbot for a travel agency, powered by AI agents.
It handles client conversations, trip search, booking, cancellation, and trip status checks.
The system is backed by a central database and an admin interface for management and analysis.

---

## Repository structure

```
agentic-travel-agency-messenger-chatbot/
├── backend/
├── frontend/
└── README.md
```

### backend/
Contains the server-side logic of the application.

Purpose:
- Handle Facebook Messenger webhooks and messages
- Process user intents (search, booking, cancellation, trip info)
- Run AI agent / multi-agent logic
- Manage database access (trips, bookings, clients, conversations)
- Expose APIs for the admin interface
- Log conversations and actions for analytics

This is the core of the system.

---

### frontend/
Contains the admin web interface.

Purpose:
- Enable or disable the chatbot
- Manage trips and voyages (add, update, delete)
- View and manage bookings
- Monitor conversations and system activity
- Display analytics and summaries
- Optional internal chatbot for staff queries

---

## Scope (current)
- Facebook Messenger chatbot
- Backend API and database
- Admin management interface
- No payment processing in the initial version

---

## Goal
Automate customer interactions for a travel agency while providing full control and visibility through an admin interface.
