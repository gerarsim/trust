#!/bin/bash

# Script to generate all remaining files for TrustStep AI

echo "Generating TrustStep AI project files..."

# Create frontend files
cat > frontend/src/App.tsx << 'EOF'
import { Routes, Route } from 'react-router-dom';
import { Toaster } from 'sonner';
import Dashboard from './pages/Dashboard';
import Analysis from './pages/Analysis';
import Settings from './pages/Settings';
import Login from './pages/Login';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      <Toaster />
    </>
  );
}

export default App;
EOF

cat > frontend/src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
EOF

# Create AI service
cat > frontend/src/ai/fraudDetector.ts << 'EOF'
import * as tf from '@tensorflow/tfjs';
import { io, Socket } from 'socket.io-client';

export interface FraudResult {
  riskScore: number;
  riskLevel: 'safe' | 'warning' | 'danger';
  confidence: number;
  detectedPatterns: string[];
  recommendations: string[];
}

export class FraudDetectorAI {
  private model: tf.LayersModel | null = null;
  private socket: Socket;
  private readonly API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  constructor() {
    this.socket = io(this.API_URL);
  }

  async loadModel() {
    try {
      this.model = await tf.loadLayersModel('/models/fraud-model.json');
      console.log('✅ TensorFlow.js model loaded');
    } catch (error) {
      console.error('Failed to load model:', error);
    }
  }

  async analyzeLocal(text: string): Promise<number> {
    if (!this.model) {
      await this.loadModel();
    }

    const tensor = this.preprocessText(text);
    const prediction = this.model!.predict(tensor) as tf.Tensor;
    const score = await prediction.data();
    
    tensor.dispose();
    prediction.dispose();
    
    return score[0];
  }

  async analyzeServer(text: string): Promise<FraudResult> {
    const response = await fetch(`${this.API_URL}/api/v1/fraud/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error('Analysis failed');
    }

    return response.json();
  }

  async analyzeRealtime(text: string): Promise<FraudResult> {
    return new Promise((resolve, reject) => {
      this.socket.emit('analyze', { text });
      
      this.socket.once('result', (data: FraudResult) => {
        resolve(data);
      });

      this.socket.once('error', (error: Error) => {
        reject(error);
      });

      setTimeout(() => reject(new Error('Timeout')), 10000);
    });
  }

  private preprocessText(text: string): tf.Tensor {
    // Simple tokenization and padding
    const maxLen = 100;
    const tokens = text.toLowerCase().split(' ').slice(0, maxLen);
    const padded = [...tokens, ...Array(maxLen - tokens.length).fill('')];
    
    // Convert to numerical representation (simplified)
    const encoded = padded.map(token => token.length);
    
    return tf.tensor2d([encoded], [1, maxLen]);
  }

  disconnect() {
    this.socket.disconnect();
  }
}
EOF

# Create backend files
cat > backend/requirements.txt << 'EOF'
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.7

# AI/ML
tensorflow==2.15.0
torch==2.2.0
transformers==4.37.0
scikit-learn==1.4.0
numpy==1.26.3
pandas==2.2.0

# NLP
spacy==3.7.2
nltk==3.8.1
sentence-transformers==2.3.1

# LLM
openai==1.12.0
anthropic==0.18.0
langchain==0.1.7
chromadb==0.4.22

# Database
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
redis==5.0.1

# Real-time
python-socketio==5.11.0
aioredis==2.0.1

# API
pydantic==2.6.0
pydantic-settings==2.1.0
httpx==0.26.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.1

# Tasks
celery==5.3.6
flower==2.0.1

# Monitoring
loguru==0.7.2
prometheus-client==0.19.0
sentry-sdk==1.40.0

# Testing
pytest==8.0.0
pytest-asyncio==0.23.4
pytest-cov==4.1.0
httpx==0.26.0
EOF

cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

cat > backend/app/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1 import fraud, analysis
from app.ml.fraud_model import FraudDetector

# Global ML model instance
fraud_detector = FraudDetector()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await fraud_detector.load_models()
    print("✅ ML Models loaded successfully")
    yield
    # Shutdown
    print("🔄 Shutting down...")

app = FastAPI(
    title="TrustStep AI API",
    version="2.0.0",
    description="AI-powered fraud detection platform",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(fraud.router, prefix="/api/v1/fraud", tags=["fraud"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])

@app.get("/")
async def root():
    return {
        "message": "TrustStep AI API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

echo "✅ Project files generated successfully!"
echo "📦 Next steps:"
echo "1. cd truststep-ai-full"
echo "2. cp .env.example .env"
echo "3. Edit .env with your API keys"
echo "4. docker-compose up -d"

