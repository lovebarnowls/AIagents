import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

if CLAUDE_API_KEY is None:
    raise ValueError("CLAUDE_API_KEY is not set in the environment variables")

headers = {
    "Content-Type": "application/json",
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01"
}

# Custom system message to set the tone and style
CUSTOM_SYSTEM_MESSAGE = """
You are an AI assistant that communicates in a manner similar to the user you're emulating. Please adhere to the following guidelines in all your responses:

1. Use British English spelling (e.g., 'colour' instead of 'color', 'realise' instead of 'realize').
2. Begin requests with phrases like "Can I please trouble you" or "Would you mind".
3. Use polite and formal language, but maintain a friendly tone.
4. Occasionally use British colloquialisms or expressions.
5. Show empathy and understanding in your responses.
6. If appropriate, use words like 'quite', 'rather', or 'quite so' to add emphasis.
7. When expressing agreement, use phrases like "I couldn't agree more" or "You're absolutely right".
8. Avoid using contractions (e.g., "one's", "it's")

Remember to maintain this style consistently throughout the conversation.
"""

def chat_with_claude(message, conversation_history=[]):
    data = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1000,
        "system": CUSTOM_SYSTEM_MESSAGE,
        "messages": conversation_history + [{"role": "user", "content": message}]
    }
    
    response = requests.post(CLAUDE_API_URL, json=data, headers=headers)
    response.raise_for_status()
    
    assistant_message = response.json()['content'][0]['text']
    return assistant_message

def main():
    print("Welcome to the Custom Claude Opus Chatbot!")
    print("Type 'quit' to exit the conversation.")
    
    conversation_history = []
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            print("I do hope you've had a pleasant experience. Farewell!")
            break
        
        try:
            response = chat_with_claude(user_input, conversation_history)
            print("\nClaude:", response)
            
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})
            
        except requests.exceptions.HTTPError as e:
            print(f"I do apologise, but it seems we've encountered an HTTP Error: {e}")
            print(f"Response content: {e.response.content}")
        except Exception as e:
            print(f"I'm terribly sorry, but an error has occurred: {e}")

if __name__ == "__main__":
    main()