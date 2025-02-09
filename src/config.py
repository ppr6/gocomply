import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration constants
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-70b-8192")

# Logging configuration
def setup_logging(debug_mode=False):
    level = logging.DEBUG if debug_mode else logging.INFO
    
    # Clear any existing handlers
    logging.getLogger().handlers = []
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    # Set third-party loggers to WARNING unless in debug mode
    if not debug_mode:
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        logging.getLogger("groq").setLevel(logging.WARNING)

# Set up logging (default to non-debug mode)
setup_logging(debug_mode=False)

# Indian Financial Regulatory Bodies
REGULATORY_BODIES = {
    "RBI": "Reserve Bank of India",
    "SEBI": "Securities and Exchange Board of India",
    "PMLA": "Prevention of Money Laundering Act",
    "IRDAI": "Insurance Regulatory and Development Authority of India"
} 