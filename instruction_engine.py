from typing import Dict, Optional, List
import json

class InstructionEngine:
    def __init__(self):
        self.domains = {}
        self.current_domain = None
        self.system_prompt = None
        
    def register_domain(self, domain_name: str, system_prompt: str, 
                       temperature: float = 0.7, model: str = "gpt-3.5-turbo"):
        """Register a new domain with its system prompt"""
        self.domains[domain_name] = {
            "system_prompt": system_prompt,
            "temperature": temperature,
            "model": model
        }
        
    def set_domain(self, domain_name: str):
        """Set the current domain"""
        if domain_name in self.domains:
            self.current_domain = domain_name
            self.system_prompt = self.domains[domain_name]["system_prompt"]
            return True
        return False
    
    def get_system_prompt(self) -> str:
        """Get the current system prompt"""
        return self.system_prompt or "You are a helpful assistant."
    
    def get_domain_config(self, domain_name: str) -> Optional[Dict]:
        """Get configuration for a domain"""
        return self.domains.get(domain_name)
    
    def list_domains(self) -> List[str]:
        """List all registered domains"""
        return list(self.domains.keys())
    
    def load_domains_from_file(self, file_path: str):
        """Load domains from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                domains_data = json.load(f)
                for domain_name, config in domains_data.items():
                    self.register_domain(
                        domain_name,
                        config["system_prompt"],
                        config.get("temperature", 0.7),
                        config.get("model", "gpt-3.5-turbo")
                    )
        except Exception as e:
            print(f"Error loading domains: {e}")