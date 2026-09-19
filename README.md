# OpsTrack

**OpsTrack** is a lightweight Task & Incident Management Platform built for a
small engineering / operations team. It's the kind of internal tool a team
might use to track day-to-day work (tasks) alongside production issues
(incidents) in one place, with a simple dashboard to see the current state
of both at a glance.

This repository contains the **application only** (backend + frontend +
database schema). It is intentionally built to be simple, testable, and
easy to containerize so it can serve as a realistic base for a separate
DevOps/production-deployment implementation (CI/CD, Docker, Kubernetes,
AWS, monitoring, etc.) — see the [`DevOps Implementation`](#devops-implementation)
section at the bottom.

---

## What problem does it solve?

Small ops/engineering teams often bounce between a task tracker and an
incident channel with no shared view of "what's on fire" vs. "what's
in progress." OpsTrack combines both into one small app with:

- A single login for the team
- Shared tasks with status/priority
- Shared incidents with severity/status and a resolved timestamp
- Comments/notes on both tasks and incidents (for handoffs and context)
- A dashboard summarizing where things stand

---

## Features

- Email/password registration and login (JWT-based auth)
- Task CRUD: title, description, status (`todo`, `in_progress`, `blocked`,
  `done`), priority (`low`, `medium`, `high`, `critical`), assignee
- Incident CRUD: title, description, severity (`sev1`–`sev4`), status
  (`open`, `investigating`, `mitigated`, `resolved`, `closed`), assignee,
  automatic `resolved_at` timestamp
- Comments/notes attachable to either a task or an incident
- Dashboard/statistics endpoint (counts by status/priority/severity, open
  incidents, stale tasks)
- Health endpoints for monitoring/deployment (`/health`, `/health/db`)
- Structured request logging
- Environment-variable based configuration (no hard-coded secrets)
- Automated backend test suite (pytest, 26 tests)
- Interactive API documentation (Swagger UI / ReDoc)
- Docker-ready backend and frontend, plus a simple docker-compose stack
  for local development

---

## Architecture

```text
React (Vite) Frontend
        |
        |  HTTPS / JSON (Axios)
        v
FastAPI Backend  (REST API, JWT auth, business logic)
        |
        |  SQLAlchemy ORM
        v
PostgreSQL
```

Deliberately simple: no microservices, no message queues, no cache layer,
no third-party auth provider, single database. This keeps the application
itself out of the way so the DevOps work (the actual point of the
portfolio project) is the interesting part.

### Data model

```text
users        (id, email, full_name, hashed_password, is_active, created_at)
tasks        (id, title, description, status, priority,
              created_by_id -> users, assigned_to_id -> users,
              created_at, updated_at)
incidents    (id, title, description, severity, status,
              created_by_id -> users, assigned_to_id -> users,
              created_at, updated_at, resolved_at)
comments     (id, entity_type ["task"|"incident"], entity_id,
              body, author_id -> users, created_at)
```

---

## Repository structure

```text
opstrack/
│
├── backend/
│   ├── app/
│   │   ├── api/routes/       # auth, users, tasks, incidents, comments, dashboard, health
│   │   ├── core/             # config, security (JWT/hashing), logging
│   │   ├── db/                # SQLAlchemy engine/session
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   └── main.py            # FastAPI app, middleware, router wiring
│   ├── tests/                 # pytest suite (26 tests)
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── api/                # axios client + typed resource helpers
│   │   ├── components/         # Navbar, PrivateRoute, Badge, ErrorBanner
│   │   ├── context/             # AuthContext
│   │   ├── pages/                # Login, Register, Dashboard, Tasks, TaskDetail,
│   │   │                          # Incidents, IncidentDetail, Profile
│   │   └── styles/global.css
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf              # used by the production build stage of the Dockerfile
│   └── Dockerfile
│
├── docs/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## Backend setup (local, without Docker)

Requirements: Python 3.11+, a running PostgreSQL instance (or use
docker-compose just for the `db` service).

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# copy env vars and edit as needed (see "Environment variables" below)
cp ../.env.example .env

# run the API (auto-reload for development)
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Database tables are
created automatically on startup (`Base.metadata.create_all`) — there is no
separate migration step required for local development.

## Frontend setup (local, without Docker)

Requirements: Node.js 20+.

```bash
cd frontend
npm install
cp .env.example .env    # set VITE_API_URL if the backend isn't on localhost:8000
npm run dev
```

The app will be available at `http://localhost:5173`.

## Database setup

Any PostgreSQL 14+ instance works. The quickest local option is the
`db` service in `docker-compose.yml`:

```bash
docker compose up -d db
```

Then point `DATABASE_URL` at it (see `.env.example`). The backend creates
its own schema on startup, so no manual `CREATE TABLE` steps are needed.

## Running everything with docker-compose

```bash
cp .env.example .env   # adjust values if you like
docker compose up --build
```

This starts PostgreSQL, the FastAPI backend, and an Nginx-served
production build of the frontend. This compose file is meant for local
application development/demo convenience — it is not a production
deployment configuration.

---

## Environment variables

Copy `.env.example` to `.env` (root) and, for local non-Docker development,
also into `backend/.env` / `frontend/.env` as needed. **Never commit a real
`.env` file** — secrets must always come from the environment.

| Variable | Used by | Description | Example |
|---|---|---|---|
| `DATABASE_URL` | backend | SQLAlchemy connection string | `postgresql+psycopg2://opstrack:opstrack@localhost:5432/opstrack` |
| `JWT_SECRET` | backend | Secret used to sign JWT access tokens | a long random string |
| `APP_ENV` | backend | `development` / `test` / `production` | `development` |
| `API_PORT` | backend / compose | Port the API listens on | `8000` |
| `LOG_LEVEL` | backend | Python logging level | `INFO` |
| `CORS_ORIGINS` | backend | Comma-separated list of allowed frontend origins | `http://localhost:5173` |
| `VITE_API_URL` | frontend | Base URL the frontend calls for the API | `http://localhost:8000` |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` / `POSTGRES_PORT` | docker-compose `db` service | Postgres container config | see `.env.example` |

---

## How to run tests

```bash
cd backend
pip install -r requirements.txt   # if not already installed
pytest
```

The suite (26 tests) runs against an isolated in-memory SQLite database
(configured in `tests/conftest.py`), so it never touches a real
PostgreSQL instance and needs no extra setup. It covers:

- Registration, duplicate-email rejection, login (success/failure), auth
  requirement on protected routes
- Health endpoint and DB health endpoint
- Task creation, retrieval, listing, invalid input, status update,
  invalid status rejection, deletion
- Incident creation, retrieval, listing, invalid severity rejection,
  resolving (and the `resolved_at` timestamp behavior)
- Comments on tasks, and rejecting comments on a non-existent entity
- Dashboard statistics, including the auth requirement

## API documentation

Once the backend is running, interactive docs are available at:

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- Raw OpenAPI schema: `http://localhost:8000/api/openapi.json`

## API overview

```text
/api/auth/register        POST    Create a user, returns a JWT
/api/auth/login           POST    Log in, returns a JWT
/api/auth/me              GET     Current authenticated user

/api/users                GET     List active users (for assignee pickers)
/api/users/{id}           GET     Get a single user

/api/tasks                GET     List tasks (filter by status/priority/assigned_to_id)
/api/tasks                POST    Create a task
/api/tasks/{id}           GET     Get a task
/api/tasks/{id}           PATCH   Update a task (status/priority/assignee/etc.)
/api/tasks/{id}           DELETE  Delete a task

/api/incidents             GET     List incidents (filter by status/severity/assigned_to_id)
/api/incidents             POST    Create an incident
/api/incidents/{id}        GET     Get an incident
/api/incidents/{id}        PATCH   Update an incident
/api/incidents/{id}        DELETE  Delete an incident

/api/comments               GET     List comments for a task or incident
/api/comments               POST    Add a comment to a task or incident
/api/comments/{id}          DELETE  Delete your own comment

/api/dashboard/stats         GET     Aggregate statistics for the dashboard
```

All routes except `/`, `/health`, `/health/db`, `/api/auth/register` and
`/api/auth/login` require a `Authorization: Bearer <token>` header.

## Health endpoints

These exist specifically to support later DevOps monitoring/deployment
work (container health checks, load balancer health checks, Kubernetes
probes):

- `GET /health` — liveness: is the process up and serving requests? Always
  returns `200` if the app is running.
- `GET /health/db` — readiness: can the app reach PostgreSQL? Returns `200`
  with `{"status": "ok", "database": "reachable"}` when it can, `503` when
  it cannot.

## Logging

The backend logs structured, single-line entries to stdout for:

- Every request (method, path, status code, duration, client)
- Application startup/shutdown
- Key business events (user registered, login success/failure, task/incident
  created/updated/deleted, comment created)
- Unhandled exceptions (with traceback)

No log shipping or aggregation (ELK/Loki/CloudWatch/etc.) is implemented
here — logs go to stdout so any log collector can pick them up later.

---

## DevOps Implementation

This section will be completed separately as part of the production
deployment and DevOps implementation.

---

## Developer Handoff for DevOps Engineer

**How to start the application (local dev, no Docker)**

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

**How to start the application (Docker / docker-compose)**

```bash
cp .env.example .env
docker compose up --build
```

**Required environment variables**

See the [Environment variables](#environment-variables) table above.
At minimum for a working deployment you need: `DATABASE_URL`, `JWT_SECRET`,
`APP_ENV`, `CORS_ORIGINS` (backend) and `VITE_API_URL` (frontend, baked in
at build time since it's a static SPA build).

**Ports used**

| Service | Port | Notes |
|---|---|---|
| Backend (FastAPI/uvicorn) | `8000` | configurable via `API_PORT` |
| Frontend dev server (Vite) | `5173` | local dev only |
| Frontend production (Nginx, in Docker) | `80` (mapped to host `3000` in docker-compose) | serves the built SPA |
| PostgreSQL | `5432` | configurable via `POSTGRES_PORT` |

**Database requirements**

- PostgreSQL 14+ (developed/tested against `postgres:16-alpine`)
- One database/user is sufficient; no extensions required
- Schema is created automatically on backend startup via
  `Base.metadata.create_all()` — there is currently **no migration
  tool** (e.g. Alembic) wired in. If you introduce one for production,
  note that the startup auto-create should be disabled/guarded to avoid
  conflicting with migrations.

**Test command**

```bash
cd backend && pytest
```

26 tests, run against an isolated in-memory SQLite DB, no external
dependencies required. Good candidate for a CI pipeline step; also a
reasonable place to wire in SonarQube/coverage reporting.

**Health endpoints**

- `GET /health` — liveness probe
- `GET /health/db` — readiness probe (checks DB connectivity, returns 503
  when the DB is unreachable)

**Build commands**

```bash
# Backend image
docker build -t opstrack-backend ./backend

# Frontend image (VITE_API_URL is baked in at build time)
docker build --build-arg VITE_API_URL=https://your-api.example.com -t opstrack-frontend ./frontend
```

**Runtime commands**

```bash
# Backend container
docker run -p 8000:8000 \
  -e DATABASE_URL=... \
  -e JWT_SECRET=... \
  -e APP_ENV=production \
  opstrack-backend

# Frontend container
docker run -p 3000:80 opstrack-frontend
```

**Assumptions**

- Single PostgreSQL database, single backend replica assumed for local
  dev; the app is stateless (JWT-based auth, no server-side sessions) so
  it should horizontally scale without extra work once behind a load
  balancer.
- The frontend is a static SPA build served by Nginx; `VITE_API_URL` is
  baked in at build time (standard Vite behavior), so a new frontend image
  build is required if the backend's public URL changes.
- CORS is currently controlled by a comma-separated `CORS_ORIGINS` env var;
  update it to match wherever the frontend is actually hosted in each
  environment.

**Known limitations (intentional, to keep the app simple)**

- No database migration tool - schema changes currently require either
  wiping the dev DB or hand-rolling a migration; worth introducing Alembic
  before this goes into a real production/CI pipeline with persistent data.
- No rate limiting, CSRF protection beyond JWT bearer auth, or refresh
  tokens - access tokens are long-lived (8 hours by default) bearer JWTs.
- No file/image attachments on tasks or incidents.
- No role-based access control - any authenticated user can view/edit any
  task or incident (comments can only be deleted by their author).
- No pagination on list endpoints yet - fine at small/demo scale, would
  need adding before large datasets.
- Logging goes to stdout only; no log shipping, metrics, tracing, or
  alerting is implemented (intentionally left for the DevOps
  implementation phase).
