# Week 2 Log — FastAPI + Pydantic

**Date completed:** 2025-05
**Status:** Done ✓

---

## What I built
- `main.py` — FastAPI server with two endpoints:
  - `GET /` — health check, returns `{"message": "hello world"}`
  - `POST /extract-email` — receives a text, extracts an email from it
- `schemas.py` — Pydantic models for request and response validation
- Integration tests using FastAPI's `TestClient`

---

## Questions I was asked — and my answers

**Q: What HTTP method does your extraction endpoint use, and why?**
A: POST, because the client is sending data to be processed. GET is for retrieving data from the server without sending a body.
*Correction: None — this was correct.*

**Q: What does `EmailExtractionRequest` look like? What fields does it have?**
A: It has one field: `text: str` — the raw text the user sends.
*Correction: None — correct, but I couldn't remember it cold. I had to re-read the file.*

**Q: What does `EmailExtractionResponse` look like?**
A: It has one field: `extracted_email: str | None = None` — the extracted email, or None if none was found.
*Correction: My actual code had `extracted_email: str = None` — missing the `| None`. That's a type annotation bug. The type said str but the value could be None. Fixed.*

**Q: Why use Pydantic models instead of plain dictionaries?**
A: "To ensure they follow the structure."
*Correction: Too vague. The real answer:*
- *Pydantic **validates** incoming data automatically — wrong types are rejected before your code runs*
- *It **serializes** responses to JSON automatically*
- *Without it, you'd manually validate every field — fragile and error-prone*

**Q: What is `TestClient` and why use it instead of calling functions directly?**
A: First answer was confused ("we won't have to start a test client").
*Correction: TestClient lets you test your endpoints **in-process** — no server running, no network, no ports. It simulates the full HTTP request/response cycle internally. Tests run faster, no setup/teardown of a real server, and it works in CI/CD pipelines.*

---

## Bug fixed

**File:** `schemas.py`

```python
# Before (wrong)
extracted_email: str = None

# After (correct)
extracted_email: str | None = None
```

The type annotation was lying — it said `str` but the value could be `None`. Always use `str | None` when a field is optional.

---

## Main concepts learned

- **POST vs GET:** POST when the client sends data to process. GET when retrieving data.
- **Pydantic's real job:** Validation + serialization, not just "structure enforcement."
- **TestClient:** In-process HTTP simulation — no real server needed for tests.
- **Type annotations matter:** `str = None` and `str | None = None` are different. The first is a lie to the type system.

---

## What to remember next week
- Read first, explain back, then build.
- If you can't explain what your code does without opening the file, you don't own it yet.


# Week 3 Log — Persistence & PostgreSQL

**Date completed:** 31-05-2026
**Status:** Done ✓

---

## What I built
- `db_repository.py` — manages database connections and queries:
  - `log_extraction()` — inserts a new entry into the database after each extraction
  - `get_history()` — returns the last N extraction records ordered by date
- `main.py` — updated to wrap `log_extraction()` in a `try/except` so a database
  failure never crashes the extraction endpoint
- `.env` — stores `DATABASE_URL` outside of source code
- `extraction_log` table in PostgreSQL with columns: `id`, `input_text`, `email`, `created_at`

---

## Questions I was asked — and my answers

**Q: What is SQL injection and how does psycopg protect you from it?**
A: SQL injection is when a user sends input that contains SQL commands, which then
get executed by the database. psycopg protects against this by sending the query
template and the values separately — PostgreSQL parses the query structure first,
then receives the values as plain data. By the time the values arrive, it's too late
to inject anything. `%s` is psycopg's syntax for the parameter slots.
*Correction: None — correct.*

**Q: What's the difference between `execute()` and `commit()` — why do both exist?**
A: `execute()` runs the command but leaves it in a pending transaction — only visible
to the current connection, not written permanently. `commit()` makes it permanent and
visible to everyone.
*Correction: The key addition — without a commit, a crash automatically rolls back
the transaction. That's intentional. Partial writes are worse than no writes.*

**Q: Why is `DATABASE_URL` in a `.env` file and not in the code?**
A: Because hardcoded credentials get exposed in Git — even if deleted later, the
history remembers.
*Correction: None — correct.*

**Q: What does `load_dotenv()` actually do?**
A: Finds the nearest `.env` file, reads it, and loads the variables into the process
environment so `os.getenv()` can access them.
*Correction: `load_dotenv()` does NOT detect which environment you're on (dev/staging/prod).
It simply loads the file. It also doesn't overwrite variables already set by the system,
which is why it's safe in production — real environment variables take priority.*

**Q: Why does `log_extraction()` sit inside a `try/except` in the endpoint?**
A: Because logging is infrastructure, not the core feature. If the insert fails, the
user should still get their extraction result. The error gets logged internally.
*Correction: None — correct.*

**Q: What columns does `extraction_log` have? What does Python send vs the database?**
A: Columns: `id`, `input_text`, `email`, `created_at`.
Python sends: `input_text`, `email`.
Database generates automatically: `id` (SERIAL), `created_at` (DEFAULT NOW()).
*Correction: None — correct.*

---

## Main concepts learned

- **SQL injection:** User input that contains SQL commands can destroy your database
  if pasted directly into a query. Always use parameterized queries (`%s`) — never
  f-strings for SQL.
- **Parameterized queries:** psycopg sends the query template and values separately.
  PostgreSQL parses the structure first, then fills the slots. Values can never become
  commands.
- **Transactions:** `execute()` creates a pending change. `commit()` makes it permanent.
  A crash before commit = automatic rollback. This is a safety feature.
- **Connection pool:** Keeps connections alive for the lifetime of the app. Requests
  borrow a connection from the pool instead of opening a new one each time — much faster
  under load.
- **Environment variables:** Credentials never go in source code. `.env` + `load_dotenv()`
  + `.gitignore` is the minimum viable pattern for local development.
- **Separation of concerns:** Logging failure should not cause extraction failure. The
  `try/except` pattern around infrastructure calls is a professional habit.

---

## What to remember next week

- Week 4 is Docker and CI — the goal is to containerize the service and add a GitHub
  Actions pipeline.
- Check the database is running before starting the server: `sudo service postgresql start`
- To inspect data directly in psql:
```bash
  sudo -u postgres psql -d ai_engineer
  SELECT * FROM extraction_log ORDER BY created_at DESC LIMIT 10;
```
- To start the server: run from the project root, not from inside `src/`
```bash
  uvicorn src.main:app --reload
```