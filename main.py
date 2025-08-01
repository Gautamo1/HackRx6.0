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
from dotenv import load_dotenv
from api.routes import router as query_router
import uvicorn

load_dotenv()

app = FastAPI(
    title="LLM-Powered Query Retrieval System",
    description="Ask natural language questions on legal, insurance, HR documents.",
    version="1.0.0"
)

app.include_router(query_router, prefix="/hackrx", tags=["Query API"])

@app.get("/")
def home():
    return {"message": "LLM Query-Retrieval System is live 🎯"}

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
