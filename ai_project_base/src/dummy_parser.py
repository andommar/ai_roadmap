from src.core.logger import get_logger

logger = get_logger(__name__)

def extract_email (text: str) -> str | None:
    logger.info(f"Looking for email: '{text}'")

    if not text:
        logger.warning("It is not a text!")
        return None
    

    words = text.split()

    for word in words:
        if "@" in word and "." in word:
            logger.info(f"Found potential email: {word}")
            return word.strip('.,')
    
    
    logger.info("No email found in the provided text.")
    return None    