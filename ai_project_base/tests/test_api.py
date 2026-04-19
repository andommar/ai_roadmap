from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_extract_email_endpoint():
    """
    Tests the /api/extract-email endpoint with a valid input.
    """
    input_text = "Hello my email is test@gmail.com, please contact me."

    response = client.post('/api/extract-email', json={"text": input_text})

    assert response.status_code == 200
    assert response.json() == {"extracted_email": "test@gmail.com"}

