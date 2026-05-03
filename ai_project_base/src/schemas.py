from pydantic import BaseModel

class EmailExtractionRequest(BaseModel):
    text: str

class EmailExtractionResponse(BaseModel):
    # We use `str | None` to explicitly say it can be a string or None.
    # The `= None` sets the default value so Pydantic knows it's optional.
    extracted_email: str | None = None
