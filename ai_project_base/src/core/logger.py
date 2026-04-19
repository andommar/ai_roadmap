import logging
import sys


def get_logger (name: str) -> logging.Logger:
    """Configures and returns standard logger"""
    logger = logging.getLogger(name)

    # Only configure it if it hasn't been configured yet
    if not logger.handlers:
        logger.setLevel(logging.INFO) # Default level

        #Create console handler (print to terminal)
        console_handler = logging.StreamHandler(sys.stdout)
    
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Add formatter to handler, and handler to logger
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    
    
    return logger