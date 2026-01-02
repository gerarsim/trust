# TrustStep AI - Advanced Fraud Detection Platform

A full-stack AI-powered fraud detection system built with React, Python (FastAPI), and Machine Learning.

## 🚀 Features

- **Real-time Fraud Detection**: AI-powered analysis of transactions and messages
- **Hybrid AI**: Client-side (TensorFlow.js) + Server-side (PyTorch/TensorFlow) models
- **LLM Integration**: Claude and GPT for advanced reasoning
- **WebSocket Real-time**: Instant fraud alerts
- **Multi-modal Analysis**: Text, transactions, behavioral patterns
- **Explainable AI**: Clear explanations for all fraud predictions

## 📁 Project Structure

```
truststep-ai-full/
├── frontend/          # React + TypeScript + Vite
├── backend/           # FastAPI + Python + ML
├── ml/               # ML training and research
├── docs/             # Documentation
├── scripts/          # Utility scripts
└── docker-compose.yml
```

## 🛠️ Tech Stack

### Frontend
- React 18 + TypeScript
- Vite 5
- TailwindCSS + Radix UI
- TensorFlow.js
- Socket.IO Client
- Zustand (State Management)
- React Query

### Backend
- FastAPI
- PyTorch + TensorFlow
- Transformers (Hugging Face)
- PostgreSQL
- Redis
- Celery
- WebSocket

### ML/AI
- Scikit-learn
- SpaCy
- LangChain
- ChromaDB
- OpenAI & Anthropic APIs

## 🚀 Quick Start

### Prerequisites
- Node.js 20+ or 22+
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL 16
- Redis 7

### 1. Clone and Setup

```bash
# Clone the repository
cd truststep-ai-full

# Copy environment files
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start with Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Flower (Celery): http://localhost:5555
```

### 3. Manual Setup

#### Frontend
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Celery Worker
```bash
cd backend
celery -A app.tasks worker -l info
```

## 📚 Documentation

- [API Documentation](docs/API.md)
- [ML Model Training](docs/ML_TRAINING.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Architecture](docs/ARCHITECTURE.md)

## 🔒 Security

- JWT Authentication
- Rate Limiting
- HTTPS Only
- Environment Variables
- CORS Configuration
- SQL Injection Protection
- XSS Prevention

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm run test

# Backend tests
cd backend
pytest -v --cov=app

# ML model evaluation
cd ml
python evaluation/evaluate_models.py
```

## 📊 Monitoring

- Prometheus metrics: http://localhost:8000/metrics
- Celery monitoring: http://localhost:5555
- Logs: `logs/` directory

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

MIT License - see LICENSE file

## 👥 Authors

- Your Name - [Your GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- TensorFlow & PyTorch teams
- Hugging Face community
- FastAPI developers
- React community

## 📧 Support

For support, email support@truststep-ai.com or open an issue.
