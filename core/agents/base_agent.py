from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from core.services.openai_service import OpenAIService
from core.utils.conversation_manager import ConversationManager

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
        self.conversation_manager.add_message("user", user_input)

        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        history = self.conversation_manager.get_recent_messages(max_turns=4)
        messages.extend(history)
        
        response = self.openai_service.chat_completion(
            messages=messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=300
        )
        
        self.conversation_manager.add_message("assistant", response)
        
        return response
    
    def reset_conversation(self):
        self.conversation_manager.reset()