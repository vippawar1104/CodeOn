import streamlit as st
from langchain.schema import AIMessage, HumanMessage
import logging
from typing import Dict, Any, Generator
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("Error setting up OpenAI API key: OpenAI API key is not set")
    st.error("OpenAI API key is not set. Please set it in your .env file.")
else:
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_generation() -> Dict[str, Any]:
    """Configure generation parameters for the model."""
    return {
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.95,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

def get_realtime_response(user_prompt: str, **kwargs) -> Generator[str, None, None]:
    """Get real-time response from the model."""
    try:
        # Simple response mechanism
        responses = {
            "hello": "Hello! How can I help you with your coding today?",
            "help": "I can help you with:\n- Writing code\n- Debugging\n- Code explanations\n- Best practices\nWhat would you like to know?",
            "python": "Python is a versatile programming language. What specific aspect would you like to learn about?",
            "javascript": "JavaScript is a powerful language for web development. What would you like to know about it?",
            "debug": "I can help you debug your code. Please share the code and the error you're encountering.",
            "code": "I can help you write code. Please describe what you want to create, and I'll guide you through it.",
            "error": "I can help you fix errors in your code. Please share the error message and the relevant code.",
            "learn": "I'm here to help you learn programming! What topic would you like to explore?",
            "best practice": "I can help you understand best practices in programming. What specific area are you interested in?",
            "algorithm": "I can help you understand algorithms and data structures. What would you like to learn about?",
        }
        
        # Default response
        response = "I'm here to help with your coding questions. Please ask me anything about programming, and I'll do my best to assist you!"
        
        # Check for keywords in the prompt
        prompt_lower = user_prompt.lower()
        for key in responses:
            if key in prompt_lower:
                response = responses[key]
                break
        
        # Simulate streaming by yielding characters
        for char in response:
            yield char
            time.sleep(0.01)  # Add a small delay for streaming effect
                
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        yield "I apologize, but I encountered an error. Please try again." 