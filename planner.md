# LLM API Service 🚀

Production-style **LLM API backend service** built with **FastAPI + OpenAI Responses API**, including:

✅ prompt template control  
✅ strict request validation  
✅ structured responses  
✅ token usage tracking  
✅ in-memory caching  
✅ status & health endpoints  
✅ Streamlit UI client  

> This project is **NOT RAG** and **NOT agentic AI**.  
> It focuses on **backend orchestration + production controls**.

---

## ✨ Features

### ✅ Backend API (FastAPI)
- Prompt template registry (`template_id`)
- Pydantic validation for request/response
- OpenAI Responses API integration
- Token usage logging: `input_tokens`, `output_tokens`, `total_tokens`
- In-memory cache with stable SHA256 hashing
- Structured error handling
- Swagger UI documentation

### ✅ UI (Streamlit)
- Calls FastAPI backend
- Shows:
  - cached status
  - token usage
  - output
  - prompt debug
- History panel
- Export history JSON
- Download output TXT

---

## 🧱 Tech Stack

**Backend**
- Python 3.10+
- FastAPI
- Uvicorn
- OpenAI Python SDK
- Pydantic / pydantic-settings

**UI**
- Streamlit
- Requests

---

## 📂 Project Structure

```bash
llm-api-service/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes_generate.py
│   │       ├── routes_health.py
│   │       └── routes_status.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── schemas/
│   │   ├── generate.py
│   │   └── errors.py
│   │
│   ├── services/
│   │   ├── cache.py
│   │   ├── llm_client.py
│   │   └── prompt_templates.py
│   │
│   ├── utils/
│   │   └── hashing.py
│   │
│   └── main.py
│
├── ui/
│   └── streamlit_app.py
│
├── requirements.txt
├── planner.txt
├── README.md
├── LICENSE
└── .gitignore
⚙️ Setup
1) Create & activate venv
bash
Copy code
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
2) Install dependencies
bash
Copy code
pip install -r requirements.txt
3) Configure environment variables
Option A: .env file (recommended)

Create .env in root:

env
Copy code
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
APP_NAME=LLM API Service
APP_ENV=dev
APP_LOG_LEVEL=INFO
Option B: PowerShell env (temporary)

powershell
Copy code
$env:OPENAI_API_KEY="sk-xxxxx"
$env:OPENAI_MODEL="gpt-4o-mini"
▶️ Run Backend API
bash
Copy code
python -m uvicorn app.main:app --reload
Swagger UI:

http://127.0.0.1:8000/docs

▶️ Run Streamlit UI
Run backend first, then:

bash
Copy code
streamlit run ui/streamlit_app.py
UI:

http://localhost:8501

🔌 API Endpoints
✅ Health
http
Copy code
GET /api/v1/health
✅ Status (templates + cache size)
http
Copy code
GET /api/v1/status
✅ Generate Info
http
Copy code
GET /api/v1/generate
✅ Generate (LLM call)
http
Copy code
POST /api/v1/generate
Content-Type: application/json
Example:

json
Copy code
{
  "template_id": "basic_chat_v1",
  "input": "Give 3 points why FastAPI is popular",
  "parameters": {
    "tone": "simple"
  }
}
🧠 Templates
Supported templates:

basic_chat_v1

summarize_v1

Templates are stored in:
app/services/prompt_templates.py

📌 Interview Pitch
“I built a production-style LLM API service with prompt template management, validation, error handling, caching, OpenAI integration, and token usage tracking, along with a Streamlit UI client.”

👨‍💻 Author
Satya Srinath
GitHub: @satya66123
Email: satyasrinath653512@gmail.com

📜 License
MIT LicenseLLM API SERVICE – PROJECT PLANNER (COMPLETED)
===========================================

Project Name
------------
llm-api-service

Goal
----
Build a production-style backend LLM API service (no RAG, no agents) with:
- Prompt template control
- Request validation
- Error handling
- Token usage logging
- In-memory caching
- Swagger API docs
- Optional Streamlit UI client inside same repo

Tech Stack
----------
Backend:
- Python 3.10+
- FastAPI
- OpenAI API (Responses API)
- Pydantic
- Uvicorn

Caching:
- In-memory dict cache with stable SHA256 hash key

UI:
- Streamlit
- Requests

----------------------------------------------------------------

TASKS (DONE)
------------

TASK 1 – Environment Setup
- Create virtual environment
- Install FastAPI, OpenAI SDK, Uvicorn
- Verify imports

TASK 2 – Run FastAPI
- Created base FastAPI app
- Started server successfully using: python -m uvicorn ...

TASK 3 – Production Folder Structure
- Introduced api/v1 router structure
- Health endpoint created

TASK 4 – Schemas & Validation
- Added Pydantic schemas for request and response
- Swagger validations working

TASK 5 – Prompt Template Engine
- Created prompt template registry
- Template validation + safe rendering

TASK 6 – OpenAI Integration
- Integrated OpenAI Responses API
- Captured token usage (input/output/total)
- Returned real LLM output

TASK 7 – In-memory Cache
- Stable SHA256 cache key
- cached=true/false returned
- Reduced cost + latency

TASK 8 – Status Endpoint
- /api/v1/status returns templates + cache size + model + env

TASK 9 – Standard Error Handling
- Global exception fallback handler
- Standard error response formatting

TASK 10 – Streamlit UI (Same Repo)
- UI client to call backend
- Shows response + cached + token usage
- History panel + export JSON + download TXT

----------------------------------------------------------------

FINAL DELIVERABLES
------------------
Backend API:
- GET  /api/v1/health
- GET  /api/v1/status
- GET  /api/v1/generate
- POST /api/v1/generate

UI:
- Streamlit UI: ui/streamlit_app.py

Outcome Statement (Interview Ready)
-----------------------------------
“I built a production-style LLM API service with prompt template management,
request validation, caching, structured errors, token tracking, and a UI client.”
