from crew import event_management_crew
from config import validate_config, check_api_quotas, shutdown_event
from datetime import datetime
import logging
import time
import sys
import os
import signal
import threading
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
is_shutting_down = False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global is_shutting_down
    logger.info(f"Received signal {signum}. Initiating graceful shutdown...")
    is_shutting_down = True
    shutdown_event.set()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def get_user_input():
    """Collect event details from user input"""
    print("="*60)
    print("           EVENT MANAGEMENT SYSTEM")
    print("="*60)
    print("Please provide the following event details:\n")
    
    # Get event topic
    while True:
        if is_shutting_down:
            sys.exit(0)
        event_topic = input("Event Topic/Name: ").strip()
        if event_topic:
            break
        print("Please enter a valid event topic.")
    
    # Get event city
    while True:
        if is_shutting_down:
            sys.exit(0)
        event_city = input("Event City: ").strip()
        if event_city:
            break
        print("Please enter a valid city name.")
    
    # Get expected participants
    while True:
        if is_shutting_down:
            sys.exit(0)
        try:
            expected_participants = int(input("Expected Number of Participants: ").strip())
            if expected_participants > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get tentative date
    while True:
        if is_shutting_down:
            sys.exit(0)
        date_input = input("Tentative Date (YYYY-MM-DD): ").strip()
        try:
            # Validate date format and ensure it's in the future
            event_date = datetime.strptime(date_input, '%Y-%m-%d')
            if event_date.date() < datetime.now().date():
                print("Please enter a future date.")
                continue
            tentative_date = date_input
            break
        except ValueError:
            print("Please enter date in YYYY-MM-DD format (e.g., 2024-12-15).")
    
    # Get budget range with better validation
    while True:
        if is_shutting_down:
            sys.exit(0)
        budget_input = input("Budget in USD (e.g., 5000 or press Enter for $5000 default): ").strip()
        if not budget_input:
            budget = "$5000"
            break
        try:
            budget_amount = int(budget_input.replace('$', '').replace(',', ''))
            if budget_amount > 0:
                budget = f"${budget_amount}"
                break
            else:
                print("Please enter a positive amount.")
        except ValueError:
            print("Please enter a valid budget amount (numbers only).")
    
    # Get special requirements (optional)
    special_requirements = input("Special Requirements (optional): ").strip()
    if not special_requirements:
        special_requirements = "None specified"
    
    # Get event duration
    while True:
        if is_shutting_down:
            sys.exit(0)
        try:
            duration_hours = float(input("Event Duration in Hours (e.g., 6.0): ").strip())
            if duration_hours > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number (can include decimals, e.g., 2.5).")
    
    return {
        'event_topic': event_topic,
        'event_city': event_city,
        'expected_participants': expected_participants,
        'tentative_date': tentative_date,
        'budget': budget,
        'special_requirements': special_requirements,
        'duration_hours': duration_hours
    }

