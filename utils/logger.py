import logging
from datetime import datetime
import os

def setup_logger(log_dir: str = "logs"):
    """Configure logging to file with timestamped entries."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s => %(message)s",
        handlers=[
            logging.FileHandler(f"{log_dir}/pipeline.log"),
            logging.StreamHandler()
        ]
    )

def log_action(action: str, status: str, details: dict = None):
    """Log pipeline activities with structured metadata."""
    message = f"{action} | Status: {status}"
    if details:
        message += " | " + " | ".join(f"{k}: {v}" for k, v in details.items())
    logging.info(message)
    
def logger(func):
    def wrapper(*args, **kwargs):
        log_action(
            f"{func.__name__}ing {args[0].file}",
            "STARTED",
            {"class": func.__qualname__, "fun": ""}
        )
        try:
            result = func(*args, **kwargs)
            log_action("action", "COMPLETED", {"result": result})
            return result
        except Exception as e:
            log_action("action", "FAILED", {"error": str(e)})
            raise
    return wrapper