# 🔍 LLM-Powered Intelligent Query–Retrieval System

This is a FastAPI-based intelligent document query system built for **HackRx 2025**. It answers natural language queries on insurance, legal, HR, and compliance documents by combining semantic search with LLM-based contextual understanding.

---

## 🚀 Features

- 📄 Upload or link PDF/DOCX/email files  
- 🧠 Clause-level semantic retrieval using FAISS + embeddings  
- 🤖 Context-aware answering using Gemini Pro via REST API  
- 🔐 Secure API with optional Bearer token authentication  
- 🗃️ Uses PostgreSQL to store metadata + FAISS index as BLOB  
- ✅ Fully supports HackRx Q1 specifications and output format  

---

## 📦 Tech Stack

- **Backend:** FastAPI (Python)  
- **Embedding:** Gemini Embedding Gecko 001  
- **LLM Answering:** Gemini 2.5 Flash (via REST API)  
- **Vector Store:** FAISS  
- **Storage:** PostgreSQL (FAISS index + metadata)  
- **Deployment:** Railway  

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Gautamo1/HackRx6.0.git
cd query-retrieval-system
````

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create a `.env` File

```ini
GEMINI_API_KEY=your_gemini_api_key
API_TOKEN=your_bearer_token
DATABASE_URL=postgresql://user:password@host:port/dbname
```

---

## ▶️ Running Locally

```bash
uvicorn main:app --reload
```

The FastAPI server will run at:
`http://127.0.0.1:8000`

---

## 🔐 Authentication

All endpoints require a Bearer token:

```http
Authorization: Bearer <your_token>
```

Default fallback token (if not set):
`Bearer 0bb47e221b4a0fcd07e75742ec888026ed66cdf92f4caa4a3e7c3cd50237d896`

---

## 🔍 API: `/hackrx/run`

### Method: `POST`

### Description:

Takes a document URL and a list of questions. Returns a structured list of answers.

### Request Body:

```json
{
  "documents": "https://example.com/document.pdf",
  "questions": [
    "What is the grace period?",
    "What is the waiting period for PED?"
  ]
}
```

### Response:

```json
{
  "answers": [
    "The grace period is 30 days.",
    "PED waiting period is 4 years."
  ]
}
```

---

## 🧪 Sample `curl` Test

```bash
curl -X POST https://web-production-609b0.up.railway.app/hackrx/run \
  -H "Authorization: Bearer 88888888888888888" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/sample.pdf",
    "questions": [
      "Does this policy cover maternity?",
      "What is the waiting period for cataract?"
    ]
  }'
```

---

## 🌐 Deployment

✅ Deployed to **Railway**

**Webhook URL (for submission)**:

```
https://web-production-609b0.up.railway.app/hackrx/run
```

---

## 📄 Submission Checklist ✅

* [x] All HackRx Q1 requirements implemented
* [x] Documents supported: PDF, DOCX, email
* [x] Clause retrieval and explainable answers
* [x] Bearer token protected endpoint
* [x] `.env` used for API secrets (not hardcoded)
* [x] Endpoints tested with real documents
* [x] Webhook submitted

---

## 🙋 About Me

* **Name:** Gautam
* **Email:** [your.kumargautam802108@gmail.com]
* **GitHub:** [github.com/Gautamo1]

\