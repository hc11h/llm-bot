
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.agents.voice_agent import VoiceAgent
import argparse

def main():
    parser = argparse.ArgumentParser(description="Medical Voice Bot")
    parser.add_argument("--domain", type=str, default="general", 
                       choices=["general", "medical", "education"],
                       help="Domain specialization")
    args = parser.parse_args()
    
    agent = VoiceAgent(domain=args.domain)
    agent.run_conversation()

if __name__ == "__main__":
    main()