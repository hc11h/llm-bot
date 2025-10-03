import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time
from core.agents.base_agent import BaseAgent
from core.instruction.domain_registry import DomainRegistry

class VoiceAgent(BaseAgent):
    def __init__(self, domain: str = "general"):
        registry = DomainRegistry()
        registry.set_domain(domain)
        
        config = registry.get_engine().get_domain_config(domain)
        super().__init__(
            system_prompt=config["system_prompt"],
            model=config["model"]
        )
        self.temperature = config["temperature"]
        
        # Initialize audio components
        pygame.mixer.init()
        self.recognizer = sr.Recognizer()
        
    def get_input(self) -> str:
        print("Listening...")
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text
        except Exception as e:
            print(f"Error: {e}")
            return ""
    
    def output_response(self, response: str):
        print(f"Bot: {response}")
        try:
           
            timestamp = str(int(time.time()))
            filename = f"temp_{timestamp}.mp3"
            
            tts = gTTS(text=response, lang='en')
            tts.save(filename)
            
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Warning: Could not delete audio file {filename}: {e}")
                
        except Exception as e:
            print(f"Error playing audio: {e}")
            print(f"[Audio playback failed] Bot: {response}")
    
    def run_conversation(self):
        print("Starting voice conversation... (Say 'quit', 'exit', or 'bye' to exit)")
        

        initial_response = self.get_response("")
        self.output_response(initial_response)
        
        while True:
            user_input = self.get_input()
            
            if user_input and user_input.lower() in ["quit", "exit", "bye"]:
                self.output_response("Thank you for chatting with me. Have a great day!")
                break
            
            if user_input: 
                response = self.get_response(user_input)
                self.output_response(response)