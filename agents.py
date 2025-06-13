from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from tools import search_tool, scrape_tool
from config import GOOGLE_API_KEY, OPENAI_API_KEY
import logging

logger = logging.getLogger(__name__)

def get_llm():
    """Get the best available LLM with proper error handling"""
    try:
        if GOOGLE_API_KEY:
            logger.info("Using Google Gemini LLM")
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.7,
                max_retries=3,
                request_timeout=120  # Increased timeout
            )
    except Exception as e:
        logger.warning(f"Error with Gemini LLM: {e}")
    
    try:
        if OPENAI_API_KEY:
            logger.info("Using OpenAI LLM as fallback")
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                openai_api_key=OPENAI_API_KEY,
                temperature=0.7,
                max_retries=3,
                request_timeout=120
            )
    except Exception as e:
        logger.warning(f"Error with OpenAI LLM: {e}")
    
    logger.warning("No LLM configured, using default")
    return None

# Get the LLM instance
llm = get_llm()

def create_venue_coordinator():
    """Create venue coordinator agent"""
    agent_kwargs = {
        "role": "Venue Coordinator",
        "goal": (
            "Identify and book an appropriate venue based on specific event requirements "
            "including capacity, budget, location, and special needs. Focus on finding "
            "ONE specific venue with complete details and contact information."
        ),
        "tools": [search_tool, scrape_tool],
        "verbose": True,
        "max_iter": 5,
        "max_execution_time": 600,  # 10 minute timeout
        "backstory": (
            "With a keen sense of space and understanding of event logistics, "
            "you excel at finding and securing the perfect venue that fits the event's theme, "
            "size, budget constraints, and special requirements. You have extensive knowledge "
            "of venue types, pricing, and availability across different cities. You always "
            "provide specific venue names, addresses, and contact details."
        )
    }
    
    if llm:
        agent_kwargs["llm"] = llm
    
    return Agent(**agent_kwargs)

def create_logistics_manager():
    """Create logistics manager agent"""
    agent_kwargs = {
        "role": "Logistics Manager",
        "goal": (
            "Manage all logistics for the event including catering, equipment, setup, "
            "and coordination based on specific requirements, budget, and timeline. "
            "Provide detailed vendor recommendations with specific contact information."
        ),
        "tools": [search_tool, scrape_tool],
        "verbose": True,
        "max_iter": 5,
        "max_execution_time": 600,
        "backstory": (
            "Organized and detail-oriented, you ensure that every logistical aspect "
            "of the event from catering to equipment setup is flawlessly executed to "
            "create a seamless experience. You have extensive experience with vendor "
            "management, dietary accommodations, technical requirements, and timeline "
            "coordination. You always provide specific vendor names and contact details."
        )
    }
    
    if llm:
        agent_kwargs["llm"] = llm
    
    return Agent(**agent_kwargs)

def create_marketing_agent():
    """Create marketing and communications agent"""
    agent_kwargs = {
        "role": "Marketing and Communications Agent",
        "goal": (
            "Create and execute comprehensive marketing strategies to promote events "
            "and engage target audiences within budget constraints and timeline requirements. "
            "Develop actionable marketing plans with specific tactics and measurable outcomes."
        ),
        "tools": [search_tool, scrape_tool],
        "verbose": True,
        "max_iter": 5,
        "max_execution_time": 600,
        "backstory": (
            "Creative and communicative, you craft compelling marketing campaigns and "
            "engage with potential attendees across multiple channels to maximize event "
            "exposure and participation. You have expertise in social media marketing, "
            "content creation, audience targeting, and measuring engagement metrics. "
            "You create detailed, actionable marketing plans."
        )
    }
    
    if llm:
        agent_kwargs["llm"] = llm
    
    return Agent(**agent_kwargs)

# Create agent instances
venue_coordinator = create_venue_coordinator()
logistics_manager = create_logistics_manager()
marketing_communications_agent = create_marketing_agent()