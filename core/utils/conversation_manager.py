from typing import List, Dict

class ConversationManager:
    def __init__(self, max_history: int = 10):
        self.history = []
        self.max_history = max_history
        
    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_recent_messages(self, max_turns: int = 4) -> List[Dict]:
        # Return recent messages in chronological order
        recent = self.history[-max_turns*2:]  # Each turn has user + assistant
        return recent
    
    def reset(self):
        self.history = []
    
    def get_context(self) -> Dict:
        return {
            "history": self.history,
            "turn_count": len(self.history) // 2
        }