import os, sys
from os.path import dirname as up
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

import streamlit as st
# Updated langchain imports for latest version
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

from custom_logger import *

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mistral Configuration
try:
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_api_key:
        raise ValueError("Mistral API key is not set")
    os.environ["MISTRAL_API_KEY"] = mistral_api_key
except Exception as e:
    logger.error(f"Error setting up Mistral API key: {str(e)}")
    raise

MODEL_NAME = "mistral-tiny"
MAX_TOKENS = 2000
TEMPERATURE = 0.7

API_URL = "https://api.mistral.ai/v1/chat/completions"