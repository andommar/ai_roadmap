from fastapi import FastAPI
from src.schemas import EmailExtractionRequest, EmailExtractionResponse
from src.services.parser_service import extract_email
from src.core.logger import get_logger
from src.db_repository import get_history, log_extraction

logger = get_logger(__name__)

app = FastAPI(title="Email Extraction API", version="1.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/history")
async def extract_history() -> list[dict]:
    return get_history()

@app.post("/api/extract-email")
async def extract_email_endpoint(request: EmailExtractionRequest) -> EmailExtractionResponse:
    logger.info(f"Recieved a request for email extraction with text: {request.text}")
    found_email = extract_email(request.text)
    try:
        log_extraction(request.text, found_email)
    except Exception as e:
        logger.error(f"Failed to log extraction to database:{e}")
    return EmailExtractionResponse(extracted_email=found_email)
