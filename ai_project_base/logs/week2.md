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