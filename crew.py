from crewai import Crew, Process
from agents import venue_coordinator, logistics_manager, marketing_communications_agent
from tasks import create_tasks
import logging

logger = logging.getLogger(__name__)

def safe_step_callback(step):
    """Safe callback that handles different step object types"""
    try:
        # Check if step has task attribute
        if hasattr(step, 'task') and hasattr(step.task, 'description'):
            task_desc = step.task.description[:50].replace('\n', ' ')
            logger.info(f"Crew step completed: {task_desc}...")
        # Check if step is a task directly
        elif hasattr(step, 'description'):
            task_desc = step.description[:50].replace('\n', ' ')
            logger.info(f"Crew step completed: {task_desc}...")
        # If it's something else, just log that a step completed
        else:
            logger.info(f"Crew step completed: {type(step).__name__}")
    except Exception as e:
        logger.warning(f"Step callback error (non-critical): {e}")

def create_event_management_crew():
    """Create and configure the event management crew"""
    try:
        # Create tasks with the agents
        venue_task, logistics_task, marketing_task = create_tasks(
            venue_coordinator, 
            logistics_manager, 
            marketing_communications_agent
        )

        # Define the crew with agents and tasks
        crew = Crew(
            agents=[
                venue_coordinator,
                logistics_manager,
                marketing_communications_agent
            ],
            tasks=[
                venue_task,
                logistics_task,
                marketing_task
            ],
            process=Process.sequential,  # Sequential process for better reliability
            verbose=True,
            max_rpm=8,  # Conservative rate limiting
            share_crew=False,  # Disable crew sharing for privacy
            full_output=True,  # Get full output for better debugging
            step_callback=safe_step_callback,  # Safe callback function
            memory=False,  # Disable memory to avoid potential issues
            cache=False,  # Disable cache for fresh results
            max_execution_time=3600,  # 1 hour timeout for entire crew
        )
        
        logger.info("Event management crew created successfully")
        return crew
    
    except Exception as e:
        logger.error(f"Failed to create crew: {e}")
        raise e

# Create the crew instance
event_management_crew = create_event_management_crew()