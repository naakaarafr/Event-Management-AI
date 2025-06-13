# 🎉 Event Management AI

*An intelligent multi-agent system for comprehensive event planning using AI*

## 📋 Overview

Event Management AI is a sophisticated system that leverages multiple AI agents to handle different aspects of event planning. Built with CrewAI, this system coordinates three specialized agents to research venues, manage logistics, and create marketing strategies for your events.

### 🤖 AI Agents

- **🏢 Venue Coordinator**: Finds and books appropriate venues with detailed contact information
- **🍽️ Logistics Manager**: Handles catering, equipment, setup, and vendor coordination  
- **📱 Marketing Agent**: Creates comprehensive marketing strategies and promotional plans

## ✨ Features

- **Multi-Agent Coordination**: Three specialized AI agents work together sequentially
- **Real-time Web Search**: Agents search the web for current venue and vendor information
- **Comprehensive Planning**: Covers venues, logistics, and marketing in one workflow
- **Output Generation**: Creates structured JSON and Markdown files with detailed plans
- **Error Handling**: Robust error handling with retry mechanisms and graceful shutdowns
- **API Flexibility**: Supports both Google Gemini and OpenAI APIs with automatic fallback
- **Rate Limit Management**: Intelligent handling of API rate limits with retry logic

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- API keys for at least one LLM provider (Google Gemini or OpenAI)
- Serper API key for web search functionality

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/naakaarafr/Event-Management-AI.git
   cd Event-Management-AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Choose at least one LLM provider
   GOOGLE_API_KEY=your_google_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Required for web search
   SERPER_API_KEY=your_serper_api_key_here
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🔑 API Setup

### Google Gemini API (Recommended)
1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create an API key
3. Free tier: 15 requests/minute, 1M tokens/minute
4. Add to `.env` as `GOOGLE_API_KEY`

### OpenAI API (Alternative)
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an API key and add credits
3. GPT-3.5-turbo: 3 requests/minute (free), 3500/minute (paid)
4. Add to `.env` as `OPENAI_API_KEY`

### Serper API (Required)
1. Visit [Serper.dev](https://serper.dev/)
2. Get your API key
3. Add to `.env` as `SERPER_API_KEY`

## 📁 Project Structure

```
event-management-ai/
├── main.py              # Main application entry point
├── agents.py            # AI agent definitions and configurations
├── tasks.py             # Task definitions for each agent
├── crew.py              # CrewAI crew setup and coordination
├── tools.py             # Web search and scraping tools
├── config.py            # Configuration management and validation
├── .env                 # Environment variables (create this)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎯 Usage

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Provide event details when prompted:**
   - Event topic/name
   - City location
   - Expected number of participants
   - Tentative date (YYYY-MM-DD format)
   - Budget in USD
   - Special requirements (optional)
   - Event duration in hours

3. **Wait for AI processing** (10-20 minutes)
   - The system will show progress updates
   - API rate limits may cause delays

4. **Review generated outputs:**
   - `venue_details.json` - Venue booking information
   - `logistics_plan.md` - Catering and equipment details
   - `marketing_strategy.md` - Promotion and outreach plan

## 📊 Output Examples

### Venue Details (JSON)
```json
{
  "name": "Conference Center Downtown",
  "address": "123 Main St, City, State 12345",
  "capacity": 150,
  "booking_status": "Available",
  "price_range": "$1500-$2500",
  "amenities": ["WiFi", "Parking", "AV Equipment"],
  "contact_info": "phone: (555) 123-4567"
}
```

### Logistics Plan (Markdown)
- Detailed catering options with vendor contacts
- Complete equipment rental lists
- Setup and breakdown timelines
- Cost breakdowns and dietary accommodations

### Marketing Strategy (Markdown)
- Target audience analysis
- Multi-channel marketing approach
- 4-week content calendar
- Budget allocation and success metrics

## ⚙️ Configuration

### Agent Settings
- **Max iterations**: 5 per agent
- **Execution timeout**: 10 minutes per agent
- **Process type**: Sequential (agents work one after another)
- **Rate limiting**: 8 requests per minute

### Timeout Settings
- **Individual agent**: 10 minutes
- **Total crew execution**: 1 hour
- **Retry attempts**: 2 with exponential backoff

## 🔧 Troubleshooting

### Common Issues

**"No LLM configured" Error**
- Ensure at least one API key (Google or OpenAI) is set in `.env`
- Check API key validity and quota limits

**Rate Limit Exceeded**
- The system automatically retries with delays
- Consider upgrading to paid API tiers for faster processing
- Free tier limits: Google (15/min), OpenAI (3/min)

**Crew Execution Timeout**
- Try reducing event scope (fewer participants, shorter duration)
- Check internet connection stability
- Verify API service status

**Missing Output Files**
- Check for API quota exhaustion
- Review logs for specific error messages
- Ensure all required environment variables are set

### Debug Mode
Enable detailed logging by modifying the logging level in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🛠️ Dependencies

### Core Frameworks
- `crewai` - Multi-agent orchestration framework
- `crewai-tools` - Web search and scraping capabilities
- `langchain-google-genai` - Google Gemini integration
- `langchain-openai` - OpenAI integration

### Utilities
- `python-dotenv` - Environment variable management
- `logging` - Comprehensive error tracking
- `threading` - Timeout and signal handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Performance Tips

### API Optimization
- Use Google Gemini for better free tier limits
- Monitor your API usage and quotas
- Consider upgrading to paid tiers for production use

### Event Planning Tips
- Be specific in event requirements for better results
- Provide realistic budgets for accurate vendor recommendations
- Plan events at least 4-6 weeks in advance

### System Performance
- Run during off-peak hours to avoid rate limits
- Ensure stable internet connection for web searches
- Close other resource-intensive applications

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI) framework
- Powered by Google Gemini and OpenAI language models
- Web search capabilities provided by Serper.dev

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs for specific error messages
3. Open an issue on GitHub with detailed error information
4. Include your system information and .env configuration (without API keys)

---

**Created by [@naakaarafr](https://github.com/naakaarafr)**
