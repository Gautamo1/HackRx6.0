from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()
API_TOKEN = os.getenv("API_TOKEN", "0bb47e221b4a0fcd07e75742ec888026ed66cdf92f4caa4a3e7c3cd50237d896")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
