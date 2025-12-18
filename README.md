# WhatsApp AI Chatbot

Multi-provider AI chatbot for WhatsApp Business API with support for Groq (free), OpenAI, and Claude.

## Features

- **Multi-Provider AI Support**: Switch between Groq, OpenAI, and Claude with a single config change
- **WhatsApp Business Integration**: Receive and respond to messages via WhatsApp Business API
- **Session-Based Conversations**: Maintains conversation context per user
- **Multi-Language**: Automatically detects and responds in user's language
- **Docker Support**: Deploy with a single command
- **Free Tier Available**: Use Groq for completely free AI inference

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  WhatsApp   │────▶│   FastAPI    │────▶│   Groq      │
│   User      │◀────│   Server     │◀────│   OpenAI    │
└─────────────┘     └──────────────┘     │   Claude    │
                           │              └─────────────┘
                    ┌──────┴──────┐
                    │  Webhook    │
                    │  (ngrok)    │
                    └─────────────┘
```

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **AI Providers**: Groq (Llama 3.3 70B), OpenAI (GPT-4o-mini), Claude (3.5 Sonnet)
- **Deployment**: Docker, Docker Compose
- **Testing**: ngrok for local webhook development

## Quick Start with Docker

### Prerequisites

1. **WhatsApp Business Account**
   - Meta Developer account
   - WhatsApp Business API access
   - Phone number verification

2. **AI Provider API Key** (choose one or more):
   - **Groq** (Free): https://console.groq.com
   - **OpenAI** (Paid): https://platform.openai.com
   - **Claude** (Paid): https://console.anthropic.com

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/semihalkanli/whatsapp-ai-chatbot.git
   cd whatsapp-ai-chatbot
   ```

2. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```

3. **Configure environment variables**
   Edit `.env` file with your credentials:
   ```env
   # WhatsApp Business API
   WHATSAPP_TOKEN=your_whatsapp_access_token
   WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
   WHATSAPP_VERIFY_TOKEN=your_custom_verify_token

   # AI Provider Selection: "groq" | "openai" | "claude"
   AI_PROVIDER=groq

   # API Keys (configure based on AI_PROVIDER)
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key  # Optional
   ANTHROPIC_API_KEY=your_anthropic_api_key  # Optional
   ```

4. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

5. **Check health**
   ```bash
   curl http://localhost:8000/health
   ```

## Manual Installation

### Prerequisites

- Python 3.11+
- pip

### Steps

1. **Clone and navigate**
   ```bash
   git clone https://github.com/semihalkanli/whatsapp-ai-chatbot.git
   cd whatsapp-ai-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## WhatsApp Business API Setup

### 1. Create Meta Developer App

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app → Select "Business" type
3. Add "WhatsApp" product to your app

### 2. Get API Credentials

1. Navigate to **WhatsApp → API Setup**
2. Copy the following:
   - **Temporary Access Token** → `WHATSAPP_TOKEN`
   - **Phone Number ID** → `WHATSAPP_PHONE_NUMBER_ID`
3. Create a custom verification token → `WHATSAPP_VERIFY_TOKEN`

### 3. Configure Webhook

1. **Expose your local server** (for development):
   ```bash
   # Install ngrok: https://ngrok.com
   ngrok http 8000
   ```
   Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

2. **Set up webhook in Meta**:
   - Go to **WhatsApp → Configuration → Webhook**
   - Callback URL: `https://abc123.ngrok.io/webhook`
   - Verify Token: Your `WHATSAPP_VERIFY_TOKEN`
   - Click "Verify and Save"

3. **Subscribe to webhook fields**:
   - Check "messages" field
   - Save changes

### 4. Test the Bot

Send a message to your WhatsApp Business number. The bot should respond!

## AI Provider Setup

### Groq (Free) - Recommended for Testing

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up (no credit card required)
3. Go to **API Keys** → Create new key
4. Copy the key to `.env` → `GROQ_API_KEY`
5. Set `AI_PROVIDER=groq`

**Free Tier**: 14,400 requests/day with Llama 3.3 70B

### OpenAI (Paid)

