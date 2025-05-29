import streamlit as st

# App config must be the first Streamlit command
st.set_page_config(
    page_title="CodeOn - AI Code Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils import *
import time
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# Custom CSS
st.markdown("""
<style>
    /* Main background and container styles */
    .main {
        background-color: #0E1117;
        background-image: linear-gradient(45deg, #0E1117 0%, #1a1c24 100%);
    }
    
    /* Neon text effect for headers */
    .neon-text {
        color: #fff;
        text-shadow: 0 0 5px #fff,
                     0 0 10px #fff,
                     0 0 20px #0ff,
                     0 0 30px #0ff,
                     0 0 40px #0ff;
        animation: neon-pulse 1.5s ease-in-out infinite alternate;
    }
    
    /* Main title neon effect */
    .main-title {
        font-size: 2.5em;
        font-weight: bold;
        color: #fff;
        text-shadow: 0 0 5px #fff,
                     0 0 10px #fff,
                     0 0 20px #0ff,
                     0 0 30px #0ff,
                     0 0 40px #0ff,
                     0 0 50px #0ff,
                     0 0 60px #0ff;
        animation: main-title-pulse 2s ease-in-out infinite alternate;
        text-align: center;
        margin: 20px 0;
    }
    
    @keyframes main-title-pulse {
        from {
            text-shadow: 0 0 5px #fff,
                         0 0 10px #fff,
                         0 0 20px #0ff,
                         0 0 30px #0ff,
                         0 0 40px #0ff,
                         0 0 50px #0ff,
                         0 0 60px #0ff;
        }
        to {
            text-shadow: 0 0 2px #fff,
                         0 0 5px #fff,
                         0 0 10px #0ff,
                         0 0 20px #0ff,
                         0 0 30px #0ff,
                         0 0 40px #0ff,
                         0 0 50px #0ff;
        }
    }
    
    @keyframes neon-pulse {
        from {
            text-shadow: 0 0 5px #fff,
                         0 0 10px #fff,
                         0 0 20px #0ff,
                         0 0 30px #0ff,
                         0 0 40px #0ff;
        }
        to {
            text-shadow: 0 0 2px #fff,
                         0 0 5px #fff,
                         0 0 10px #0ff,
                         0 0 20px #0ff,
                         0 0 30px #0ff;
        }
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: rgba(30, 30, 30, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Input area styling */
    .stChatInput {
        background-color: rgba(46, 46, 46, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border-radius: 25px;
        padding: 12px 30px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        background: linear-gradient(45deg, #45a049, #4CAF50);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(30, 30, 30, 0.7);
        backdrop-filter: blur(10px);
    }
    
    /* Code block styling */
    .stCodeBlock {
        background-color: rgba(40, 40, 40, 0.7);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Smooth scrolling */
    * {
        scroll-behavior: smooth;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/code.png", width=100)
    st.markdown('<h1 class="neon-text">CodeOn</h1>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<h3 class="neon-text">About</h3>', unsafe_allow_html=True)
    st.markdown("CodeOn is your intelligent coding companion, powered by advanced AI to help you write, debug, and understand code better.")
    
    add_vertical_space(2)
    st.markdown('<h3 class="neon-text">Features</h3>', unsafe_allow_html=True)
    st.markdown("""
    - 💡 Smart Code Generation
    - 🔍 Code Analysis
    - 🐛 Debugging Assistance
    - 📚 Learning Support
    """)
    
    add_vertical_space(2)
    st.markdown('<h3 class="neon-text">Quick Tools</h3>', unsafe_allow_html=True)
    
    # Code Line Counter
    st.markdown('<h4 class="neon-text">📝 Code Line Counter</h4>', unsafe_allow_html=True)
    code_to_count = st.text_area("Paste your code here to count lines", height=100)
    if st.button("Count Lines"):
        if code_to_count:
            # Count total lines
            total_lines = len(code_to_count.splitlines())
            # Count non-empty lines
            non_empty_lines = len([line for line in code_to_count.splitlines() if line.strip()])
            # Count comment lines
            comment_lines = len([line for line in code_to_count.splitlines() if line.strip().startswith('#')])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Lines", total_lines)
            with col2:
                st.metric("Code Lines", non_empty_lines - comment_lines)
            with col3:
                st.metric("Comment Lines", comment_lines)
    
    add_vertical_space(1)
    
    # Simple Code Beautifier
    st.markdown('<h4 class="neon-text">✨ Code Beautifier</h4>', unsafe_allow_html=True)
    code_to_beautify = st.text_area("Paste your code here to beautify", height=100)
    if st.button("Beautify"):
        if code_to_beautify:
            try:
                # Simple indentation fix
                lines = code_to_beautify.splitlines()
                indent_level = 0
                beautified_lines = []
                
                for line in lines:
                    stripped = line.strip()
                    if stripped:
                        # Handle indentation
                        if stripped.endswith(':'):
                            beautified_lines.append('    ' * indent_level + stripped)
                            indent_level += 1
                        elif stripped.startswith(('return', 'break', 'continue')):
                            indent_level = max(0, indent_level - 1)
                            beautified_lines.append('    ' * indent_level + stripped)
                        else:
                            beautified_lines.append('    ' * indent_level + stripped)
                    else:
                        beautified_lines.append('')
                
                beautified_code = '\n'.join(beautified_lines)
                st.code(beautified_code, language='python')
            except Exception as e:
                st.error("Error beautifying code. Please check your Python syntax.")
    
    add_vertical_space(1)
    
    # Programming Resources
    st.markdown('<h4 class="neon-text">🔗 Resources</h4>', unsafe_allow_html=True)
    st.markdown("""
    - [Python Documentation](https://docs.python.org/3/)
    - [Real Python Tutorials](https://realpython.com/)
    - [GeeksforGeeks](https://www.geeksforgeeks.org/)
    - [Stack Overflow](https://stackoverflow.com/)
    - [GitHub](https://github.com/)
    """)
    
    add_vertical_space(2)

# Main content
st.markdown('<h1 class="main-title">🚀 CodeOn - Your AI Coding Companion</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #fff; font-size: 1.2em;">Write, debug, and learn code with AI assistance</p>', unsafe_allow_html=True)

# Setting generation configuration - This will override the parameter that is set in the Modelfile
get_config_gen = configure_generation()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="👋 Hello! I'm CodeOn, your AI coding assistant. I can help you with:\n\n"
                         "• Writing and debugging code\n"
                         "• Explaining programming concepts\n"
                         "• Optimizing your code\n"
                         "• Learning best practices\n\n"
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
            for chunk in get_realtime_response(user_prompt=user_query, **get_config_gen):
                full_response += chunk
                response_placeholder.markdown(full_response)
        
        logger.info("Response successfully generated.")
    
    st.session_state.chat_history.append(AIMessage(content=full_response))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p class="neon-text">Built with Streamlit • Powered by AI</p>
</div>
""", unsafe_allow_html=True)
