import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
import logging
from typing import Dict, Any, Generator
import time
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure Mistral API key
mistral_api_key = os.getenv("MISTRAL_API_KEY")
if not mistral_api_key:
    logging.error("Error setting up Mistral API key: Mistral API key is not set")
    st.error("Mistral API key is not set. Please set it in your .env file.")
else:
    os.environ["MISTRAL_API_KEY"] = mistral_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_generation() -> Dict[str, Any]:
    """Configure generation parameters for the Mistral model."""
    return {
        "model": "mistral-tiny",
        "temperature": 0.7,
        "max_tokens": 2000,
    }

def get_realtime_response(user_prompt: str, **kwargs) -> Generator[str, None, None]:
    """Get real-time response from the Mistral API."""
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
        
        payload = {
            "model": kwargs.get("model", "mistral-tiny"),
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful coding assistant. Answer only coding and programming-related questions. Be concise and helpful."
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
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
                        import json
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