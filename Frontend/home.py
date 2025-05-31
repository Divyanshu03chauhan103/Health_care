import streamlit as st
from navbar import navbar
from styles import load_styles
from footer import footer

# Set Page Configuration
st.set_page_config(
    page_title="MediMind AI | Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom styles
load_styles()

# Display navbar
navbar()

# Hero Section with Modern Design
st.markdown(
    """
    <div class="hero" id="home">
        <div class="hero-content">
            <h1>
                <span style="color: #2D8CFF;">Medi</span><span style="color: #34C759;">Mind</span> AI
            </h1>
            <h2 style="margin-top: 0; color: #4A5568; font-size: 1.5rem; font-weight: 500;">Transforming Healthcare with Artificial Intelligence</h2>
            <p>Experience the future of healthcare with our AI-powered platform. Get instant insights from patient reports, manage hospital operations efficiently, and access reliable medical information with ease.</p>
            <div style="display: flex; justify-content: center; gap: 15px;">
                <a class="btn" href="/app">  
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                    </svg>
                    Start Diagnosis
                </a>
                <a class="btn btn-outline" href="/gpt">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    Search Medical Info
                </a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Create two columns for main content
col1, col2 = st.columns([2, 1])

st.markdown(
    """
    <div class="card" id="contact">
        <div class="section-header">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2D8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </svg>
            <h2 style="margin: 0 0 0 10px;">Contact Us - </h2>
            <h4>You can contact us using the following number:</h4>
        </div><p>9283112344</p><p>Have questions? Reach out to our support team for assistance.</p>
    </div>
    """,
    unsafe_allow_html=True
)

footer()