1. Visit [platform.openai.com](https://platform.openai.com)
2. Create account and add payment method
3. Go to **API Keys** → Create new secret key
4. Copy to `.env` → `OPENAI_API_KEY`
5. Set `AI_PROVIDER=openai`

**Cost**: ~$0.15 per 1M input tokens (GPT-4o-mini)

### Claude (Paid)

1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create account and add payment method
3. Go to **API Keys** → Create key
4. Copy to `.env` → `ANTHROPIC_API_KEY`
5. Set `AI_PROVIDER=claude`

**Cost**: ~$3 per 1M input tokens (Claude 3.5 Sonnet)

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `WHATSAPP_TOKEN` | WhatsApp Business API access token | ✅ | - |
| `WHATSAPP_PHONE_NUMBER_ID` | WhatsApp Business phone number ID | ✅ | - |
| `WHATSAPP_VERIFY_TOKEN` | Custom webhook verification token | ✅ | - |
| `AI_PROVIDER` | AI provider to use | ✅ | `groq` |
| `GROQ_API_KEY` | Groq API key | ⚠️ | - |
| `OPENAI_API_KEY` | OpenAI API key | ⚠️ | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | ⚠️ | - |
| `DEBUG` | Enable debug mode | ❌ | `false` |
| `LOG_LEVEL` | Logging level | ❌ | `info` |

⚠️ = Required based on `AI_PROVIDER` selection

### Switching AI Providers

Simply change the `AI_PROVIDER` variable in `.env`:

```env
AI_PROVIDER=groq      # Use Groq (free)
AI_PROVIDER=openai    # Use OpenAI (paid)
AI_PROVIDER=claude    # Use Claude (paid)
```

Restart the application for changes to take effect.

## Development

### Project Structure

```
whatsapp-ai-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── routers/
│   │   └── webhook.py       # WhatsApp webhook endpoints
│   ├── services/
│   │   ├── whatsapp.py      # WhatsApp API service
│   │   └── ai/
│   │       ├── __init__.py  # AI service & factory
│   │       ├── base.py      # Abstract base class
│   │       ├── groq.py      # Groq provider
│   │       ├── openai.py    # OpenAI provider
│   │       └── claude.py    # Claude provider
│   └── models/
│       └── messages.py      # Pydantic models
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

### Running in Development Mode

```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=debug

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing Webhook Locally

1. Start the server
2. Start ngrok: `ngrok http 8000`
3. Update webhook URL in Meta Developer Portal
4. Send test message from WhatsApp

## Troubleshooting

### Webhook not receiving messages

- Check ngrok is running and URL is correct
- Verify `WHATSAPP_VERIFY_TOKEN` matches Meta configuration
- Check webhook subscription includes "messages" field
- Look at ngrok web interface: `http://localhost:4040`

### AI responses not working

- Verify API key is correct for selected provider
- Check `AI_PROVIDER` matches configured API key
- Look at application logs: `docker-compose logs -f`
- Test API key directly with provider's API

### Docker build fails

- Ensure Docker and Docker Compose are installed
- Check `.env` file exists and is configured
- Try rebuilding: `docker-compose build --no-cache`

### Rate limiting issues

- **Groq Free**: 14,400 req/day - Use for testing only
- **OpenAI**: Increase quota in billing settings
- **Claude**: Check usage limits in console

## Production Deployment

### Recommendations

1. **Use paid AI provider** (OpenAI or Claude) for reliability
2. **Deploy on cloud**:
   - AWS ECS, Google Cloud Run, or Azure Container Apps
   - Use managed PostgreSQL for conversation persistence (optional enhancement)
3. **Set up monitoring**:
   - Health check endpoint: `/health`
   - Log aggregation (CloudWatch, Stackdriver)
4. **Security**:
   - Use HTTPS (automatic with cloud providers)
   - Rotate API keys regularly
   - Set up proper firewall rules

### Environment Variables for Production

```env
DEBUG=false
LOG_LEVEL=warning
AI_PROVIDER=openai  # or claude
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with service info |
| `/health` | GET | Health check |
| `/webhook` | GET | Webhook verification (Meta) |
| `/webhook` | POST | Receive WhatsApp messages |

## License

MIT License - Feel free to use this project for commercial purposes.

## Support

For issues and questions:
- Open an issue on GitHub
- Check troubleshooting section above

## Acknowledgments

- [Meta WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Groq](https://groq.com) for free AI inference
- [FastAPI](https://fastapi.tiangolo.com/) framework
- [Anthropic Claude](https://www.anthropic.com)
- [OpenAI](https://openai.com)
