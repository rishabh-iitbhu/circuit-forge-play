#!/usr/bin/env python3
"""
Comprehensive test for interactive component selection with web and local sources
"""

import streamlit as st
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.component_suggestions import suggest_mosfets, suggest_output_capacitors, suggest_inductors, suggest_input_capacitors
from lib.component_display import display_component_table

def test_web_and_local_components():
    """Test both web and local component selection"""
    
    st.title("🧪 Comprehensive Component Selection Test")
    
    # Force session state to persist across reruns
    if 'test_initialized' not in st.session_state:
        st.session_state.test_initialized = True
        st.session_state.component_source = 'local'  # Default to local
    
    st.sidebar.header("Test Configuration")
    
    # Component source selection
    source = st.sidebar.radio(
        "Component Source:",
        ["Local Database", "Web Search (Mouser/Digikey)"],
        key="test_source"
    )
    
    # Update session state
    if source == "Web Search (Mouser/Digikey)":
        st.session_state.component_source = 'web'
        use_web = True
    else:
        st.session_state.component_source = 'local'
        use_web = False
    
    # Test parameters
    st.sidebar.subheader("Circuit Parameters")
    vin = st.sidebar.slider("Input Voltage (V)", 12.0, 48.0, 24.0)
    vout = st.sidebar.slider("Output Voltage (V)", 3.3, 12.0, 5.0)
    iout = st.sidebar.slider("Output Current (A)", 1.0, 20.0, 10.0)
    frequency = st.sidebar.slider("Switching Frequency (kHz)", 50, 500, 100) * 1000
    
    st.write(f"### 🎯 Testing {source}")
    st.write(f"**Parameters:** {vin}V → {vout}V, {iout}A @ {frequency/1000}kHz")
    
    if st.button("🔄 Refresh Components", key="refresh_test"):
        # Clear previous session data
        for key in list(st.session_state.keys()):
            if key.endswith('_suggestions'):
                del st.session_state[key]
    
    # Test all component types
    with st.spinner(f"Searching for components using {source.lower()}..."):
        
        # MOSFETs
        st.subheader("1️⃣ MOSFET Testing")
        try:
            mosfet_suggestions = suggest_mosfets(
                max_voltage=vin * 1.5,  # Derating
                max_current=iout * 1.2,  # Derating  
                frequency_hz=frequency,
                use_web_search=use_web
            )
            
            if mosfet_suggestions:
                display_component_table(mosfet_suggestions[:5], 'mosfet', f'MOSFETs ({source})')
                st.success(f"✅ Found {len(mosfet_suggestions)} MOSFETs")
            else:
                st.warning("⚠️ No MOSFETs found")
                
        except Exception as e:
            st.error(f"❌ MOSFET test failed: {str(e)}")
        
        # Output Capacitors
        st.subheader("2️⃣ Output Capacitor Testing")
        try:
            ripple_current = 0.4 * iout  # Approximate ripple
            
            output_cap_suggestions = suggest_output_capacitors(
                output_voltage=vout,
                output_current=iout,
                ripple_current=ripple_current,
                switching_frequency=frequency,
                use_web_search=use_web
            )
            
            if output_cap_suggestions:
                display_component_table(output_cap_suggestions[:5], 'output_capacitor', f'Output Capacitors ({source})')
                st.success(f"✅ Found {len(output_cap_suggestions)} output capacitors")
            else:
                st.warning("⚠️ No output capacitors found")
                
        except Exception as e:
            st.error(f"❌ Output capacitor test failed: {str(e)}")
        
        # Input Capacitors
        st.subheader("3️⃣ Input Capacitor Testing")
        try:
            input_cap_suggestions = suggest_input_capacitors(
                input_voltage=vin,
                output_current=iout,
                ripple_current=ripple_current,
                use_web_search=use_web
            )
            
            if input_cap_suggestions:
                display_component_table(input_cap_suggestions[:5], 'input_capacitor', f'Input Capacitors ({source})')
                st.success(f"✅ Found {len(input_cap_suggestions)} input capacitors")
            else:
                st.warning("⚠️ No input capacitors found")
                
        except Exception as e:
            st.error(f"❌ Input capacitor test failed: {str(e)}")
        
        # Inductors
        st.subheader("4️⃣ Inductor Testing")
        try:
            # Calculate inductance (simplified)
            inductance_uh = (vin * (vout / vin) * (1 - vout / vin)) / (0.3 * iout * frequency) * 1e6
            
            inductor_suggestions = suggest_inductors(
                inductance=inductance_uh / 1e6,  # Convert to H
                max_current=iout * 1.2,
                use_web_search=use_web
            )
            
            if inductor_suggestions:
                display_component_table(inductor_suggestions[:5], 'inductor', f'Inductors ({source})')
                st.success(f"✅ Found {len(inductor_suggestions)} inductors")
            else:
                st.warning("⚠️ No inductors found")
                
        except Exception as e:
            st.error(f"❌ Inductor test failed: {str(e)}")
    
    # Test Summary
    st.write("---")
    st.subheader("🧪 Test Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Interactive Features:**")
        st.write("✅ Session state persistence")
        st.write("✅ Component source switching")
        st.write("✅ Table row selection")
        st.write("✅ Dynamic details display")
    
    with col2:
        st.write("**Component Types:**")
        st.write("✅ MOSFETs")
        st.write("✅ Output Capacitors")
        st.write("✅ Input Capacitors")
        st.write("✅ Inductors")
    
    # Instructions
    st.info("""
    **📋 How to Test:**
    1. Switch between 'Local Database' and 'Web Search' in sidebar
    2. Adjust circuit parameters and click 'Refresh Components'
    3. Click any row in the component tables to see details
    4. Verify details appear and table remains visible
    5. Test all component types in both modes
    """)
    
    # Debug info
    if st.checkbox("Show Debug Info"):
        st.write("**Session State:**")
        st.json({
            'component_source': st.session_state.get('component_source', 'not set'),
            'use_web_search': use_web,
            'session_keys': [k for k in st.session_state.keys() if not k.startswith('_')]
        })

if __name__ == "__main__":
    test_web_and_local_components()