import streamlit as st

def load_styles():
    # Custom CSS for a modern, clean healthcare UI
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');
            
            :root {
                --primary: #2D8CFF;
                --primary-light: #E6F1FF;
                --secondary: #34C759;
                --text-dark: #2D3748;
                --text-light: #718096;
                --bg-light: #F7FAFC;
                --bg-white: #FFFFFF;
                --shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            
            /* Base Styling */
            .stApp {
                background-color: var(--bg-light);
                font-family: 'Poppins', sans-serif;
            }
            
            h1, h2, h3, h4, h5 {
                font-family: 'Montserrat', sans-serif;
                font-weight: 600;
            }
            
            p {
                font-family: 'Poppins', sans-serif;
                color: var(--text-light);
                line-height: 1.6;
            }
            
            /* Navbar Styling */
            .navbar {
                background-color: var(--bg-white);
                padding: 15px 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: var(--shadow);
                border-radius: 12px;
                margin-bottom: 20px;
            }
            
            .navbar-links {
                display: flex;
                align-items: center;
            }
            
            .navbar a {
                text-decoration: none;
                margin: 0 15px;
                color: var(--text-dark);
                font-weight: 500;
                font-size: 16px;
                transition: 0.3s;
                padding: 8px 15px;
                border-radius: 6px;
            }
            
            .navbar a:hover {
                background-color: var(--primary-light);
                color: var(--primary);
            }
            
            /* Branding */
            .brand {
                font-size: 24px;
                font-weight: 700;
                font-family: 'Montserrat', sans-serif; 
                color: var(--primary);
                display: flex;
                align-items: center;
            }
            
            /* Containers */
            .card {
                background-color: var(--bg-white);
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 20px;
                box-shadow: var(--shadow);
                transition: transform 0.3s;
            }
            
            .card:hover {
                transform: translateY(-5px);
            }
            
            /* Hero Section */
            .hero {
                text-align: center;
                padding: 40px 20px;
                background-color: var(--bg-white);
                border-radius: 12px;
                box-shadow: var(--shadow);
                margin-bottom: 30px;
                background-image: url('https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=1000&q=80');
                background-size: cover;
                background-position: center;
                position: relative;
                overflow: hidden;
            }
            
            .hero::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(255, 255, 255, 0.9);
                z-index: 1;
            }
            
            .hero-content {
                position: relative;
                z-index: 2;
            }
            
            .hero h1 {
                color: var(--primary);
                font-size: 2.5rem;
                margin-bottom: 15px;
            }
            
            .hero p {
                color: var(--text-light);
                font-size: 1.1rem;
                max-width: 700px;
                margin: 0 auto 25px;
            }
            
            /* Buttons */
            .btn {
                background-color: var(--primary);
                color: white !important;
                padding: 12px 24px;
                border-radius: 8px;
                text-decoration: none !important;
                font-size: 16px;
                font-weight: 600;
                box-shadow: 0 4px 6px rgba(45, 140, 255, 0.2);
                transition: 0.3s;
                display: inline-block;
                border: none;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 8px rgba(45, 140, 255, 0.25);
            }
            
            .btn-outline {
                background-color: transparent;
                color: var(--primary) !important;
                border: 2px solid var(--primary);
            }
            
            .btn-outline:hover {
                background-color: var(--primary-light);
            }
            
            /* Section Headers */
            .section-header {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                color: var(--primary);
                font-size: 1.5rem;
            }
            
            .section-header i {
                margin-right: 10px;
                font-size: 1.8rem;
            }
            
            /* File Uploader Styling */
            .stFileUploader {
                padding: 15px !important;
                border-radius: 10px !important;
                border: 2px dashed var(--primary-light) !important;
                background-color: white !important;
            }
            
            .stFileUploader:hover {
                border-color: var(--primary) !important;
            }
            
            /* Form Elements */
            .stTextInput > div > div > input {
                border-radius: 8px !important;
                padding: 10px 15px !important; 
                border: 1px solid #E2E8F0 !important;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: var(--primary) !important;
                box-shadow: 0 0 0 2px rgba(45, 140, 255, 0.2) !important;
            }
            
            button {
                border-radius: 8px !important;
                padding: 10px 20px !important;
                background-color: var(--primary) !important;
                color: white !important;
                font-weight: 500 !important;
            }
            
            /* Success/Info Messages */
            .success-message {
                background-color: rgba(52, 199, 89, 0.1);
                border-left: 4px solid var(--secondary);
                padding: 15px;
                border-radius: 4px;
                margin: 15px 0;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .navbar {
                    flex-direction: column;
                    text-align: center;
                }
                
                .navbar-links {
                    margin-top: 15px;
                    flex-wrap: wrap;
                    justify-content: center;
                }
                
                .navbar a {
                    margin: 5px;
                }
                
                .hero h1 {
                    font-size: 2rem;
                }
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #d1d5db;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #a0aec0;
            }
            
            /* Footer */
            .footer {
                text-align: center;
                padding: 20px;
                background-color: var(--bg-white);
                color: var(--text-light);
                border-radius: 12px;
                box-shadow: var(--shadow);
                margin-top: 30px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )