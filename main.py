# # main.py

# from fastapi import FastAPI
# from api.routes import router as query_router
# from dotenv import load_dotenv
# import uvicorn

# # Load .env for GEMINI_API_KEY and others
# load_dotenv()

# # Initialize FastAPI app
# app = FastAPI(
#     title="LLM-Powered Query Retrieval System",
#     description="Ask natural language questions on legal, insurance, HR documents.",
#     version="1.0.0"
# )

# # Include API route for /hackrx/ask
# app.include_router(query_router, prefix="/hackrx", tags=["Query API"])

# # Health check
# @app.get("/")
# def home():
#     return {"message": "LLM Query-Retrieval System is live 🎯"}

# # For running via `python main.py`
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



# from fastapi import FastAPI
# from api.routes import router as query_router
# from dotenv import load_dotenv
# import uvicorn

# load_dotenv()

# app = FastAPI(
#     title="LLM-Powered Query Retrieval System",
#     description="Ask natural language questions on legal, insurance, HR documents.",
#     version="1.0.0"
# )

# # ✅ Mount all /hackrx/* routes here
# app.include_router(query_router, prefix="/hackrx", tags=["Query API"])

# @app.get("/")
# def home():
#     return {"message": "LLM Query-Retrieval System is live 🎯"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


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
