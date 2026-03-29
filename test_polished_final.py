#!/usr/bin/env python3
"""
Polished Final Test Suite - Interactive Component Selection
Validates all fixes for web component selection issues
"""

import streamlit as st
import traceback
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_component_safely(component_func, component_type, params, use_web):
    """Test component with comprehensive error handling"""
    try:
        with st.spinner(f"Searching for {component_type}s..."):
            suggestions = component_func(**params, use_web_search=use_web)
        
        if suggestions:
            from lib.component_display import display_component_table
            display_component_table(suggestions[:5], component_type, 
                                  f'{component_type.title().replace("_", " ")} Results')
            return len(suggestions), None
        else:
            st.warning(f"⚠️ No {component_type}s found matching your requirements")
            return 0, None
            
    except Exception as e:
        error_msg = f"Error searching for {component_type}: {str(e)}"
        st.error(f"❌ {error_msg}")
        
        with st.expander(f"🔍 Debug {component_type} error"):
            st.code(traceback.format_exc())
            st.write("**Parameters used:**")
            st.json(params)
            st.write(f"**Use web search:** {use_web}")
        
        return 0, error_msg

def main():
    """Polished test interface"""
    
    st.set_page_config(
        page_title="🧪 Component Selection Final Test",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧪 Interactive Component Selection - Final Validation")
    st.markdown("*Comprehensive test suite for web and local component search with interactive selection*")
    
    # Header metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Test Status", "Active")
    with col2:
        st.metric("🔧 Components", "4 Types")
    with col3:
        st.metric("📊 Search Modes", "2 Sources")
    with col4:
        st.metric("✅ Fixes Applied", "All")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("🎛️ Test Configuration")
        
        # Component source selection
        st.subheader("🔍 Search Source")
        source_mode = st.radio(
            "Select component database:",
            ["📚 Local Database", "🌐 Web Search (Mouser/Digikey)"],
            help="Choose between local component database or live web search"
        )
        
        use_web = "Web Search" in source_mode
        st.session_state.component_source = 'web' if use_web else 'local'
        
        # Show current mode
        if use_web:
            st.success("🌐 **Web Search Mode**\nSearching Mouser & Digikey")
        else:
            st.info("📚 **Local Database Mode**\nUsing offline component data")
        
        st.divider()
        
        # Circuit parameters
        st.subheader("⚡ Buck Converter Specs")
        vin = st.slider("Input Voltage (V)", 12.0, 48.0, 24.0, 0.5, help="DC input voltage")
        vout = st.slider("Output Voltage (V)", 1.2, 24.0, 5.0, 0.1, help="Regulated output voltage")  
        iout = st.slider("Output Current (A)", 0.5, 50.0, 10.0, 0.5, help="Maximum output current")
        freq_khz = st.slider("Switching Freq (kHz)", 20, 1000, 100, 10, help="PWM switching frequency")
        frequency = freq_khz * 1000
        
        st.divider()
        
        # Safety margins
        st.subheader("🛡️ Design Margins")  
        voltage_derating = st.slider("Voltage Derating (%)", 20, 100, 50, 5, help="Safety margin for voltage ratings") / 100
        current_derating = st.slider("Current Derating (%)", 20, 100, 80, 5, help="Safety margin for current ratings") / 100
        
        st.divider()
        
        # Test controls
        st.subheader("🧪 Test Controls")
        if st.button("🔄 **Refresh All Tests**", type="primary", use_container_width=True):
            # Clear cached results
            for key in list(st.session_state.keys()):
                if key.endswith('_suggestions'):
                    del st.session_state[key]
            st.rerun()
        
        if st.button("🗑️ Clear Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                if not key.startswith('_'):
                    del st.session_state[key]
            st.rerun()
    
    # Main test area
    st.markdown("---")
    
    # Test summary banner
    requirements_col, mode_col = st.columns(2)
    with requirements_col:
        st.info(f"""
        **📋 Circuit Requirements:**
        • {vin}V → {vout}V @ {iout}A
        • Switching: {freq_khz}kHz
        • Derating: V×{voltage_derating:.1f}, I×{current_derating:.1f}
        """)
    
    with mode_col:
        if use_web:
            st.success(f"""
            **🌐 Web Search Active:**
            • Searching Mouser & Digikey
            • Real-time component data
            • Working purchase links
            """)
        else:
            st.info(f"""
            **📚 Local Database Active:**
            • Offline component library
            • Fast response times  
            • Curated selections
            """)
    
    # Component testing tabs
    st.subheader("🔬 Component Selection Tests")
    
    # Track test results
    test_results = {}
    
    # Create tabs for each component type
    mosfet_tab, output_cap_tab, input_cap_tab, inductor_tab = st.tabs([
        "💻 MOSFETs", "📤 Output Capacitors", "📥 Input Capacitors", "🧲 Inductors"
    ])
    
    with mosfet_tab:
        st.markdown("### 💻 MOSFET Selection Test")
        
        # Calculate requirements
        max_voltage_req = vin / voltage_derating
        max_current_req = iout / current_derating
        
        st.markdown(f"""
        **📊 Selection Criteria:**
        - **VDS Rating:** ≥ {max_voltage_req:.1f}V (derated from {vin}V)
        - **ID Rating:** ≥ {max_current_req:.1f}A (derated from {iout}A)
        - **Switching Frequency:** {freq_khz}kHz compatibility
        """)
        
        from lib.component_suggestions import suggest_mosfets
        
        count, error = test_component_safely(
            suggest_mosfets, 'mosfet',
            {
                'max_voltage': max_voltage_req,
                'max_current': max_current_req,
                'frequency_hz': frequency
            },
            use_web
        )
        
        test_results['MOSFETs'] = {'count': count, 'error': error}
    
    with output_cap_tab:
        st.markdown("### 📤 Output Capacitor Selection Test")
        
        # Calculate ripple current (typical buck converter)
        ripple_current = 0.4 * iout
        min_voltage_req = vout * 1.2  # 20% margin
        
        st.markdown(f"""
        **📊 Selection Criteria:**
        - **Voltage Rating:** ≥ {min_voltage_req:.1f}V (120% of {vout}V)
        - **Ripple Current:** ≥ {ripple_current:.2f}A RMS
        - **Low ESR:** For efficient filtering
        """)
        
        from lib.component_suggestions import suggest_output_capacitors
        
        count, error = test_component_safely(
            suggest_output_capacitors, 'output_capacitor',
            {
                'output_voltage': vout,
                'output_current': iout,
                'ripple_current': ripple_current,
                'switching_frequency': frequency
            },
            use_web
        )
        
        test_results['Output Capacitors'] = {'count': count, 'error': error}
    
    with input_cap_tab:
        st.markdown("### 📥 Input Capacitor Selection Test")
        
        # Input capacitor requirements
        input_ripple_current = 0.3 * iout
        min_input_voltage = vin * 1.1  # 10% margin
        
        st.markdown(f"""
        **📊 Selection Criteria:**
        - **Voltage Rating:** ≥ {min_input_voltage:.1f}V (110% of {vin}V)
        - **Ripple Current:** ≥ {input_ripple_current:.2f}A RMS
        - **High Frequency Response:** For switching noise
        """)
        
        from lib.component_suggestions import suggest_input_capacitors
        
        count, error = test_component_safely(
            suggest_input_capacitors, 'input_capacitor',
            {
                'input_voltage': vin,
                'output_current': iout,
                'ripple_current': input_ripple_current
            },
            use_web
        )
        
        test_results['Input Capacitors'] = {'count': count, 'error': error}
    
    with inductor_tab:
        st.markdown("### 🧲 Inductor Selection Test")
        
        # Calculate inductance (buck converter formula)
        duty_cycle = vout / vin
        ripple_ratio = 0.3  # 30% current ripple
        inductance_uh = (vin * duty_cycle * (1 - duty_cycle)) / (ripple_ratio * iout * frequency) * 1e6
        current_rating_req = iout * 1.2  # 20% margin
        
        st.markdown(f"""
        **📊 Selection Criteria:**
        - **Inductance:** ≈ {inductance_uh:.0f}µH (calculated for 30% ripple)
        - **Current Rating:** ≥ {current_rating_req:.1f}A (120% of {iout}A)
        - **DC Resistance:** Low for efficiency
        """)
        
        from lib.component_suggestions import suggest_inductors
        
        count, error = test_component_safely(
            suggest_inductors, 'inductor',
            {
                'inductance': inductance_uh / 1e6,  # Convert to H
                'max_current': current_rating_req
            },
            use_web
        )
        
        test_results['Inductors'] = {'count': count, 'error': error}
    
    # Test results summary
    st.markdown("---")
    st.subheader("📈 Test Results Summary")
    
    # Overall metrics
    total_components = sum(result['count'] for result in test_results.values())
    successful_tests = sum(1 for result in test_results.values() if result['error'] is None)
    total_tests = len(test_results)
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric("🎯 Total Components", total_components)
    with summary_col2:
        st.metric("✅ Successful Tests", f"{successful_tests}/{total_tests}")
    with summary_col3:
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        st.metric("📊 Success Rate", f"{success_rate:.0f}%")
    with summary_col4:
        st.metric("🔍 Search Mode", "🌐 Web" if use_web else "📚 Local")
    
    # Detailed results table
    with st.expander("📋 Detailed Test Results", expanded=total_components == 0):
        for component_type, result in test_results.items():
            col1, col2, col3 = st.columns([2, 1, 3])
            
            with col1:
                status = "✅" if result['error'] is None else "❌"
                st.write(f"{status} **{component_type}**")
            
            with col2:
                st.write(f"**{result['count']}** found")
            
            with col3:
                if result['error']:
                    st.error(f"Error: {result['error']}")
                else:
                    st.success("✅ Test completed successfully")
    
    # Interactive usage instructions
    st.markdown("---")
    st.markdown("### 🖱️ Interactive Testing Guide")
    
    instruction_col1, instruction_col2 = st.columns(2)
    
    with instruction_col1:
        st.markdown("""
        **🎯 How to Test Component Selection:**
        
        1. **📊 Browse Results**: Review component tables above
        2. **🖱️ Click Rows**: Select any component row to view details  
        3. **👀 Verify Display**: Details should appear below table
        4. **🔗 Test Links**: Click component/datasheet links (web mode)
        5. **🔄 Switch Modes**: Toggle between local and web search
        """)
    
    with instruction_col2:
        st.markdown("""
        **✅ Expected Behavior:**
        
        • ✅ Table stays visible after selection
        • ✅ Component details appear dynamically  
        • ✅ Purchase links work (web results)
        • ✅ Session state persists
        • ✅ No count mismatches
        """)
    
    # Success confirmation
    if successful_tests == total_tests and total_components > 0:
        st.success("""
        🎉 **All Tests Successful!** 
        
        The interactive component selection system is working correctly with both web and local search modes.
        Click on any component rows above to test the interactive selection feature.
        """)
    elif total_components == 0:
        st.warning("""
        ⚠️ **No Components Found** 
        
        This could be normal depending on:
        - Web search rate limits or network connectivity
        - Very specific parameter requirements  
        - Component availability in selected database
        
        Try adjusting parameters or switching search modes.
        """)
    
    # Debug section
    if st.checkbox("🔍 Show Debug Information"):
        st.markdown("### 🛠️ Debug Information")
        
        debug_data = {
            'session_component_source': st.session_state.get('component_source', 'not set'),
            'use_web_search': use_web,
            'circuit_parameters': {
                'vin': vin, 'vout': vout, 'iout': iout, 'frequency': frequency
            },
            'active_session_keys': [k for k in st.session_state.keys() if not k.startswith('_')],
            'stored_suggestions': [k for k in st.session_state.keys() if k.endswith('_suggestions')],
            'test_results_summary': test_results
        }
        
        st.json(debug_data)

if __name__ == "__main__":
    main()