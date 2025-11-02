"""
Circuit Designer Pro - Streamlit Application (Debug Version)
Minimal version to isolate deployment issues
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Circuit Designer Pro - Debug",
    page_icon="⚡",
    layout="wide"
)

def test_imports():
    """Test all imports step by step"""
    import_results = {}
    
    # Test pandas
    try:
        import pandas as pd
        import_results['pandas'] = "✅ Success"
    except Exception as e:
        import_results['pandas'] = f"❌ Error: {e}"
    
    # Test numpy
    try:
        import numpy as np
        import_results['numpy'] = "✅ Success"
    except Exception as e:
        import_results['numpy'] = f"❌ Error: {e}"
    
    # Test plotly
    try:
        import plotly
        import_results['plotly'] = "✅ Success"
    except Exception as e:
        import_results['plotly'] = f"❌ Error: {e}"
    
    # Test python-docx
    try:
        from docx import Document
        import_results['python-docx'] = "✅ Success"
    except Exception as e:
        import_results['python-docx'] = f"❌ Error: {e}"
    
    return import_results

def test_file_system():
    """Test file system access"""
    import os
    
    results = {}
    
    # Current directory
    cwd = os.getcwd()
    results['current_dir'] = cwd
    
    # Check for key directories
    dirs_to_check = ['lib', 'pages', 'assets', 'assets/component_data', 'assets/design_heuristics']
    
    for dir_name in dirs_to_check:
        path = os.path.join(cwd, dir_name)
        if os.path.exists(path):
            results[dir_name] = f"✅ Found: {path}"
            if os.path.isdir(path):
                try:
                    files = os.listdir(path)[:5]  # First 5 files
                    results[f"{dir_name}_files"] = files
                except:
                    results[f"{dir_name}_files"] = "Could not list files"
        else:
            results[dir_name] = f"❌ Not found: {path}"
    
    return results

def test_module_imports():
    """Test importing our custom modules"""
    results = {}
    
    # Test lib modules
    lib_modules = ['calculations', 'component_data', 'component_suggestions', 'document_analyzer']
    
    for module in lib_modules:
        try:
            exec(f"from lib import {module}")
            results[f"lib.{module}"] = "✅ Success"
        except Exception as e:
            results[f"lib.{module}"] = f"❌ Error: {e}"
    
    # Test page modules
    page_modules = ['buck_calculator', 'component_library']
    
    for module in page_modules:
        try:
            exec(f"from pages import {module}")
            results[f"pages.{module}"] = "✅ Success"
        except Exception as e:
            results[f"pages.{module}"] = f"❌ Error: {e}"
    
    return results

def main():
    """Main debug application"""
    
    st.title("🔍 Circuit Designer Pro - Debug Mode")
    st.write("This debug version helps identify deployment issues.")
    
    # Test 1: Basic Streamlit functionality
    st.header("1. Basic Streamlit Test")
    if st.button("Test Button"):
        st.success("✅ Basic Streamlit functionality works!")
    
    # Test 2: Package imports
    st.header("2. Package Import Tests")
    
    with st.spinner("Testing package imports..."):
        import_results = test_imports()
    
    for package, result in import_results.items():
        st.write(f"**{package}**: {result}")
    
    # Test 3: File system
    st.header("3. File System Tests")
    
    with st.spinner("Testing file system access..."):
        fs_results = test_file_system()
    
    for item, result in fs_results.items():
        if not item.endswith('_files'):
            st.write(f"**{item}**: {result}")
            if f"{item}_files" in fs_results:
                st.write(f"  📁 Files: {fs_results[f'{item}_files']}")
    
    # Test 4: Module imports
    st.header("4. Custom Module Tests")
    
    with st.spinner("Testing custom module imports..."):
        module_results = test_module_imports()
    
    for module, result in module_results.items():
        st.write(f"**{module}**: {result}")
    
    # Test 5: Component data loading
    st.header("5. Component Data Loading Test")
    
    try:
        from lib import component_data
        
        st.write("Testing MOSFET data loading...")
        mosfets = component_data.load_mosfets_from_csv()
        st.write(f"✅ Loaded {len(mosfets)} MOSFETs")
        
        st.write("Testing Capacitor data loading...")
        capacitors = component_data.load_capacitors_from_csv()
        st.write(f"✅ Loaded {len(capacitors)} Capacitors")
        
        st.write("Testing Inductor data loading...")
        inductors = component_data.load_inductors_from_csv()
        st.write(f"✅ Loaded {len(inductors)} Inductors")
        
    except Exception as e:
        st.error(f"❌ Component data loading failed: {e}")
        st.write("This might be the source of the deployment issue!")
    
    st.success("🎉 Debug tests completed!")

if __name__ == "__main__":
    main()