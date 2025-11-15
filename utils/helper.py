import os, sys
from os.path import dirname as up
from typing import Generator, Dict, Any
import logging
import requests
import json
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

# Load environment variables
load_dotenv()

from utils.common_libraries import *
from utils.constants import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_realtime_response(user_prompt: str, **kwargs) -> Generator[str, None, None]:
    """Get real-time response from the Mistral API with conversation context - NO hardcoded responses."""
    try:
        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_api_key:
            yield "Error: Mistral API key is not configured."
            return
        
        # Mistral API endpoint
        api_url = "https://api.mistral.ai/v1/chat/completions"
        
        # Prepare the request
        headers = {
            "Authorization": f"Bearer {mistral_api_key}",
            "Content-Type": "application/json"
        }
        
        # Build conversation history from kwargs if provided
        chat_history = kwargs.get("chat_history", [])
        messages = [
            {
                "role": "system",
                "content": "You are a helpful coding assistant. Answer only coding and programming-related questions. Be concise and helpful. IMPORTANT: Always refer back to the conversation history when the user asks follow-up questions like 'give me the best approach', 'optimize it', 'explain more', etc. If the user previously asked about a specific problem or code, assume their follow-up questions are about that same topic."
            }
        ]
        
        # Add conversation history (limit to last 8 messages to avoid token limits, excluding the initial greeting)
        relevant_history = [msg for msg in chat_history if hasattr(msg, 'content') and 
                          "Hello! I'm CodeOn" not in msg.content][-8:]
        
        for msg in relevant_history:
            if hasattr(msg, 'content'):
                role = "assistant" if msg.__class__.__name__ == "AIMessage" else "user"
                messages.append({
                    "role": role,
                    "content": msg.content
                })
        
        # Add current user prompt
        messages.append({
            "role": "user",
            "content": user_prompt
        })
        
        payload = {
            "model": kwargs.get("model", "mistral-tiny"),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000),
            "stream": True
        }
        
        # Make the API request with streaming
        response = requests.post(api_url, headers=headers, json=payload, stream=True)
        
        if response.status_code != 200:
            logger.error(f"Mistral API error: {response.status_code} - {response.text}")
            yield f"Error: Unable to get response from Mistral API (Status: {response.status_code})"
            return
        
        # Stream the response
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                if line_text.startswith('data: '):
                    data_text = line_text[6:]  # Remove 'data: ' prefix
                    if data_text.strip() == '[DONE]':
                        break
                    try:
                        data = json.loads(data_text)
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        continue
                
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        yield "I apologize, but I encountered an error while processing your request. Please try again."

def configure_generation() -> Dict[str, Any]:
    """Configure generation parameters for the Mistral model."""
    return {
        "model": "mistral-tiny",
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }
