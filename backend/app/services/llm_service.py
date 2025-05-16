from app.core.config import settings
from typing import Dict, Any
from google import genai
from google.genai import types

def run_prompt(
    video_url: str,
    prompt: str
) -> Dict[str, Any]:
    """
    Run a prompt through the Gemini LLM.
    """
    try:
      client = genai.Client(api_key=settings.GOOGLE_API_KEY)

      response = client.models.generate_content(
        model='models/gemini-2.0-flash',
        contents=types.Content(
          parts=[
            types.Part(
              file_data=types.FileData(file_uri=video_url)
            ),
            types.Part(text=prompt)
          ]
        )
      )

      # Extract token counts if available
      prompt_tokens = len(prompt.split())  # Approximate token count
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