import streamlit as st

def footer():
    # Footer Section
    st.markdown(
        """
        <div class="footer">
            <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 15px;">
                <a href="#" style="color: var(--text-light); text-decoration: none;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
                    </svg>
                </a>
                <a href="#" style="color: var(--text-light); text-decoration: none;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                        <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                        <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                    </svg>
                </a>
                <a href="#" style="color: var(--text-light); text-decoration: none;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
                    </svg>
                </a>
                <a href="#" style="color: var(--text-light); text-decoration: none;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                        <rect x="2" y="9" width="4" height="12"></rect>
                        <circle cx="4" cy="4" r="2"></circle>
                    </svg>
                </a>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="#" style="color: var(--text-light); text-decoration: none; margin: 0 10px;">About Us</a>
                <a href="#" style="color: var(--text-light); text-decoration: none; margin: 0 10px;">Privacy Policy</a>
                <a href="#" style="color: var(--text-light); text-decoration: none; margin: 0 10px;">Terms of Service</a>
            </div>
            <p style="margin: 0; color: var(--text-light); font-size: 0.9rem;">© 2025 MediMind AI. All rights reserved.</p>
            <p style="margin: 5px 0 0; color: var(--text-light); font-size: 0.8rem;">Powered by AI & Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )