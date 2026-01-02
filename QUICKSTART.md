# TrustStep AI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites

- **Node.js** 20+ or 22+ ([Download](https://nodejs.org/))
- **Python** 3.10+ ([Download](https://python.org/))
- **Docker** & Docker Compose ([Download](https://www.docker.com/))
- **Git** ([Download](https://git-scm.com/))

### Option 1: Docker (Recommended - Easiest)

```bash
# 1. Navigate to project
cd truststep-ai-full

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env with your API keys (optional but recommended)
nano .env  # or use your preferred editor

# Add your API keys:
# OPENAI_API_KEY=sk-your-key-here
# ANTHROPIC_API_KEY=sk-ant-your-key-here

# 4. Start everything with Docker
docker-compose up -d

# 5. Wait 30 seconds for services to start, then open:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Flower (Celery): http://localhost:5555
```

That's it! 🎉

### Option 2: Manual Setup (More Control)

#### Step 1: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_sm

# Setup environment
cp ../.env.example .env
# Edit .env with your settings

# Run database migrations (if PostgreSQL is running)
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at: http://localhost:8000

#### Step 2: Setup Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be running at: http://localhost:3000

#### Step 3: Start Celery Worker (Optional)

For background tasks, open another terminal:

```bash
cd backend
source venv/bin/activate  # Activate venv

# Start Celery worker
celery -A app.tasks worker -l info
```

#### Step 4: Start Flower (Optional)

For monitoring Celery tasks:

```bash
cd backend
source venv/bin/activate

# Start Flower
celery -A app.tasks flower
```

Flower UI: http://localhost:5555

## 🧪 Testing the Application

### Test Fraud Detection

1. Open http://localhost:3000
2. Navigate to "Analysis" page
3. Enter a test message:

**Example Fraud Message:**
```
URGENT! Your bank account has been suspended due to suspicious activity. 
Click here immediately to verify your identity: http://fake-bank.tk/verify
You have 24 hours or your account will be permanently blocked!
```

The system should detect:
- ✅ Urgency tactics
- ✅ Fear/threat language
- ✅ Suspicious link
- ✅ Authority impersonation

**Example Safe Message:**
```
Hi, this is a reminder that your appointment with Dr. Smith is tomorrow at 3 PM.
Please arrive 10 minutes early. See you then!
```

The system should show low risk.

### Test API Directly

```bash
# Test health check
curl http://localhost:8000/health

# Test fraud analysis
curl -X POST http://localhost:8000/api/v1/fraud/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "URGENT! Your account will be closed!"}'
```

## 📊 View API Documentation

- Interactive API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Kill the process
kill -9 <PID>
```

### Docker Issues

```bash
# Stop all containers
docker-compose down

# Remove volumes and restart fresh
docker-compose down -v
docker-compose up -d --build
```

### Node.js Version Error

```bash
# Check version
node --version

# Should be 20.x or 22.x
# If not, install using nvm:
nvm install 20
nvm use 20
```

### Python Dependencies Fail

```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs db

# Recreate database
docker-compose down -v
docker-compose up -d db
```

## 🔑 API Keys Setup

### Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Create new API key
3. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

**Note:** The app works without API keys using rule-based detection, but LLM features will be disabled.

## 📁 Project Structure

```
truststep-ai-full/
├── frontend/              # React TypeScript app
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Page components
│   │   ├── ai/           # TensorFlow.js models
│   │   ├── services/     # API services
│   │   └── App.tsx       # Main app
│   └── package.json
│
├── backend/               # FastAPI Python app
│   ├── app/
│   │   ├── api/v1/       # API endpoints
│   │   ├── ml/           # ML models
│   │   ├── core/         # Configuration
│   │   └── main.py       # FastAPI app
│   └── requirements.txt
│
├── ml/                    # ML training
│   ├── notebooks/        # Jupyter notebooks
│   ├── models/           # Saved models
│   └── training/         # Training scripts
│
├── docker-compose.yml    # Docker orchestration
└── .env.example          # Environment template
```

## 🎯 Next Steps

1. ✅ Explore the API docs at http://localhost:8000/docs
2. ✅ Test fraud detection with various messages
3. ✅ Train custom ML models in `ml/` directory
4. ✅ Customize the frontend in `frontend/src/`
5. ✅ Add more fraud patterns in `backend/app/ml/fraud_model.py`
6. ✅ Deploy to production (see DEPLOYMENT.md)

## 💬 Need Help?

- 📖 Read full docs: `docs/` folder
- 🐛 Report issues: GitHub Issues
- 💡 Feature requests: GitHub Discussions
- 📧 Email: support@truststep-ai.com

## 🎉 You're Ready!

The TrustStep AI platform is now running. Start detecting fraud! 🛡️