def display_event_summary(event_details):
    """Display a summary of the event details"""
    print("\n" + "="*60)
    print("           EVENT DETAILS SUMMARY")
    print("="*60)
    print(f"Event Topic:        {event_details['event_topic']}")
    print(f"City:               {event_details['event_city']}")
    print(f"Expected Attendees: {event_details['expected_participants']}")
    print(f"Date:               {event_details['tentative_date']}")
    print(f"Duration:           {event_details['duration_hours']} hours")
    print(f"Budget:             {event_details['budget']}")
    print(f"Special Requirements: {event_details['special_requirements']}")
    print("="*60)
    
    # Confirm with user
    while True:
        if is_shutting_down:
            sys.exit(0)
        confirm = input("\nAre these details correct? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            return True
        elif confirm in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def run_crew_safely(event_details, timeout_seconds=2400):  # 40 minute timeout
    """Run crew with timeout and error handling"""
    result = None
    error = None
    
    def crew_runner():
        nonlocal result, error
        try:
            logger.info("Starting crew execution...")
            logger.info(f"Event: {event_details['event_topic']} in {event_details['event_city']}")
            result = event_management_crew.kickoff(inputs=event_details)
            logger.info("Crew execution completed successfully")
        except Exception as e:
            error = e
            logger.error(f"Crew execution failed: {e}")
            # Log more details for debugging
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
    
    # Run crew in a separate thread with timeout
    crew_thread = threading.Thread(target=crew_runner, daemon=True)
    crew_thread.start()
    
    # Wait for completion or timeout with progress updates
    start_time = time.time()
    while crew_thread.is_alive():
        elapsed = int(time.time() - start_time)
        if elapsed > 0 and elapsed % 60 == 0:  # Update every minute
            logger.info(f"Crew still running... {elapsed//60} minutes elapsed")
        
        crew_thread.join(timeout=1)  # Check every second
        
        if elapsed >= timeout_seconds:
            logger.error("Crew execution timed out")
            return None, Exception(f"Crew execution timed out after {timeout_seconds//60} minutes")
    
    return result, error

def parse_crew_output(result):
    """Parse and format crew output for better display"""
    try:
        if hasattr(result, 'tasks_outputs'):
            outputs = {}
            for i, task_output in enumerate(result.tasks_outputs):
                task_name = ["Venue Search", "Logistics Planning", "Marketing Strategy"][i]
                outputs[task_name] = {
                    'summary': task_output.summary if hasattr(task_output, 'summary') else 'No summary',
                    'output': task_output.exported_output if hasattr(task_output, 'exported_output') else str(task_output)
                }
            return outputs
        else:
            return {"Result": str(result)}
    except Exception as e:
        logger.warning(f"Could not parse crew output: {e}")
        return {"Raw Output": str(result)}

def run_crew_with_retry(event_details, max_retries=2):
    """Run crew with retry logic for rate limiting"""
    for attempt in range(max_retries):
        if is_shutting_down:
            break
            
        try:
            logger.info(f"Starting crew execution (attempt {attempt + 1}/{max_retries})")
            print(f"\n🚀 Starting AI agents (attempt {attempt + 1}/{max_retries})...")
            print("This may take 10-15 minutes. Please be patient...\n")
            
            result, error = run_crew_safely(event_details)
            
            if result:
                return result
            elif error:
                error_msg = str(error)
                
                # Check for specific error types and handle them appropriately
                if any(term in error_msg.lower() for term in ["list", "attribute", "crewai"]):
                    logger.error("CrewAI internal error detected. This might be a version compatibility issue.")
                    if attempt < max_retries - 1:
                        logger.info("Retrying with simplified approach...")
                        time.sleep(10)  # Short wait before retry
                        continue
                    else:
                        raise Exception("CrewAI compatibility issue. Please check CrewAI version or configuration.")
                
                # Check if it's a rate limiting error
                elif any(term in error_msg.lower() for term in ["resourceexhausted", "429", "rate", "quota", "limit"]):
                    if attempt < max_retries - 1:
                        wait_time = min(60 * (2 ** attempt), 300)  # Max 5 minutes
                        logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds before retry...")
                        print(f"⏳ Rate limit hit. Waiting {wait_time} seconds...")
                        print("💡 Tip: Consider upgrading your API plan for faster processing")
                        
                        # Wait with periodic checks for shutdown
                        for i in range(wait_time):
                            if is_shutting_down:
                                return None
                            if i % 30 == 0:  # Update every 30 seconds
                                print(f"   Waiting... {wait_time - i} seconds remaining")
                            time.sleep(1)
                        continue
                    else:
                        logger.error("Max retries exceeded due to rate limiting")
                        raise Exception("API rate limit exceeded. Please try again later or upgrade your API plan.")
                
                # Check if it's an authentication error
                elif any(term in error_msg.lower() for term in ["authentication", "unauthorized", "api key", "invalid"]):
                    logger.error("Authentication failed. Please check your API keys.")
                    raise Exception("Invalid API key. Please check your .env file configuration.")
                
                # For timeout errors
                elif "timeout" in error_msg.lower():
                    if attempt < max_retries - 1:
                        logger.warning("Crew execution timed out. Retrying with extended timeout...")
                        continue
                    else:
                        raise Exception("Crew execution consistently timing out. Try reducing the scope or check your internet connection.")
                
                # For other errors, don't retry
                else:
                    logger.error(f"Unexpected error: {error_msg}")
                    raise error
            else:
                logger.error("Crew returned no result and no error")
                raise Exception("Crew execution failed with unknown error")
                
        except KeyboardInterrupt:
            logger.info("Execution interrupted by user")
            return None
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            print(f"❌ Attempt {attempt + 1} failed. Retrying...")
    
    return None

def display_results(event_details):
    """Display formatted results from output files"""
    print("\n" + "="*80)
    print("                    🎉 EVENT PLANNING COMPLETE! 🎉")
    print("="*80)
    
    # Venue Details
    if os.path.exists("venue_details.json"):
        print("\n📋 VENUE DETAILS")
        print("-" * 50)
        with open("venue_details.json", "r") as f:
            content = f.read()
            try:
                venue_data = json.loads(content)
                for key, value in venue_data.items():
                    if key == 'amenities':
                        print(f"Amenities: {', '.join(value)}")
                    else:
                        print(f"{key.replace('_', ' ').title()}: {value}")
            except json.JSONDecodeError:
                print("Warning: Invalid JSON format in venue_details.json")
                print("Raw output:")
                print(content)
    else:
        print("\n📋 VENUE DETAILS")
        print("-" * 50)
        print("❌ Venue details not generated")

    # Logistics Plan
    if os.path.exists("logistics_plan.md"):
        print("\n📋 LOGISTICS PLAN")
        print("-" * 50)
        with open("logistics_plan.md", "r") as f:
            content = f.read()
            print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("\n📋 LOGISTICS PLAN")
        print("-" * 50)
        print("❌ Logistics plan not generated")

    # Marketing Strategy
    if os.path.exists("marketing_strategy.md"):
        print("\n📋 MARKETING STRATEGY")
        print("-" * 50)
        with open("marketing_strategy.md", "r") as f:
            content = f.read()
            print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("\n📋 MARKETING STRATEGY")
        print("-" * 50)
        print("❌ Marketing strategy not generated")

    # Summary of Generated Files
    print("\n" + "="*80)
    print("📁 GENERATED FILES:")
    print("="*80)
    files_info = [
        ("venue_details.json", "Venue booking information"),
        ("logistics_plan.md", "Catering & equipment details"),
        ("marketing_strategy.md", "Promotion & outreach plan")
    ]
    files_created = False
    for filename, description in files_info:
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"✅ {filename} ({file_size} bytes) - {description}")
            files_created = True
        else:
            print(f"❌ {filename} - Not generated")
    
    if files_created:
        print("\n💡 Check the generated files for complete details!")
    else:
        print("\n⚠️ No output files were generated.")
    print("="*80)

