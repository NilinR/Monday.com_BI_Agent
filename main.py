from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bi_agent import get_founder_insight

app = FastAPI()

# Allow CORS for REST communication with the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a production environment, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        answer = get_founder_insight(request.question)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/leadership-update")
async def leadership_update_endpoint():
    try:
        # Fulfills the optional requirement via a dedicated REST endpoint
        prompt = "Summarize the current state of both boards (Deals and Work Orders) into a 3-bullet executive summary highlighting risks and revenue."
        answer = get_founder_insight(prompt)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))