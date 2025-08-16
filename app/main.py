from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from .models import AITaskRequest, AITaskResponse, TokenRequest
from .database import create_tables, get_db
from .auth import create_access_token, verify_token
from .services.qa_service import QAService
from .services.image_service import ImageService
from .services.content_service import ContentService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Trader Task API",
    description="Multi-task AI API for Softvence Omega recruitment",
    version="1.0.0"
)

# Security scheme
security = HTTPBearer(auto_error=False)

# Create database tables on startup
@app.on_event("startup")
async def startup():
    await create_tables()

# Initialize services
qa_service = QAService()
image_service = ImageService()
content_service = ContentService()

# Serve frontend files at root with html support
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.post("/token")
async def login(token_request: TokenRequest):
    """Generate JWT token (optional endpoint for authentication)"""
    # Simple authentication - in production, verify against user database
    if token_request.username == "admin" and token_request.password == "password":
        access_token = create_access_token(data={"sub": token_request.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token (optional authentication)"""
    if not credentials:
        return None  # Allow unauthenticated access
    
    token = credentials.credentials
    try:
        payload = verify_token(token)
        return payload.get("sub")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@app.post("/ai-task", response_model=AITaskResponse)
async def ai_task_handler(
    request: AITaskRequest,
    current_user: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Single route to handle all AI tasks:
    - qa: Question & Answer with agent
    - fetch_latest: Get latest Q&A from database
    - generate_image: Generate image from prompt
    - generate_content: Generate platform-specific content
    """
    
    try:
        if request.task == "qa":
            if not request.question:
                raise HTTPException(status_code=400, detail="Question is required for Q&A task")
            
            result = await qa_service.process_question(request.question, db)
            return AITaskResponse(
                task=request.task,
                success=True,
                data=result,
                message="Q&A processed successfully"
            )
        
        elif request.task == "fetch_latest":
            result = await qa_service.get_latest_qa(db)
            return AITaskResponse(
                task=request.task,
                success=True,
                data=result,
                message="Latest Q&A retrieved successfully"
            )
        
        elif request.task == "generate_image":
            if not request.prompt:
                raise HTTPException(status_code=400, detail="Prompt is required for image generation")
            
            result = await image_service.generate_image(request.prompt)
            return AITaskResponse(
                task=request.task,
                success=True,
                data=result,
                message="Image generated successfully"
            )
        
        elif request.task == "generate_content":
            if not request.prompt:
                raise HTTPException(status_code=400, detail="Prompt is required for content generation")
            
            platform = request.platform or "general"
            result = await content_service.generate_content(request.prompt, platform)
            return AITaskResponse(
                task=request.task,
                success=True,
                data=result,
                message=f"Content generated for {platform} successfully"
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown task: {request.task}")
    
    except Exception as e:
        return AITaskResponse(
            task=request.task,
            success=False,
            data=None,
            message=f"Error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Trader Task API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)