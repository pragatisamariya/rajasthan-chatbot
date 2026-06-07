from fastapi import FastAPI
from pydantic import BaseModel
from rajasthan_module import ask_rajasthan  # replace with your module if needed
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rajasthan Tourism AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat(query: Query):
    response = ask_rajasthan(query.message)
    return {"response": response}

@app.get("/")
def root():
    return {"message": "Rajasthan Tourism AI is live!"}
