import os
import openai
from typing import Dict, Any
from ..database import Database
from ..mcp_client import mcp_client

class QAService:
    """Question & Answer service with AI agent"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    async def process_question(self, question: str, db: Database) -> Dict[str, Any]:
        """Process question with AI agent and save to database"""
        try:
            # Generate answer using AI
            answer = await self._generate_answer(question)
            
            # Save Q&A to database
            qa_id = await db.save_qa(question, answer)
            
            # Use MCP for additional processing
            mcp_result = await mcp_client.call_tool("text_generation", {
                "prompt": f"Enhance this Q&A: Q: {question} A: {answer}",
                "max_length": 200
            })
            
            return {
                "id": qa_id,
                "question": question,
                "answer": answer,
                "mcp_enhancement": mcp_result.get("result", ""),
                "timestamp": "now"
            }
            
        except Exception as e:
            # Fallback answer if AI service fails
            fallback_answer = self._get_fallback_answer(question)
            qa_id = await db.save_qa(question, fallback_answer)
            
            return {
                "id": qa_id,
                "question": question,
                "answer": fallback_answer,
                "note": f"Fallback used due to: {str(e)}",
                "timestamp": "now"
            }
    
    async def _generate_answer(self, question: str) -> str:
        """Generate AI answer using OpenAI or fallback"""
        if not self.openai_api_key:
            return self._get_fallback_answer(question)
        
        try:
            # Use OpenAI API (you can replace with other AI services)
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that provides accurate and informative answers."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._get_fallback_answer(question)
    
    def _get_fallback_answer(self, question: str) -> str:
        """Generate fallback answer when AI service is unavailable"""
        # Simple keyword-based responses
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["machine learning", "ml", "ai"]):
            return "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed."
        
        elif any(word in question_lower for word in ["python", "programming"]):
            return "Python is a high-level, interpreted programming language known for its simplicity and versatility. It's widely used in web development, data science, AI, and automation."
        
        elif any(word in question_lower for word in ["fastapi", "api"]):
            return "FastAPI is a modern, fast web framework for building APIs with Python. It provides automatic API documentation, type checking, and high performance."
        
        elif any(word in question_lower for word in ["trading", "finance"]):
            return "Algorithmic trading uses computer programs to execute trading strategies automatically based on predefined rules and market conditions."
        
        else:
            return f"Thank you for your question: '{question}'. I'm currently processing this query and will provide a detailed response based on available information and context."
    
    async def get_latest_qa(self, db: Database) -> Dict[str, Any]:
        """Get latest Q&A from database"""
        latest_qa = await db.get_latest_qa()
        
        if latest_qa:
            return {
                "found": True,
                "qa": latest_qa
            }
        else:
            return {
                "found": False,
                "message": "No Q&A entries found in database"
            }