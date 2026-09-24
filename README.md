# 💰 FinBot — AI Personal Finance Advisor

> An AI-powered personal finance advisor built with **Google Gemini AI**, **FastAPI**, and **React + Vite**.
> Designed for college submission — Engineering 2nd Year Project.

[![Made with Gemini](https://img.shields.io/badge/AI-Google%20Gemini-blue?logo=google)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB?logo=react)](https://react.dev/)

---

## 📸 Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Chat** | Powered by Google Gemini 3.8 Flash with multi-turn memory |
| 💬 **Streaming** | Real-time token streaming (like ChatGPT) |
| 🧮 **EMI Calculator** | Home, car, personal loan EMI |
| 📊 **Budget Planner** | 50/30/20 rule budget analysis |
| 📈 **SIP Calculator** | Mutual fund SIP return projections |
| 🏦 **FD Calculator** | Fixed Deposit maturity calculator |
| 🎯 **Savings Goal** | Time-to-goal savings planner |
| 🎙️ **Voice Input** | Speak your queries (Chrome) |
| 📱 **Responsive** | Works on mobile and desktop |

---

## 🏗️ Project Architecture

```
personal-finance-bot/
├── backend/                  ← FastAPI Python server
│   ├── main.py               ← API routes & entry point
│   ├── advisor.py            ← Gemini AI integration
│   ├── models.py             ← Pydantic data models
│   ├── tools.py              ← Finance calculators
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 ← React + Vite UI
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── QuickActions.jsx
│   │   │   └── Header.jsx
│   │   ├── hooks/useChat.js
│   │   └── services/api.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── render.yaml
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **AI** | Google Gemini 3.8 Flash (`google-genai >= 2.3.0`) |
| **Backend** | FastAPI + Uvicorn (Python 3.11) |
| **Frontend** | React 18 + Vite + Tailwind CSS |
| **Deployment** | Render (backend) + Vercel (frontend) |
| **Containerization** | Docker + Docker Compose |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API Key (free at [aistudio.google.com](https://aistudio.google.com/apikey))

### Step 1: Clone & Setup

```bash
git clone https://github.com/your-username/personal-finance-bot.git
cd personal-finance-bot
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env and paste your GEMINI_API_KEY

# Start backend
uvicorn main:app --reload
```
Backend runs at: http://localhost:8000
API Docs at: http://localhost:8000/docs

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
copy .env.example .env
# .env already has VITE_API_URL=http://localhost:8000

# Start frontend
npm run dev
```
Frontend runs at: http://localhost:5173

---

## 🐳 Docker (One-Command Start)

```bash
# Copy env file
copy backend\.env.example backend\.env
# Edit backend/.env and add your GEMINI_API_KEY

# Start everything
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## ☁️ Deploy to Render (Free Hosting)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → Blueprint
3. Connect your repo (has `render.yaml`)
4. Add environment variable: `GEMINI_API_KEY = your_key`
5. Click **Deploy** → Your app is live! 🎉

---

## 🤖 How the AI Works

```
User Message
     ↓
FastAPI Backend
     ↓
Gemini 3.8 Flash (with function calling)
     ↓
If math query → calls finance tool (EMI/SIP/FD/Budget)
     ↓
Tool returns result → Gemini formats response
     ↓
Streamed back to React frontend
     ↓
Displayed with markdown rendering
```

---

## 🧮 Finance Calculators

### EMI Calculator
```
Formula: EMI = P × r × (1+r)^n / ((1+r)^n - 1)
Where: P = Principal, r = Monthly rate, n = Tenure months
```

### SIP Returns
```
Formula: FV = PMT × ((1+r)^n - 1) / r × (1+r)
Where: PMT = Monthly SIP, r = Monthly rate, n = Months
```

### Fixed Deposit
```
Formula: A = P × (1 + r/n)^(n×t)
Where: P = Principal, r = Annual rate, n = Compounding, t = Years
```

---

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Service status |
| POST | `/chat` | Chat (full response) |
| POST | `/chat/stream` | Chat (streaming SSE) |
| GET | `/tools` | List available tools |
| GET | `/docs` | Swagger UI |

---

## 👨‍💻 Team

Built as an Engineering 2nd Year college project demonstrating:
- REST API design with FastAPI
- AI integration with Google Gemini
- React component architecture
- Real-time streaming with SSE
- Docker containerization
- Cloud deployment

---

## 📄 License

MIT License — Free to use for educational purposes.
