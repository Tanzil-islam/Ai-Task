import os
import base64
import requests
import replicate
from typing import Dict, Any
from ..mcp_client import mcp_client

class ImageService:
    """Image generation service using AI models"""
    
    def __init__(self):
        self.replicate_api_key = os.getenv("REPLICATE_API_KEY")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if self.replicate_api_key:
            os.environ["REPLICATE_API_TOKEN"] = self.replicate_api_key
    
    async def generate_image(self, prompt: str) -> Dict[str, Any]:
        """Generate image from text prompt"""
        try:
            # Try Replicate first (if API key available)
            if self.replicate_api_key:
                result = await self._generate_with_replicate(prompt)
                if result["success"]:
                    return result
            
            # Try Hugging Face as fallback
            if self.huggingface_api_key:
                result = await self._generate_with_huggingface(prompt)
                if result["success"]:
                    return result
            
            # Use MCP for image-related processing
            mcp_result = await mcp_client.call_tool("image_analysis", {
                "prompt": prompt,
                "task": "generation"
            })
            
            # Return placeholder if no API keys available
            return {
                "success": True,
                "image_url": "https://via.placeholder.com/512x512.png?text=Image+Generated",
                "prompt": prompt,
                "note": "Placeholder image - Add your API keys for actual generation",
                "mcp_info": mcp_result.get("result", "")
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt
            }
    
    async def _generate_with_replicate(self, prompt: str) -> Dict[str, Any]:
        """Generate image using Replicate API"""
        try:
            # Using Stable Diffusion model on Replicate
            output = replicate.run(
                "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
                input={
                    "prompt": prompt,
                    "width": 512,
                    "height": 512,
                    "num_outputs": 1,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 50
                }
            )
            
            if output and len(output) > 0:
                image_url = output[0]
                return {
                    "success": True,
                    "image_url": image_url,
                    "prompt": prompt,
                    "service": "replicate"
                }
            else:
                return {"success": False, "error": "No output from Replicate"}
                
        except Exception as e:
            print(f"Replicate error: {e}")
            return {"success": False, "error": str(e)}
    
    async def _generate_with_huggingface(self, prompt: str) -> Dict[str, Any]:
        """Generate image using Hugging Face API"""
        try:
            # Using Stable Diffusion on Hugging Face
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}
            
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": prompt},
                timeout=60
            )
            
            if response.status_code == 200:
                # Convert image to base64
                image_bytes = response.content
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                return {
                    "success": True,
                    "image_base64": f"data:image/png;base64,{image_base64}",
                    "prompt": prompt,
                    "service": "huggingface"
                }
            else:
                return {
                    "success": False, 
                    "error": f"Hugging Face API error: {response.status_code}"
                }
                
        except Exception as e:
            print(f"Hugging Face error: {e}")
            return {"success": False, "error": str(e)}