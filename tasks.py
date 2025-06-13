from crewai import Task

def create_tasks(venue_coordinator, logistics_manager, marketing_communications_agent):
    """Create all tasks for the event management crew"""
    
    # Task 1: Venue Coordination
    venue_task = Task(
        description=(
            "Find a specific venue in {event_city} that meets all criteria for {event_topic}. "
            "The venue must accommodate {expected_participants} participants for {duration_hours} hours "
            "on {tentative_date}. Budget consideration: {budget}. "
            "Special requirements: {special_requirements}. "
            "You MUST provide ONE specific venue with complete details including:\n"
            "- Exact venue name and address\n"
            "- Contact information (phone, email, website)\n"
            "- Capacity and pricing details\n"
            "- Available amenities\n"
            "- Booking availability status\n"
            "Return your response as a valid JSON string with this structure:\n"
            "{{\n"
            "  'name': 'venue name',\n"
            "  'address': 'venue address',\n"
            "  'capacity': 100,\n"
            "  'booking_status': 'Available',\n"
            "  'price_range': '$1000-$2000',\n"
            "  'amenities': ['WiFi', 'Parking'],\n"
            "  'contact_info': 'phone or email'\n"
            "}}"
        ),
        expected_output="A valid JSON string containing the venue details with fields: name, address, capacity, booking_status, price_range, amenities, contact_info",
        output_file="venue_details.json",
        agent=venue_coordinator,
        human_input=False
    )

    # Task 2: Logistics Management
    logistics_task = Task(
        description=(
            "Create comprehensive logistics plan for {event_topic} with {expected_participants} "
            "participants on {tentative_date} for {duration_hours} hours. Budget: {budget}. "
            "Special requirements: {special_requirements}. You must provide:\n"
            "- At least 3 specific catering options with vendor names and contact info\n"
            "- Complete equipment rental list with vendor recommendations\n"
            "- Detailed setup and breakdown timeline\n"
            "- Cost breakdown and vendor contact information\n"
            "- Dietary accommodation plans\n"
            "Return your response as a markdown-formatted string with clear sections."
        ),
        expected_output="A markdown string containing the logistics plan with catering options, equipment list, timeline, and cost breakdown",
        output_file="logistics_plan.md",
        agent=logistics_manager,
        context=[venue_task],
        human_input=False
    )

    # Task 3: Marketing Strategy
    marketing_task = Task(
        description=(
            "Develop comprehensive marketing strategy for {event_topic} in {event_city} "
            "on {tentative_date}. Target: professionals interested in the topic. "
            "Goal: engage {expected_participants} potential attendees. Budget: {budget}. "
            "Duration: {duration_hours} hours. Create actionable marketing plan with:\n"
            "- Target audience analysis\n"
            "- Multi-channel marketing strategy\n"
            "- Content calendar for 4 weeks pre-event\n"
            "- Budget allocation for different channels\n"
            "- Success metrics and KPIs\n"
            "Return your response as a markdown-formatted string with clear sections."
        ),
        expected_output="A markdown string containing the marketing strategy with audience analysis, channel strategy, content calendar, and KPIs",
        output_file="marketing_strategy.md",
        agent=marketing_communications_agent,
        context=[venue_task, logistics_task],
        human_input=False
    )
    
    return venue_task, logistics_task, marketing_task