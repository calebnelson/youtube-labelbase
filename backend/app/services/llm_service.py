import google.generativeai as genai
from app.core.config import settings
from typing import Dict, Any

# Configure the Gemini API
genai.configure(api_key=settings.GOOGLE_API_KEY)

def run_prompt(
    video_id: str,
    system_prompt: str,
    user_prompt: str
) -> Dict[str, Any]:
    """
    Run a prompt through the Gemini LLM.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Combine system and user prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        # Extract token counts if available
        prompt_tokens = len(full_prompt.split())  # Approximate token count
        completion_tokens = len(response.text.split())  # Approximate token count
        
        return {
            "content": response.text,
            "model": "gemini-pro",
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        }
    except Exception as e:
        raise Exception(f"Error running prompt: {str(e)}") 