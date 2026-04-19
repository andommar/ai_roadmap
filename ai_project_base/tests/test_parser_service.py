# https://realpython.com/pytest-python-testing/

from src.services.parser_service import extract_email

def test_extract_email_with_valid_string():
    """
    Tests that the function correctly extracts an email from a simple sentence.
    """
    
    input_text = "Hello my email is test@gmail.com, please contact me."

    result = extract_email(input_text)

    assert result == "test@gmail.com"



def test_extract_email_with_no_email():
    """
    Tests that the function correctly reports a missing email from a simple sentence.
    """
    input_text = "Hello my email is email, please contact me."

    result = extract_email(input_text)

    assert result == None


def test_extract_email_with_on_invalid_format():
    """
    Tests that the function correctly reports a missing email from a simple sentence.
    """
    input_text = "My twitter is @hello"

    result = extract_email(input_text)

    assert result is None