# ebShield Backend

The ebShield backend is the control-plane API for the project. It stores users,
organizations, hosts, processes, and firewall rules in MongoDB, serves data to the
web interface, and synchronizes host state and policy with the ebShield agent.

The service is built with FastAPI, Beanie, MongoDB, Pydantic, and JWT authentication.

## API boundaries

The backend deliberately exposes two API surfaces under `/api`. They share the same
database models, but serve different clients and purposes.

| API | Base path | Client | Purpose |
| --- | --- | --- | --- |
| UI API | `/api/ui` | React frontend and human users | Authentication, organization management, dashboards, browsing agents and processes, and firewall-rule management |
| Host API | `/api/host` | ebShield agents running on protected hosts | Agent enrollment/status checks, process-state reporting, exclusion-list retrieval, and fetching rules for enforcement |

### `app/api/ui`: web control plane

`app/api/ui` contains the routes, services, repositories, and UI-specific models used
by the frontend. Its main route groups are:

- `/api/ui/auth` — register, log in, and refresh/validate the current JWT.
- `/api/ui/user` — read the current user and create an organization for that user.
- `/api/ui/organization` — create/read organizations and invite users.
- `/api/ui/agent` — list agents or read an agent, optionally embedding its processes.
- `/api/ui/process` — list processes for an agent or read a process, optionally
  embedding its rules.
- `/api/ui/rule` — create, read, update, and delete process firewall rules.
- `/api/ui/dashboard` — aggregated agent, process, rule, user, and location metrics.

The frontend sends its bearer token to this API. Registration and login are public;
most user, agent, process, rule, and dashboard operations are protected by the JWT
dependency. The organization router currently has no router-level JWT dependency,
which should be reviewed before a production deployment.

### `app/api/host`: agent synchronization API

`app/api/host` is not a second UI API. It is the machine-facing interface used by an
ebShield agent to announce a host, publish its observed process state, and retrieve
the policy data it needs to enforce rules locally.

Its current endpoints are:

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/host/agent/` | Register an agent/host |
| `GET` | `/api/host/agent/exists/{agent_id}` | Check whether an agent is registered |
| `GET` | `/api/host/agent/{agent_id}/processes-to-exclude` | Retrieve process names the agent should ignore |
| `PATCH` | `/api/host/process/agent/{agent_id}` | Synchronize the processes currently observed by an agent |
| `GET` | `/api/host/process/agent/{agent_id}/command/rules` | Retrieve rules grouped by process command for local enforcement |

No authentication dependency is currently attached to the host routes. Treat this
as a development-state interface and add agent authentication or an equivalent
trusted-network boundary before exposing it publicly.

## How the pieces fit together

```text
React frontend ── JWT requests ──> /api/ui ──┐
                                             ├── services/repositories ──> MongoDB
Host agent ── state and policy sync ─> /api/host ─┘
```

Shared persisted models live in `app/api/models`. Both API surfaces follow a
route → service → repository structure. Application startup, configuration,
authentication, logging, and database lifecycle code live in `app/core`.

## Requirements

- Python 3.12 or newer (the current source uses PEP 695 `type` aliases; although
  `pyproject.toml` presently declares Python 3.10+, Python 3.10 and 3.11 cannot parse
  those aliases)
- [Poetry](https://python-poetry.org/docs/#installation)
- A reachable MongoDB instance
- A Geo IP API key for agent-location enrichment

## Configuration

The application loads configuration from `backend/.env`. Start from
`.env.template`, then make sure the file contains all of the settings expected by
`app/core/config.py`:

```dotenv
HOST=0.0.0.0
PORT=8000
CONNECTION_STRING=mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000
DB_NAME=eb-shield
GEO_IP_API_KEY=replace-with-your-key

JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `JWT_` prefix is required because JWT settings use that environment prefix.
Do not commit `.env` or real secrets.

## Local development

From the `backend` directory:

```bash
poetry install
cp .env.template .env
# Update .env using the configuration above.
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Alternatively, `./scripts/run.sh` starts the development server on port `8080`.
Whichever port you choose must match the frontend's `VITE_BACKEND_URL`.

Once running:

- Health check: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI schema: `http://localhost:8000/openapi.json`
- Agent installer asset: `http://localhost:8000/static/install-agent.sh`

## Development commands

```bash
# Run the test suite
poetry run pytest

# Start the API with the repository helper (port 8080)
./scripts/run.sh
```

The `tests` package is currently a scaffold, so new behavior should be accompanied by
route/service tests as the suite is expanded.

## Project layout

```text
backend/
├── app/
│   ├── api/
│   │   ├── host/          # Agent-facing synchronization API
│   │   ├── ui/            # Frontend-facing control-plane API
│   │   ├── models/        # Shared Beanie/Pydantic domain models
│   │   └── errors/        # API exception types and handlers
│   ├── core/              # FastAPI setup, auth, config, DB, and logging
│   └── main.py            # ASGI entry point
├── scripts/               # Development/install helpers
├── static/                # Publicly served agent installer
├── tests/                 # Backend tests
├── pyproject.toml
└── poetry.lock
```

## Frontend connection

The frontend expects the backend origin, without an API suffix. For example:

```dotenv
VITE_BACKEND_URL=http://localhost:8000
```

The frontend appends `/api/ui` itself. The backend's development CORS configuration
already allows the Vite development and preview origins on ports `5173` and `4173`.
