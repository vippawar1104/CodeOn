import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import logging

from custom_logger import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Configuration
try:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is not set")
    os.environ["OPENAI_API_KEY"] = openai_api_key
except Exception as e:
    logger.error(f"Error setting up OpenAI API key: {str(e)}")
    raise

MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 2000
TEMPERATURE = 0.7

API_URL = "https://api-inference.huggingface.co/models/facebook/opt-125m"