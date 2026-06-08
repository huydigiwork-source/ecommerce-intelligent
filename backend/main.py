from fastapi import FastAPI
import uvicorn

# Import FastAPI app từ app.py
import sys
sys.path.insert(0, '/app')
from app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)