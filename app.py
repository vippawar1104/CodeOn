import streamlit as st
import warnings
import os
import sys

# Suppress all warnings including torch
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Suppress streamlit watcher warnings
import logging
logging.getLogger('streamlit.watcher.local_sources_watcher').setLevel(logging.ERROR)

# App config must be the first Streamlit command
st.set_page_config(
    page_title="CodeOn - AI Code Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils import *
import time
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def is_coding_question(query: str, chat_history: list = None) -> bool:
    """Check if the user query is related to coding/programming, considering conversation context."""
    coding_keywords = [
        "code", "python", "java", "javascript", "c++", "c#", "programming", "algorithm", 
        "function", "variable", "bug", "debug", "error", "exception", "compile", "run", 
        "execute", "library", "framework", "syntax", "logic", "data structure", "class", 
        "object", "method", "loop", "array", "list", "dictionary", "set", "tuple", 
        "recursion", "sort", "search", "database", "sql", "api", "web", "backend", 
        "frontend", "devops", "git", "github", "version control", "test", "unit test", 
        "integration test", "deployment", "cloud", "docker", "kubernetes", 
        "machine learning", "ai", "deep learning", "nlp", "pandas", "numpy", 
        "matplotlib", "plot", "visualization", "regex", "security", "best practices",
        "html", "css", "react", "node", "vue", "angular", "typescript", "rust",
        "go", "kotlin", "swift", "php", "ruby", "scala", "perl", "bash", "shell"
    ]
    
    query_lower = query.lower()
    
    # Check if query contains coding keywords
    if any(keyword in query_lower for keyword in coding_keywords):
        return True
    
    # If chat history exists and has recent coding context, allow follow-up questions
    if chat_history and len(chat_history) > 1:
        # Check last few messages for coding context
        recent_messages = chat_history[-5:]  # Last 5 messages
        for msg in recent_messages:
            if hasattr(msg, 'content'):
                msg_lower = msg.content.lower()
                if any(keyword in msg_lower for keyword in coding_keywords):
                    # Recent conversation was about coding, so allow follow-ups like:
                    # "explain more", "give me the best approach", "optimize it", etc.
                    follow_up_patterns = [
                        "explain", "show", "give", "how", "what", "why", "best", "better",
                        "optimize", "improve", "example", "more", "another", "different",
                        "clarify", "tell me", "can you", "please", "thanks", "thank you"
                    ]
                    if any(pattern in query_lower for pattern in follow_up_patterns):
                        return True
    
    return False

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/code.png", width=100)
    st.markdown('<h1>CodeOn</h1>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<h3>About</h3>', unsafe_allow_html=True)
    st.markdown("CodeOn is your intelligent coding companion, powered by advanced AI to help you write, debug, and understand code better.")
    
    st.markdown('<h3>Features</h3>', unsafe_allow_html=True)
    st.markdown("""
    - Smart Code Generation
    - Code Analysis
    - Debugging Assistance
    - Learning Support
    """)
    
    # Programming Resources
    st.markdown('<h4>Resources</h4>', unsafe_allow_html=True)
    st.markdown("""
    - [Python Documentation](https://docs.python.org/3/)
    - [Real Python Tutorials](https://realpython.com/)
    - [GeeksforGeeks](https://www.geeksforgeeks.org/)
    - [Stack Overflow](https://stackoverflow.com/)
    - [GitHub](https://github.com/)
    """)
    
# Main content
st.markdown('<h1>CodeOn - Your AI Coding Companion</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #fff; font-size: 1.2em;">Write, debug, and learn code with AI assistance</p>', unsafe_allow_html=True)

# Setting generation configuration - This will override the parameter that is set in the Modelfile
get_config_gen = configure_generation()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm CodeOn, your AI coding assistant. I can help you with:\n\n"
                         "- Writing and debugging code\n"
                         "- Explaining programming concepts\n"
                         "- Optimizing your code\n"
                         "- Learning best practices\n\n"
                         "How can I assist you today?")
    ]

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message("AI" if isinstance(message, AIMessage) else "Human"):
        if isinstance(message, AIMessage):
            st.markdown(message.content)
        else:
            st.write(message.content)

# User input
if user_query := st.chat_input("Ask me anything about coding..."):
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.write(user_query)

    with st.chat_message("AI"):
        response_placeholder = st.empty()
        full_response = ""
        # Add typing animation
        with st.spinner("Thinking..."):
            # Check if the question is coding-related (with conversation context)
            if is_coding_question(user_query, st.session_state.chat_history):
                # Pass chat history for context
                config_with_history = {**get_config_gen, "chat_history": st.session_state.chat_history}
                for chunk in get_realtime_response(user_prompt=user_query, **config_with_history):
                    full_response += chunk
                    response_placeholder.markdown(full_response)
                logger.info("Response successfully generated.")
            else:
                apology = "Sorry, I can only assist with coding and programming-related questions."
                response_placeholder.markdown(apology)
                full_response = apology
    st.session_state.chat_history.append(AIMessage(content=full_response))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with Streamlit • Powered by AI</p>
</div>
""", unsafe_allow_html=True)
