from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from openai_service import OpenAIService
from conversation_manager import ConversationManager

class BaseAgent(ABC):
    def __init__(self, system_prompt: str, model: str = "gpt-3.5-turbo"):
        self.system_prompt = system_prompt
        self.model = model
        self.openai_service = OpenAIService()
        self.conversation_manager = ConversationManager()
        self.temperature = 0.7
        
    @abstractmethod
    def get_input(self) -> str:
        pass
    
    @abstractmethod
    def output_response(self, response: str):
        pass
    
    def get_response(self, user_input: str) -> str:
        # Add user input to conversation history
        self.conversation_manager.add_message("user", user_input)
        
        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history
        history = self.conversation_manager.get_recent_messages(max_turns=4)
        messages.extend(history)
        
        # Get response from OpenAI
        response = self.openai_service.chat_completion(
            messages=messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=300
        )
        
        # Add response to conversation history
        self.conversation_manager.add_message("assistant", response)
        
        return response
    
    def reset_conversation(self):
        self.conversation_manager.reset()
