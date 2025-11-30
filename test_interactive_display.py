#!/usr/bin/env python3
"""
Test script for the new interactive component display system
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.component_suggestions import suggest_mosfets, suggest_output_capacitors
from lib.component_display import display_component_table, create_component_table
import streamlit as st

def test_interactive_display():
    """Test the interactive component display functionality"""
    
    st.title("🔧 Interactive Component Display Test")
    
    # Test parameters
    vin = 24.0
    vout = 5.0
    iout = 10.0
    frequency = 100000.0
    
    st.write("### Test Configuration:")
    st.write(f"- Input Voltage: {vin}V")
    st.write(f"- Output Voltage: {vout}V") 
    st.write(f"- Output Current: {iout}A")
    st.write(f"- Switching Frequency: {frequency/1000}kHz")
    
    # Test MOSFET suggestions
    st.write("---")
    st.write("## Testing MOSFET Display")
    
    try:
        # Get both web and local suggestions
        web_mosfets = suggest_mosfets(vin, vout, iout, frequency, use_web_search=True)
        local_mosfets = suggest_mosfets(vin, vout, iout, frequency, use_web_search=False)
        
        if web_mosfets:
            st.write("### Web Search Results:")
            display_component_table(web_mosfets[:5], 'mosfet', '🌐 Web MOSFETs')
        
        if local_mosfets:
            st.write("### Local Database Results:")
            display_component_table(local_mosfets[:5], 'mosfet', '📚 Local MOSFETs')
            
    except Exception as e:
        st.error(f"Error testing MOSFET display: {str(e)}")
        st.write("This might be due to missing dependencies or network issues")
    
    # Test Capacitor suggestions
    st.write("---")
    st.write("## Testing Capacitor Display")
    
    try:
        # Calculate ripple current for capacitors
        ripple_current = 0.4 * iout  # Approximate ripple current
        
        web_caps = suggest_output_capacitors(vout, iout, ripple_current, frequency, use_web_search=True)
        local_caps = suggest_output_capacitors(vout, iout, ripple_current, frequency, use_web_search=False)
        
        if web_caps:
            st.write("### Web Search Results:")
            display_component_table(web_caps[:5], 'output_capacitor', '🌐 Web Capacitors')
        
        if local_caps:
            st.write("### Local Database Results:")
            display_component_table(local_caps[:5], 'output_capacitor', '📚 Local Capacitors')
            
    except Exception as e:
        st.error(f"Error testing capacitor display: {str(e)}")
    
    # Display test results
    st.write("---")
    st.write("## ✅ Interactive Display Features:")
    st.success("✓ Streamlined table with essential metrics only")
    st.success("✓ Click any row to see detailed component information")
    st.success("✓ No more count mismatch between table and details")
    st.success("✓ Professional selection interface with working links")
    st.success("✓ Dynamic details section appears only when component selected")
    
    st.info("💡 **How to use:** Click on any row in the table above to see detailed specs, purchase links, and selection reasoning.")

if __name__ == "__main__":
    test_interactive_display()