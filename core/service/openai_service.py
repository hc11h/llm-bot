import openai
import time
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable"
            )
        
        self.client = openai.OpenAI(api_key=self.api_key)
        
    def chat_completion(self, messages: List[Dict], 
                       model: str = "gpt-3.5-turbo",
                       temperature: float = 0.7,
                       max_tokens: int = 300,
                       retries: int = 3) -> str:
        
        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
                
            except openai.RateLimitError:
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2 
                    time.sleep(wait_time)
                    continue
                return "I'm experiencing high demand right now. Please try again in a moment."
                
            except openai.AuthenticationError:
                return "I'm having trouble connecting to my brain. Let me try again."
                
            except openai.APIError as e:
                return f"I'm sorry, I encountered an error: {str(e)}. Let's try a different approach."
                
            except Exception as e:
                return f"I'm experiencing technical difficulties: {str(e)}. Please try again later."
        
        return "I'm experiencing technical difficulties. Please try again later."