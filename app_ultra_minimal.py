"""
Circuit Designer Pro - Ultra Minimal Debug
"""

import streamlit as st

# Minimal page config
st.set_page_config(page_title="Debug", page_icon="⚡")

# Immediate output
st.title("🎉 App is Loading!")
st.write("If you see this, basic Streamlit is working.")

# Test button
if st.button("Click me!"):
    st.success("✅ Button works!")

# Progressive testing
st.subheader("Testing Step by Step...")

# Test 1: Basic imports
try:
    import os
    st.write("✅ os module works")
    st.write(f"Current directory: {os.getcwd()}")
except Exception as e:
    st.error(f"❌ os module failed: {e}")

# Test 2: Pandas
if st.button("Test pandas import"):
    try:
        import pandas as pd
        st.success("✅ pandas imported successfully")
    except Exception as e:
        st.error(f"❌ pandas failed: {e}")

# Test 3: Check file structure
if st.button("Check file structure"):
    try:
        import os
        files = os.listdir(".")
        st.write("📁 Files in current directory:")
        for f in files[:10]:  # Show first 10
            st.write(f"- {f}")
    except Exception as e:
        st.error(f"❌ File listing failed: {e}")

# Test 4: Check lib folder
if st.button("Check lib folder"):
    try:
        import os
        if os.path.exists("lib"):
            lib_files = os.listdir("lib")
            st.write("📁 Files in lib folder:")
            for f in lib_files:
                st.write(f"- {f}")
        else:
            st.error("❌ lib folder not found")
    except Exception as e:
        st.error(f"❌ lib folder check failed: {e}")

st.write("---")
st.write("🔍 This ultra-minimal version should load instantly.")
st.write("If this is still hanging, the issue is with Streamlit Cloud environment setup.")