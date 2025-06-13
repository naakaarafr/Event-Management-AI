import os
from dotenv import load_dotenv
import logging
import signal
import sys
import threading
import atexit

# Load environment variables
load_dotenv()

# Configuration settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Thread management
active_threads = []
shutdown_event = threading.Event()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal. Cleaning up...")
    shutdown_event.set()
    sys.exit(0)

def cleanup_threads():
    """Clean up active threads"""
    shutdown_event.set()
    for thread in active_threads:
        if thread.is_alive():
            thread.join(timeout=5)

# Register cleanup handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
atexit.register(cleanup_threads)

def validate_config():
    """Validate configuration with multiple API key options"""
    missing_vars = []
    
    # Check for at least one LLM API key
    if not GOOGLE_API_KEY and not OPENAI_API_KEY:
        missing_vars.append("GOOGLE_API_KEY or OPENAI_API_KEY")
    
    if not SERPER_API_KEY:
        missing_vars.append("SERPER_API_KEY")
    
    if missing_vars:
        logger.error("Missing required environment variables:")
        for var in missing_vars:
            logger.error(f"  - {var}")
        logger.error("\nPlease add these variables to your .env file")
        logger.info("\nFor Google Gemini API:")
        logger.info("  1. Go to https://ai.google.dev/")
        logger.info("  2. Get your API key")
        logger.info("  3. Check your quota limits")
        logger.info("\nFor OpenAI API (alternative):")
        logger.info("  1. Go to https://platform.openai.com/")
        logger.info("  2. Get your API key")
        logger.info("  3. Add credits to your account")
        return False
    
    # Log available APIs
    available_apis = []
    if GOOGLE_API_KEY:
        available_apis.append("Google Gemini")
    if OPENAI_API_KEY:
        available_apis.append("OpenAI")
    
    logger.info(f"Available LLM APIs: {', '.join(available_apis)}")
    return True

def check_api_quotas():
    """Check API quotas and provide recommendations"""
    logger.info("API Quota Recommendations:")
    logger.info("="*50)
    
    if GOOGLE_API_KEY:
        logger.info("Google Gemini API:")
        logger.info("  - Free tier: 15 requests/minute, 1M tokens/minute")
        logger.info("  - Paid tier: 1000 requests/minute, 4M tokens/minute")
        logger.info("  - Check quota: https://ai.google.dev/gemini-api/docs/rate-limits")
    
    if OPENAI_API_KEY:
        logger.info("OpenAI API:")
        logger.info("  - Rate limits vary by model and tier")
        logger.info("  - GPT-3.5-turbo: 3 requests/minute (free), 3500/minute (paid)")
        logger.info("  - Check usage: https://platform.openai.com/usage")
    
    logger.info("="*50)