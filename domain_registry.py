from instruction_engine import InstructionEngine

class DomainRegistry:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.instruction_engine = InstructionEngine()
        self._register_default_domains()
    
    def _register_default_domains(self):
        # Register default domains
        self.instruction_engine.register_domain(
            "general",
            "You are a helpful assistant. Answer questions accurately and be friendly.",
            temperature=0.7
        )
        
        self.instruction_engine.register_domain(
            "medical",
            """You are a medical assistant bot. Your role is to:
1. Provide general health information and answer medical questions
2. Help users understand symptoms and possible causes
3. Recommend when to seek professional medical help

IMPORTANT RULES:
- Never diagnose medical conditions
- Never prescribe medications
- Always recommend consulting healthcare professionals for specific concerns
- If someone describes a medical emergency, direct them to call emergency services

RESPONSE STYLE:
- Use simple, clear language
- Be empathetic and supportive
- Ask clarifying questions when needed
- Provide information in digestible chunks
- If the user asks non-medical questions, politely redirect to medical topics""",
            temperature=0.3
        )
        
        self.instruction_engine.register_domain(
            "education",
            """You are an educational assistant. Your role is to:
1. Explain complex topics in simple terms
2. Help with homework and learning
3. Provide educational resources and guidance

RESPONSE STYLE:
- Use clear, simple language
- Provide examples when helpful
- Encourage learning and curiosity
- Be patient and supportive""",
            temperature=0.5
        )
    
    def get_engine(self) -> InstructionEngine:
        return self.instruction_engine
    
    def register_domain(self, domain_name: str, system_prompt: str, 
                      temperature: float = 0.7, model: str = "gpt-3.5-turbo"):
        self.instruction_engine.register_domain(domain_name, system_prompt, temperature, model)
    
    def set_domain(self, domain_name: str):
        return self.instruction_engine.set_domain(domain_name)
    
    def list_domains(self):
        return self.instruction_engine.list_domains()
