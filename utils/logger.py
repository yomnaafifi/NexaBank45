import logging
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
            f"{func.__name__}ing {args[0].file_name}",
            "STARTED",
            {"row count": len(args[0].df), "fun": ""}
        )
        try:
            result = func(*args, **kwargs)
            log_action(f"{func.__name__}ed {args[0].file_name}",
                "COMPLETED",
                {"row count": len(args[0].df), "fun": ""})
            return result
        except Exception as e:
            log_action("action", "FAILED", {"error": str(e)})
            raise
    return wrapper