def main():
    try:
        print("🤖 Welcome to the AI Event Management System!")
        print("This system uses AI agents to help plan your event.\n")
        
        # Show API quota information
        check_api_quotas()
        print("\n" + "="*60)
        
        # Get event details from user
        while True:
            if is_shutting_down:
                sys.exit(0)
            event_details = get_user_input()
            if display_event_summary(event_details):
                break
            print("\nLet's try again...\n")
        
        print("\n🚀 Starting AI Event Planning Agents...")
        print("📋 The AI agents will handle:")
        print("   1. 🏢 Venue Research & Booking")
        print("   2. 🍽️  Catering & Equipment Planning") 
        print("   3. 📱 Marketing & Promotion Strategy")
        print("\n⏳ This may take 10-20 minutes due to API rate limits.")
        print("📧 Press Ctrl+C to cancel at any time.\n")
        
        # Run the crew with retry logic
        result = run_crew_with_retry(event_details)
        
        if result and not is_shutting_down:
            display_results(event_details) 
            
            print("\n🎯 Next Steps:")
            print("1. Review the generated files for detailed information")
            print("2. Contact venues and vendors using the provided details")
            print("3. Execute the marketing plan 4-6 weeks before your event")
            print("4. Finalize bookings and confirm arrangements")
            
        elif not is_shutting_down:
            print("❌ Event planning failed after multiple attempts.")
            print("\n🔧 Try these troubleshooting steps:")
            print("1. Check your internet connection")
            print("2. Verify API keys in .env file")
            print("3. Wait a few minutes and try again")
            print("4. Reduce event scope (fewer participants, shorter duration)")
            
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        print("\n👋 Program interrupted. Exiting gracefully...")
    except Exception as e:
        logger.error(f"Crew execution failed: {e}")
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting suggestions:")
        print("1. Check your API keys in the .env file")
        print("2. Verify your API quota limits haven't been exceeded")
        print("3. Try again later if rate limited")
        print("4. Consider using a different LLM provider")
        print("5. Update CrewAI: pip install --upgrade crewai crewai-tools")
        print("6. Check your internet connection")
        sys.exit(1)
    finally:
        # Ensure clean shutdown
        shutdown_event.set()

if __name__ == "__main__":
    try:
        # Validate configuration
        if not validate_config():
            print("❌ Configuration validation failed. Please check your .env file.")
            sys.exit(1)
        
        main()
    except KeyboardInterrupt:
        print("\n👋 Program interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"💥 Fatal error: {e}")
        sys.exit(1)