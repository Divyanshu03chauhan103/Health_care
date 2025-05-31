import streamlit as st
from PIL import Image
import google.generativeai as genai
from navbar import navbar
from footer import footer
# from internetsearchtool import InternetSearcher
# from search_agent import SearchAgent  # Import the SearchAgent class
from webscrappingtool import WebScraper  # Import the WebScraper class

# Import custom styles
from styles import load_styles

# Set Page Configuration
st.set_page_config(
    page_title="MediMind AI | Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom styles
load_styles()

# Set Gemini API Key (Replace with actual key in production)
GOOGLE_API_KEY = "AIzaSyBMQzWLHcTOTNzDHQoCB-rD0B2x558RyrA"
genai.configure(api_key=GOOGLE_API_KEY)

# Function to handle chatbot responses
def get_chat_response(prompt):
    try:
        # Initialize the WebScraper
        scraper = WebScraper()
        
        # Step 1: Get medical information from the LLM (Gemini)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        system_instruction = "You are a helpful medical assistant. Provide clear, accurate information but always remind users to consult healthcare professionals for medical advice."
        full_prompt = f"{system_instruction}\n\nUser question: {prompt}"
        llm_response = model.generate_content(full_prompt)
        
        # Step 2: Get web scraping results from allowed websites
        scraping_results = []
        for site in scraper.ALLOWED_SITES:  # Access as scraper.ALLOWED_SITES
            query = f"{prompt} site:{site}"  # Search within the specific site
            links = scraper.search_duckduckgo(query)  # Use DuckDuckGo for search
            for link in links[:3]:  # Limit to top 3 results per site
                content = scraper.scrape_website(link)
                if content:
                    scraping_results.append({
                        "source": link,
                        "content": content[:500]  # Limit content length for brevity
                    })
        
        # Step 3: Format the response
        response = f"Medical Information (LLM):\n{llm_response.text}\n\n"
        
        if scraping_results:
            response += "Web Scraping Results (Trusted Sources):\n"
            for result in scraping_results:
                response += f"Source: {result['source']}\n"
                response += f"Content: {result['content']}...\n\n"
        else:
            response += "No additional information found from trusted sources.\n"
        
        return response, True
    except Exception as e:
        return f"Error: Unable to get response. {str(e)}", False

# Additional custom CSS for this specific page
st.markdown("""
<style>
    /* Chat container styling */
    .chat-container {
        background-color: var(--bg-white);
        border-radius: 12px;
        padding: 25px;
        box-shadow: var(--shadow);
        margin-bottom: 25px;
    }
    
    .chat-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .chat-icon {
        font-size: 32px;
        margin-right: 15px;
        color: var(--primary);
    }
    
    /* Chat input area styling */
    .chat-input {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: white;
    }
    
    /* Message styling */
    .user-message {
        background-color: var(--primary-light);
        color: var(--primary);
        padding: 12px 18px;
        border-radius: 18px 18px 2px 18px;
        margin-bottom: 15px;
        max-width: 80%;
        align-self: flex-end;
        margin-left: auto;
    }
    
    .bot-message {
        background-color: #F7FAFC;
        color: var(--text-dark);
        padding: 12px 18px;
        border-radius: 18px 18px 18px 2px;
        margin-bottom: 15px;
        max-width: 80%;
        border-left: 4px solid var(--primary);
    }
    
    /* Action buttons styling */
    .action-button-container {
        display: flex;
        gap: 20px;
        justify-content: center;
        margin-top: 25px;
    }
    
    .action-button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 500;
        transition: all 0.3s;
        width: 100%;
        cursor: pointer;
        text-align: center;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(45, 140, 255, 0.25);
    }
    
    .action-button-secondary {
        background-color: white;
        color: var(--primary);
        border: 1px solid var(--primary);
    }
    
    .action-button-secondary:hover {
        background-color: var(--primary-light);
    }
    
    .button-icon {
        margin-right: 8px;
        font-size: 18px;
    }
    
    /* Feature cards styling */
    .features-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 30px;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        flex: 1;
        min-width: 250px;
        box-shadow: var(--shadow);
        transition: transform 0.3s;
        border-top: 4px solid var(--primary);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 32px;
        color: var(--primary);
        margin-bottom: 15px;
    }
    
    /* Example queries styling */
    .examples-container {
        margin-top: 20px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .example-query {
        background-color: var(--primary-light);
        color: var(--primary);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .example-query:hover {
        background-color: var(--primary);
        color: white;
    }
    
    /* Message history container */
    .message-history {
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 20px;
        padding: 10px;
        border-radius: 8px;
        background-color: #F8FAFC;
    }
    
    /* Disclaimer styling */
    .disclaimer {
        font-size: 12px;
        color: var(--text-light);
        text-align: center;
        margin-top: 15px;
        padding: 10px;
        border-radius: 8px;
        background-color: rgba(113, 128, 150, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []  # Initialize as an empty list
    
    # Call navbar component
    navbar()
    
    # Hero Section
    with st.container():
        st.markdown('''
        <div class="hero">
            <div class="hero-content">
                <h1>AI Chatbot & Patient Data System</h1>
                <p>Get instant medical information and manage your health records in one place.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Main chat container
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Chat header
        st.markdown('''
        <div class="chat-header">
            <div class="chat-icon">💬</div>
            <h2>Chat with AI about Medical Issues</h2>
        </div>
        <p>Ask something about your health or medical concerns:</p>
        ''', unsafe_allow_html=True)
        
        # Example queries that users can click
        st.markdown('<div class="examples-container">', unsafe_allow_html=True)
        examples = [
            "What are symptoms of diabetes?",
            "How can I lower my blood pressure naturally?",
            "What should I do for a migraine?",
            "Is my medication causing this side effect?",
            "What vaccines do I need this year?"
        ]
        
        for i, example in enumerate(examples):
            if st.button(example, key=f"example_{i}"):
        # Add user message
                st.session_state.chat_history.append({"role": "user", "content": example})
                with st.spinner("Processing your question..."):
                    response, success = get_chat_response(example)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown('<div class="message-history">', unsafe_allow_html=True)
            for message in st.session_state.chat_history:
                role = message["role"]
                content = message["content"]
                if role == "user":
                    st.markdown(f'<div class="user-message">{content}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">{content}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input area
        user_input = st.text_area("Type your message", key="chat-input", placeholder="Type your medical question here...", height=120)
        
        # Get response button
        if st.button("Get Response", key="send_button"):
            if user_input:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Get AI response
                with st.spinner("Processing your question..."):
                    response, success = get_chat_response(user_input)
                
                # Add AI response to history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Force a rerun to display the updated chat
                st.rerun()
            else:
                st.warning("Please enter a message to chat.")
        
        # Medical disclaimer
        st.markdown('''
        <div class="disclaimer">
            <strong>Medical Disclaimer:</strong> The information provided by this AI assistant is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
        <div class="action-button" onclick="window.location.href='upload_patient_report.py'">
            <span class="button-icon">⬆</span>
            Upload Data
        </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown('''
        <div class="action-button action-button-secondary" onclick="window.location.href='retrieve_patient_data.py'">
            <span class="button-icon">📂</span>
            Retrieve Data
        </div>
        ''', unsafe_allow_html=True)
    
    # Features section
    st.markdown("<h2 style='margin-top: 40px;'>Key Features</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="features-container">', unsafe_allow_html=True)
        
        # Feature 1
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 style = "color: #4C585B;">AI-Powered Medical Assistance</h3>
            <p>Get instant answers to your health questions using advanced medical AI trained on the latest research.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Feature 2
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3 style = "color: #4C585B;">Secure Health Records</h3>
            <p>Your medical data is encrypted and stored securely. Only you control access to your information.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Feature 3
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 style = "color: #4C585B;">Health Analytics</h3>
            <p>Track your health metrics over time and receive personalized insights and recommendations.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    footer()

main()