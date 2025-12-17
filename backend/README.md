# Agentic Travel Agency Messenger Chatbot — Backend

FastAPI backend for a travel agency system (trips, clients, bookings, message history) designed to be used by a Facebook Messenger bot and an admin UI.

## Tech stack

- **FastAPI**: Python web API framework.
- **Uvicorn**: ASGI server (runs the FastAPI app).
- **PostgreSQL (Supabase)**: hosted SQL database.
- **SQLAlchemy**: ORM (Object-Relational Mapper — maps Python classes to database tables).
- **Pydantic**: request/response models + validation.
- **pytest**: unit tests.

## Repository layout (backend)

```
backend/
  app/
    main.py
    core/
      config.py
      database.py
    dbmodels/
      base.py
      trip.py
      client.py
      booking.py
      message.py
    services/
      trips.py
      clients.py
      bookings.py
      messages.py
    routes/
      trips.py
      clients.py
      bookings.py
      messages.py
    tests/
      conftest.py
      test_trip.py
      test_client.py
      test_booking.py
      test_message.py
  scripts/
    manual_test_trip.py
  requirements.txt
  .env
  .env.example
```

## Environment variables

Create `backend/.env` locally (never commit real secrets). A safe template lives in `.env.example`.

Example (`backend/.env.example`):

```env
DB_HOST=aws-1-eu-west-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.<YOUR_PROJECT_REF>
DB_PASSWORD=<YOUR_DB_PASSWORD>

GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
```

Notes:
- Use the **pooler** connection info (host + port 6543) if your network has IPv4 only.
- Keep credentials out of Git history.

## Install

From `backend/`:

```bash
python -m venv travel_agency_agent_venv
# Windows (PowerShell)
travel_agency_agent_venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Run the API

From `backend/app/`:

```bash
python main.py
```

Or:

```bash
uvicorn main:app --reload
```

API runs on:
- `http://localhost:8000`

Interactive docs:
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## CORS

CORS (Cross-Origin Resource Sharing — allows browser frontends from other domains) is enabled in `main.py` with `allow_origins=["*"]` for development.

For production, lock this down to your frontend domain(s).

## API endpoints

### Trips (`/trips`)
- `POST /trips` create trip
- `GET /trips/{trip_id}` get trip
- `GET /trips` list or search (query params)
- `PATCH /trips/{trip_id}` update trip
- `PATCH /trips/{trip_id}/active` activate/deactivate trip
- `POST /trips/{trip_id}/decrement-seats` decrement available seats
- `DELETE /trips/{trip_id}` delete trip

### Clients (`/clients`)
- `POST /clients` create client
- `POST /clients/get-or-create` get or create by Messenger PSID
- `GET /clients/{client_id}` get client
- `GET /clients/by-psid/{messenger_psid}` get by PSID
- `GET /clients` list clients
- `PATCH /clients/{client_id}` update client
- `DELETE /clients/{client_id}` delete client

**PSID**: Page-Scoped ID (unique per user per Facebook page).

### Bookings (`/bookings`)
- `POST /bookings` create booking (status = `pending`)
- `GET /bookings/{booking_id}` get booking
- `GET /bookings` list bookings (optional `client_id` or `trip_id`)
- `PATCH /bookings/{booking_id}` update booking (non-status fields)
- `POST /bookings/{booking_id}/confirm` confirm booking **and decrement trip seats**
- `POST /bookings/{booking_id}/cancel` cancel booking
- `DELETE /bookings/{booking_id}` delete booking

### Messages (`/messages`)
- `POST /messages` log a message (`direction`: `"in"` or `"out"`)
- `GET /messages/recent/{client_id}` recent messages (newest → oldest)
- `GET /messages/recent/{client_id}/chronological` recent messages (oldest → newest)

## Testing

### Unit tests (fast, local)

These tests run against **SQLite in-memory** (not Supabase) to validate service logic quickly.

From the repo root or from `backend/`:

```bash
python -m pytest
```

### Manual real-DB check (Supabase)

Run a one-off script that uses your real Supabase DB to validate connectivity + schema.

From `backend/app/`:

```bash
python ../scripts/manual_test_trip.py
```
