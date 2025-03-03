from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from app.agents.planner import Planner
from app.schemas.chat import ChatRequest, ChatResponse
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MentorAI",
    description="API for a virtual tutoring system with multiple agents",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = Planner()

@app.get("/", response_model=Dict[str, Any])
async def read_root():
    """Root endpoint showing basic API information"""
    return {
        "name": "MentorAI API",
        "version": "1.0",
        "status": "active",
        "description": "API for a virtual tutoring system with multiple agents",
        "endpoints": {
            "chat": "/chat - POST to interact with the teachers",
            "docs": "/docs - Interactive API documentation"
        }
    }

@app.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Returns a simple web interface to test the chat"""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>MentorAI Chat</title>
        </head>
        <body>
            <h1>MentorAI Chat</h1>
            <p>Please ask your questions in English.</p>
            <input type="text" id="message" placeholder="Type your question...">
            <button onclick="sendMessage()">Send</button>
            <div id="response"></div>

            <script>
            async function sendMessage() {
                const message = document.getElementById('message').value;
                const response = document.getElementById('response');
                
                try {
                    const res = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({message: message})
                    });
                    
                    const data = await res.json();
                    response.innerHTML = `<p><strong>Response:</strong> ${data.message}</p>`;
                } catch (error) {
                    response.innerHTML = `<p style="color: red;">Error: ${error}</p>`;
                }
            }
            </script>
        </body>
    </html>
    """

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint with enhanced error handling"""
    try:
        logger.debug(f"Received chat request: {request.message}")
        
        response = await planner.process_message(request.message)
        logger.debug(f"Got response from planner: {response}")
        
        return ChatResponse(
            message=response["message"],
            subject=response["subject"],
            teacher=response["teacher"]
        )
            
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )