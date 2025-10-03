from base_agent import BaseAgent
from domain_registry import DomainRegistry

class TextAgent(BaseAgent):
    def __init__(self, domain: str = "general"):
        registry = DomainRegistry()
        registry.set_domain(domain)
        
        config = registry.get_engine().get_domain_config(domain)
        super().__init__(
            system_prompt=config["system_prompt"],
            model=config["model"]
        )
        self.temperature = config["temperature"]
        
    def get_input(self) -> str:
        return input("You: ")
    
    def output_response(self, response: str):
        print(f"Bot: {response}")
    
    def run_conversation(self):
        print("Starting conversation... (Type 'quit', 'exit', or 'bye' to exit)")
        
        # Initial message
        initial_response = self.get_response("")
        self.output_response(initial_response)
        
        while True:
            user_input = self.get_input()
            
            if user_input.lower() in ["quit", "exit", "bye"]:
                self.output_response("Thank you for chatting with me. Have a great day!")
                break
            
            response = self.get_response(user_input)
            self.output_response(response)
