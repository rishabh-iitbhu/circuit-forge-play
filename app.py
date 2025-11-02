"""
Circuit Designer Pro - Streamlit Application
Main application file for circuit design with PFC and Buck converter calculators
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Circuit Designer Pro",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Hide sidebar completely with multiple selectors */
    .css-1d391kg, .css-1y4p8pa, .css-17eq0hr, .css-1lcbmhc, .css-1outpf7 {
        display: none !important;
    }
    
    section[data-testid="stSidebar"], 
    .stSidebar, 
    div[data-testid="stSidebar"],
    .sidebar {
        display: none !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
    }
    
    /* Force full width for main content */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
        width: 100% !important;
    }
    
    .stApp > div:first-child {
        margin-left: 0 !important;
    }
    
    /* Custom button styling for Component Library */
    .stButton > button[kind="secondary"] {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #5a67d8;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        color: #64748b;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .component-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Import pages
from pages import pfc_calculator, buck_calculator, component_library

def main():
    """Main application entry point"""
    
    # Header with Component Library button in top-right
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<div class="main-header">⚡ Circuit Designer Pro</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Design circuits with AI-powered component calculations and grounded theory</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        if st.button("📚 Component Library", type="secondary"):
            st.session_state.page = "Component Library"
    
    # Main navigation for circuit types only
    selected = st.radio(
        "Select Circuit Type",
        ["Buck Converter"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Route to appropriate page
    if st.session_state.get('page') == "Component Library":
        component_library.show()
        # Add back button
        if st.button("← Back to Circuits"):
            st.session_state.page = None
            st.rerun()
    elif selected == "Buck Converter":
        st.session_state.page = None
        buck_calculator.show()

if __name__ == "__main__":
    main()
