from fastapi import FastAPI
from fastapi.responses import Response
from dotenv import load_dotenv
from api.routes import router as query_router
import uvicorn
import os

# Load environment variables from .env
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="LLM-Powered Query Retrieval System",
    description="Ask natural language questions on legal, insurance, HR documents.",
    version="1.0.0"
)

# Include your query-related routes under /hackrx
app.include_router(query_router, prefix="/hackrx", tags=["Query API"])

# Root GET endpoint for status check
@app.get("/")
def home():
    return {"message": "LLM Query-Retrieval System is live 🎯"}

# HEAD endpoint so UptimeRobot or other monitors don't return 405
@app.head("/")
def home_head():
    return Response(status_code=200)

# Main entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
