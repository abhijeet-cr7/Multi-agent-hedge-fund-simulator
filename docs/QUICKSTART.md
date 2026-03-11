# Quick Start Guide

## Prerequisites

- Docker Desktop installed and running
- Git
- At least one LLM API key:
  - [Groq](https://console.groq.com) (free tier available — recommended for quick start)
  - [OpenAI](https://platform.openai.com)
  - [Anthropic](https://console.anthropic.com)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/abhijeet-cr7/Multi-agent-hedge-fund-simulator.git
cd Multi-agent-hedge-fund-simulator
```

---

## Step 2: Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in the required values:

```env
# Required
JWT_SECRET=your-random-secret-string-here

# At least one LLM key required
GROQ_API_KEY=gsk_your-groq-api-key     # Recommended — free tier

# Optional (fallbacks)
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
```

The database and Redis URLs are pre-configured for Docker and don't need to be changed.

---

## Step 3: Start All Services

```bash
docker-compose up -d
```

This will start:
- **PostgreSQL** on port `5432`
- **Redis** on port `6379`
- **NestJS API** on port `3001`
- **Next.js Web** on port `3000`
- **Python AI Service** on port `8000`

Wait for all services to start (~30-60 seconds).

---

## Step 4: Initialize the Database

```bash
docker-compose exec api npx prisma db push
```

---

## Step 5: Access the Application

Open your browser and navigate to:

**http://localhost:3000**

You'll see the Hedge Fund Simulator dashboard with:
- Portfolio summary
- Market overview
- Agent activity feed

---

## Step 6: Run Your First Analysis

### Option A: Via the Web UI

1. Navigate to the **Agents** page
2. Click "Run Analysis"
3. Enter a stock symbol (e.g., `AAPL`)
4. Watch the agents analyze the stock in real-time

### Option B: Via the API

First, create an account:
```bash
curl -X POST http://localhost:3001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "password123", "name": "Demo User"}'
```

Save the `accessToken` from the response, then trigger an analysis:
```bash
curl -X POST http://localhost:3001/agents/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"symbol": "AAPL"}'
```

### Option C: Directly via Python AI Service

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "NVDA", "agent_type": "all"}'
```

---

## Checking Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f python-ai
docker-compose logs -f api
```

---

## Stopping the Application

```bash
docker-compose down

# To also remove volumes (wipes database)
docker-compose down -v
```

---

## Troubleshooting

### Services not starting
```bash
docker-compose ps          # Check status
docker-compose logs api    # View API logs
```

### Database connection errors
Wait a few seconds for PostgreSQL to be ready, then re-run:
```bash
docker-compose exec api npx prisma db push
```

### Python AI service errors
Check that you have at least one valid LLM API key in your `.env` file.

### Port conflicts
If ports are already in use, modify the port mappings in `docker-compose.yml`.
