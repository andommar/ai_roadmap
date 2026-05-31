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