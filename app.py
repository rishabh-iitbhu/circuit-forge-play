"""
Circuit Designer Pro - Streamlit Application
Main application file for circuit design with PFC and Buck converter calculators
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Circuit Designer Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
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
    
    # Header
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown('<div class="main-header">⚡ Circuit Designer Pro</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Design circuits with AI-powered component calculations and grounded theory</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("📚 Component Library", use_container_width=True):
            st.session_state.show_library = not st.session_state.get('show_library', False)
    
    # Show component library in sidebar if requested
    if st.session_state.get('show_library', False):
        with st.sidebar:
            st.header("Component Library")
            component_library.show_sidebar_library()
    
    # Main navigation
    selected = st.radio(
        "Select Circuit Type",
        ["PFC Circuit", "Buck Converter"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Route to appropriate page
    if selected == "PFC Circuit":
        pfc_calculator.show()
    elif selected == "Buck Converter":
        buck_calculator.show()

if __name__ == "__main__":
    main()
