# 🏦 Multi-Agent Hedge Fund Simulator

A production-ready, full-stack AI hedge fund simulator that uses specialized AI agents powered by multiple LLMs to analyze stocks, generate investment signals, and manage a simulated portfolio.

---

## Architecture

```
React Frontend (Next.js 14)
        ↓
NestJS API Gateway (TypeScript)
        ↓
Redis Queue (BullMQ)
        ↓
Python AI Workers (FastAPI)
        ↓
Multi-Agent Engine (LangChain)
        ↓
LLM Router (OpenAI / Claude / Groq)
        ↓
Financial Data (yfinance)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Monorepo** | pnpm workspaces + Turborepo |
| **Backend API** | NestJS (TypeScript) with Prisma ORM |
| **Frontend** | Next.js 14 (App Router) + Tailwind CSS + Recharts |
| **AI Agents** | Python (FastAPI) with LangChain |
| **Database** | PostgreSQL 16 |
| **Cache/Queue** | Redis 7 + BullMQ |
| **Real-time** | WebSockets (Socket.IO) |
| **Containerization** | Docker + Docker Compose |

---

## Features

- 📊 **Dashboard** – Real-time portfolio overview, market indices, agent activity feed
- 📈 **Stock Analysis** – Price charts, key metrics, and per-agent signal breakdown
- 💼 **Portfolio Management** – Holdings, trade execution, P&L tracking
- 🤖 **AI Agents** – 6 specialized agents (Fundamental, Technical, Sentiment, Risk, Sector, Portfolio Manager)
- 🔀 **LLM Router** – Automatic routing and fallback across OpenAI, Anthropic, and Groq
- ⚡ **Real-time Updates** – WebSocket-powered live agent decisions and portfolio changes
- 🐳 **Docker Ready** – One-command deployment with Docker Compose

---

## AI Agents

| Agent | Purpose |
|-------|---------|
| **Fundamental** | Analyzes P/E ratio, EPS growth, revenue trends, debt ratios |
| **Technical** | Analyzes RSI, MACD, Bollinger Bands, moving averages |
| **Sentiment** | Analyzes market sentiment using LLM reasoning |
| **Risk** | Calculates VaR, Sharpe ratio, max drawdown, beta |
| **Sector** | Analyzes sector rotation and relative strength vs ETF |
| **Portfolio Manager** | Meta-agent: aggregates all signals, produces final decision |

---

## Prerequisites

- Node.js 18+
- pnpm 8+
- Docker & Docker Compose
- Python 3.11+ (for local dev without Docker)
- At least one LLM API key (OpenAI, Anthropic, or Groq)

---

## Quick Start (Docker)

```bash
# 1. Clone the repository
git clone https://github.com/abhijeet-cr7/Multi-agent-hedge-fund-simulator.git
cd Multi-agent-hedge-fund-simulator

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# 3. Start all services
docker-compose up -d

# 4. Initialize the database
docker-compose exec api npx prisma db push

# 5. Open the app
open http://localhost:3000
```

---

## Manual Setup

```bash
# Install dependencies
pnpm install

# Set up environment
cp .env.example .env
# Fill in DATABASE_URL, REDIS_URL, JWT_SECRET, and LLM API keys

# Start database and Redis
docker-compose up -d postgres redis

# Push Prisma schema
pnpm db:push

# Start all services in development mode
pnpm dev
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |

### Stocks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stocks/:symbol` | Get latest stock data |
| GET | `/stocks/:symbol/history` | Get historical price data |
| GET | `/stocks/market/overview` | Market summary (SPY, QQQ, DIA, IWM) |

### Portfolio
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/portfolio` | Get user's portfolio with holdings |
| POST | `/portfolio/trade` | Execute a BUY or SELL trade |
| GET | `/portfolio/performance` | Portfolio performance metrics |

### Agents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/agents/decisions` | Get recent agent decisions |
| GET | `/agents/decisions/:symbol` | Get decisions for a specific stock |
| POST | `/agents/run` | Trigger agent analysis for a symbol |

### AI Callback
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai-callback/decision` | Receive agent decisions from Python AI |

### Python AI Service
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/analyze` | Analyze a stock with all agents |
| POST | `/analyze/:agent_type` | Analyze with a specific agent |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | Required |
| `JWT_SECRET` | JWT signing secret | Required |
| `OPENAI_API_KEY` | OpenAI API key | Optional |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | Optional |
| `GROQ_API_KEY` | Groq API key | Optional |
| `NEXT_PUBLIC_API_URL` | NestJS API URL for frontend | `http://localhost:3001` |
| `NEXT_PUBLIC_WS_URL` | WebSocket URL for frontend | `http://localhost:3001` |
| `PYTHON_AI_URL` | Python AI service URL | `http://localhost:8000` |

---

## Project Structure

```
Multi-agent-hedge-fund-simulator/
├── apps/
│   ├── api/          # NestJS backend
│   └── web/          # Next.js frontend
├── services/
│   └── python-ai/    # FastAPI + LangChain agents
├── docs/
│   └── QUICKSTART.md
├── docker-compose.yml
├── pnpm-workspace.yaml
└── turbo.json
```

---

## Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

---

## License

MIT
