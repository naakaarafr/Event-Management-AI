from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from config import SERPER_API_KEY
import logging

logger = logging.getLogger(__name__)

# Initialize the tools with error handling
def initialize_search_tool():
    """Initialize search tool with proper error handling"""
    try:
        if not SERPER_API_KEY:
            logger.warning("SERPER_API_KEY not found, using default configuration")
            return SerperDevTool()
        
        search_tool = SerperDevTool(
            api_key=SERPER_API_KEY,
            n_results=5,  # Limit results to avoid overwhelming the agents
            safesearch='moderate'
        )
        logger.info("Search tool initialized successfully with API key")
        return search_tool
    except Exception as e:
        logger.error(f"Error initializing search tool: {e}")
        logger.info("Falling back to default search tool configuration")
        return SerperDevTool()

def initialize_scrape_tool():
    """Initialize scrape tool with proper error handling"""
    try:
        scrape_tool = ScrapeWebsiteTool(
            timeout=30,  # 30 second timeout
            wait_time=3  # Wait 3 seconds for page load
        )
        logger.info("Scrape tool initialized successfully")
        return scrape_tool
    except Exception as e:
        logger.error(f"Error initializing scrape tool: {e}")
        logger.info("Falling back to default scrape tool configuration")
        return ScrapeWebsiteTool()

# Initialize tools
search_tool = initialize_search_tool()
scrape_tool = initialize_scrape_tool()