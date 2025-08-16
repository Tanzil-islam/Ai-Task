import os
import openai
from typing import Dict, Any
from ..mcp_client import mcp_client

class ContentService:
    """Platform-specific content generation service"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Platform-specific content guidelines
        self.platform_guidelines = {
            "facebook": {
                "tone": "engaging and friendly",
                "length": "medium (100-300 words)",
                "features": "use emojis, ask questions, encourage sharing",
                "hashtags": "2-5 relevant hashtags",
                "call_to_action": "always include a CTA"
            },
            "linkedin": {
                "tone": "professional and informative",
                "length": "longer (200-500 words)",
                "features": "industry insights, professional achievements",
                "hashtags": "3-8 professional hashtags",
                "call_to_action": "encourage professional discussion"
            },
            "twitter": {
                "tone": "concise and impactful",
                "length": "short (under 280 characters)",
                "features": "trending topics, mentions, retweets",
                "hashtags": "1-3 hashtags maximum",
                "call_to_action": "encourage retweets/replies"
            },
            "instagram": {
                "tone": "visual and storytelling",
                "length": "medium (150-400 words)",
                "features": "visual descriptions, storytelling",
                "hashtags": "10-20 hashtags",
                "call_to_action": "encourage likes and comments"
            }
        }
    
    async def generate_content(self, prompt: str, platform: str) -> Dict[str, Any]:
        """Generate platform-specific content"""
        try:
            platform = platform.lower()
            
            # Use MCP for content optimization
            mcp_result = await mcp_client.call_tool("content_optimization", {
                "content": prompt,
                "platform": platform
            })
            
            # Generate content using AI
            content = await self._generate_ai_content(prompt, platform)
            
            return {
                "content": content,
                "platform": platform,
                "prompt": prompt,
                "guidelines_used": self.platform_guidelines.get(platform, {}),
                "mcp_optimization": mcp_result.get("result", "")
            }
            
        except Exception as e:
            # Fallback content generation
            fallback_content = self._generate_fallback_content(prompt, platform)
            
            return {
                "content": fallback_content,
                "platform": platform,
                "prompt": prompt,
                "note": f"Fallback used due to: {str(e)}"
            }
    
    async def _generate_ai_content(self, prompt: str, platform: str) -> str:
        """Generate AI content using OpenAI or fallback"""
        if not self.openai_api_key:
            return self._generate_fallback_content(prompt, platform)
        
        try:
            guidelines = self.platform_guidelines.get(platform, self.platform_guidelines["facebook"])
            
            system_prompt = f"""You are a social media content creator specializing in {platform} content.
            
            Platform Guidelines:
            - Tone: {guidelines.get('tone', 'engaging')}
            - Length: {guidelines.get('length', 'medium')}
            - Features: {guidelines.get('features', 'engaging content')}
            - Hashtags: {guidelines.get('hashtags', 'relevant hashtags')}
            - Call to Action: {guidelines.get('call_to_action', 'encourage engagement')}
            
            Create content that follows these guidelines and is optimized for {platform}."""
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create {platform} content about: {prompt}"}
                ],
                max_tokens=300 if platform != "twitter" else 100,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._generate_fallback_content(prompt, platform)
    
    def _generate_fallback_content(self, prompt: str, platform: str) -> str:
        """Generate fallback content when AI service is unavailable"""
        platform = platform.lower()
        
        base_content = f"📢 Exciting news about {prompt}! "
        
        if platform == "facebook":
            return f"""{base_content}
            
We're thrilled to share this update with our amazing community! 🚀

What are your thoughts on this? Let us know in the comments below! 👇

#Innovation #Community #Updates #Exciting #News"""
        
        elif platform == "linkedin":
            return f"""{base_content}

In today's rapidly evolving landscape, developments like this showcase the importance of innovation and forward-thinking approaches.

Key takeaways:
• Innovation drives progress
• Community engagement is crucial  
• Staying updated is essential

What's your perspective on this development? I'd love to hear your professional insights.

#Innovation #Professional #Industry #Networking #Growth #Technology #Business"""
        
        elif platform == "twitter":
            return f"🚀 {prompt} - this is game-changing! Thoughts? #Innovation #Tech #Updates"
        
        elif platform == "instagram":
            return f"""{base_content}

✨ Swipe to see more about this incredible development! 

Behind every great innovation is a story of dedication, creativity, and vision. This is one of those moments that reminds us why we love what we do.

📸 Tag someone who needs to see this!
💭 What's your take? Drop a comment!

#Innovation #Inspiration #Creative #Community #Updates #Exciting #Vision #Dedication #Progress #Amazing #Incredible #Development #Story #Moments #Love"""
        
        else:
            return f"{base_content} This is an exciting development that we wanted to share with you! #Updates #News #Innovation"
