"""
Minimal Circuit Designer Pro - For debugging deployment issues
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Circuit Designer Pro - Debug",
    page_icon="⚡",
    layout="wide"
)

def main():
    """Minimal application entry point for debugging"""
    
    st.title("⚡ Circuit Designer Pro")
    st.write("🎉 **App is working!** This is a minimal version to test deployment.")
    
    # Test basic functionality
    if st.button("Test Button"):
        st.success("Button works!")
    
    # Test imports step by step
    st.subheader("🔍 Debugging Information")
    
    try:
        import pandas as pd
        st.success("✅ Pandas imported successfully")
    except Exception as e:
        st.error(f"❌ Pandas import failed: {e}")
    
    try:
        from lib import calculations
        st.success("✅ Calculations module imported successfully")
    except Exception as e:
        st.error(f"❌ Calculations module import failed: {e}")
    
    try:
        from lib import component_data
        st.success("✅ Component data module imported successfully")
    except Exception as e:
        st.error(f"❌ Component data module import failed: {e}")
    
    try:
        from pages import buck_calculator
        st.success("✅ Buck calculator imported successfully")
    except Exception as e:
        st.error(f"❌ Buck calculator import failed: {e}")
    
    try:
        from pages import component_library
        st.success("✅ Component library imported successfully")
    except Exception as e:
        st.error(f"❌ Component library import failed: {e}")
    
    # Test file access
    import os
    st.subheader("📁 File System Check")
    current_dir = os.getcwd()
    st.write(f"Current directory: {current_dir}")
    
    # Check for assets folder
    assets_path = os.path.join(current_dir, 'assets')
    if os.path.exists(assets_path):
        st.success("✅ Assets folder found")
        
        # Check component data
        csv_path = os.path.join(assets_path, 'component_data')
        if os.path.exists(csv_path):
            st.success("✅ Component data folder found")
            files = os.listdir(csv_path)
            st.write(f"CSV files: {files}")
        else:
            st.warning("⚠️ Component data folder not found")
    else:
        st.error("❌ Assets folder not found")

if __name__ == "__main__":
    main()