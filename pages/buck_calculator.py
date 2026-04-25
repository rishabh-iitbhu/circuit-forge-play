"""
Buck Converter Calculator Page
"""

import streamlit as st
from lib.calculations import CircuitCalculator, BuckInputs, validate_inputs
from lib.component_suggestions import suggest_mosfets, suggest_capacitors, suggest_inductors, suggest_input_capacitors
from lib.component_data import reload_component_data, INDUCTOR_LIBRARY
import os

def get_component_ranges():
    """
    Get available parameter ranges from component database
    """
    try:
        # Load component data to get ranges
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # MOSFET ranges
        mosfet_ranges = {
            'voltage': (25, 650),  # From component data: 25V to 650V
            'current': (18, 150),  # From component data: 18A to 150A
        }
        
        # Capacitor ranges  
        capacitor_ranges = {
            'voltage': (25, 63),   # From component data: 25V to 63V
            'capacitance': (10, 330), # From component data: 10µF to 330µF
        }
        
        # Inductor ranges
        inductor_ranges = {
            'inductance': (220, 10000), # From component data: 220µH to 10mH
            'current': (0.48, 4.5),     # From component data: 0.48A to 4.5A (max from Würth)
        }
        
        return {
            'input_voltage': (10, 60),    # Based on MOSFET capabilities
            'output_voltage': (3.3, 25),  # Based on capacitor ratings
            'power': (2, 20),             # Based on inductor current capability (4.5A * 5V = 22.5W max)
            'frequency': (50000, 1000000) # Optimal switching range
        }
        
    except Exception:
        # Fallback ranges if data loading fails
        return {
            'input_voltage': (10, 60),
            'output_voltage': (3.3, 25), 
            'power': (5, 100),
            'frequency': (50000, 1000000)
        }


def compute_available_inductor_ranges(required_inductance_uh, max_current, inductor_suggestions=None, use_web_search=False):
    """
    Compute available inductor ranges depending on selected source.

    Args:
        required_inductance_uh: Required inductance in µH
        max_current: Required max current in A
        inductor_suggestions: Optional list of ComponentSuggestion returned when using web search
        use_web_search: If True, derive ranges from web suggestions, otherwise from local INDUCTOR_LIBRARY

    Returns:
        (L_min, L_max, I_min, I_max, inductor_ok)
    """
    try:
        if use_web_search and inductor_suggestions:
            inductances = [getattr(s.component, 'inductance', 0) for s in inductor_suggestions if getattr(s.component, 'inductance', 0) > 0]
            currents = [getattr(s.component, 'current', 0) for s in inductor_suggestions if getattr(s.component, 'current', 0) > 0]
        else:
            # Local DB fallback
            from lib.component_data import INDUCTOR_LIBRARY
            inductances = [i.inductance for i in INDUCTOR_LIBRARY if hasattr(i, 'inductance') and i.inductance > 0]
            currents = [i.current for i in INDUCTOR_LIBRARY if hasattr(i, 'current') and i.current > 0]

        if inductances:
            L_min = min(inductances)
            L_max = max(inductances)
        else:
            L_min, L_max = 0, 0

        if currents:
            I_min = min(currents)
            I_max = max(currents)
        else:
            I_min, I_max = 0, 0

        inductor_ok = (L_min <= required_inductance_uh <= L_max) and (max_current <= I_max)
        return (L_min, L_max, I_min, I_max, inductor_ok)
    except Exception:
        return (0, 0, 0, 0, False)

def check_component_availability(mosfet_suggestions, input_cap_suggestions, output_cap_suggestions, inductor_suggestions):
    """
    Check if suitable components are available for simulation
    """
    try:
        # Check if we have at least one suggestion for each critical component
        has_mosfets = mosfet_suggestions and len(mosfet_suggestions) > 0
        has_input_caps = input_cap_suggestions and len(input_cap_suggestions) > 0
        has_output_caps = output_cap_suggestions and len(output_cap_suggestions) > 0
        has_inductors = inductor_suggestions and len(inductor_suggestions) > 0
        
        # Debug output
        st.write(f"🔍 **Component Check:** MOSFETs: {len(mosfet_suggestions) if mosfet_suggestions else 0}, "
                f"Input Caps: {len(input_cap_suggestions) if input_cap_suggestions else 0}, "
                f"Output Caps: {len(output_cap_suggestions) if output_cap_suggestions else 0}, "
                f"Inductors: {len(inductor_suggestions) if inductor_suggestions else 0}")
        
        # For simulation, we need at least inductors and output capacitors
        # Input capacitors and MOSFETs are less critical for basic simulation
        return has_output_caps and has_inductors
        
    except Exception as e:
        st.error(f"Error checking components: {e}")
        return False



def show():
    """Display Buck converter calculator page"""
    
    # Always reload component database on page load to ensure ranges are sourced
    try:
        reload_component_data()
    except Exception:
        # Non-fatal: proceed with whatever data is loaded
        pass

    st.header("🔋 Buck Converter Designer")
    
    st.markdown("---")
    
    # Create three columns for input parameters
    col1, col2, col3 = st.columns(3)
    
    # Get dynamic ranges based on available components
    ranges = get_component_ranges()
    
    # Check if auto-fix values should be applied
    auto_fix = st.session_state.get('auto_fix_applied', {})
    if auto_fix:
        # Clear the auto-fix flag after one use
        if 'auto_fix_applied' in st.session_state:
            del st.session_state['auto_fix_applied']
    
    with col1:
        st.subheader("⚡ Voltage Parameters")
        v_in_min = st.number_input(f"Min Input Voltage (V) [Range: {ranges['input_voltage'][0]}-{ranges['input_voltage'][1]}V]", 
                                  value=float(auto_fix.get('buck_v_in_min', 20.0)), min_value=0.1, step=0.1, key="buck_v_in_min")
        v_in_max = st.number_input(f"Max Input Voltage (V) [Range: {ranges['input_voltage'][0]}-{ranges['input_voltage'][1]}V]", 
                                  value=float(auto_fix.get('buck_v_in_max', 25.0)), min_value=0.1, step=0.1, key="buck_v_in_max")
        v_out_min = st.number_input(f"Min Output Voltage (V) [Range: {ranges['output_voltage'][0]}-{ranges['output_voltage'][1]}V]", 
                                   value=float(auto_fix.get('buck_v_out_min', 11.4)), min_value=0.1, step=0.1, key="buck_v_out_min")
        v_out_max = st.number_input(f"Max Output Voltage (V) [Range: {ranges['output_voltage'][0]}-{ranges['output_voltage'][1]}V]", 
                                   value=float(auto_fix.get('buck_v_out_max', 12.6)), min_value=0.1, step=0.1, key="buck_v_out_max")
        v_ripple_max = st.number_input("Output Voltage Ripple (V)", 
                          value=float(auto_fix.get('buck_v_ripple_max', 0.1)), min_value=0.001, step=0.01, key="buck_v_ripple_max")
        v_in_ripple = st.number_input("Input Voltage Ripple (V)", 
                         value=float(auto_fix.get('buck_v_in_ripple', 0.3)), min_value=0.001, step=0.01, key="buck_v_in_ripple")
    
    with col2:
        st.subheader("⚙️ Power & Current")
        p_out_max = st.number_input(f"Max Output Power (W) [Range: {ranges['power'][0]}-{ranges['power'][1]}W]", 
                                   value=float(auto_fix.get('buck_p_out_max', 12.0)), min_value=0.1, step=1.0, key="buck_p_out_max")
        efficiency = st.number_input("Efficiency (0-1)", 
                        value=float(auto_fix.get('buck_efficiency', 0.90)), min_value=0.01, max_value=1.0, step=0.01, key="buck_efficiency")
        i_out_ripple = st.number_input("Inductor Current Ripple (A)", 
                          value=float(auto_fix.get('buck_i_out_ripple', 1.0)), min_value=0.01, step=0.1, key="buck_i_out_ripple")
    
    with col3:
        st.subheader("📊 Transient Parameters")
        switching_freq = st.number_input(f"Switching Frequency (Hz) [Range: {ranges['frequency'][0]/1000:.0f}k-{ranges['frequency'][1]/1000:.0f}kHz]", 
                        value=float(auto_fix.get('buck_switching_freq', 300000.0)), min_value=1.0, step=10000.0, key="buck_switching_freq", format="%f")
        v_overshoot = st.number_input("Voltage Overshoot (V)", 
                         value=float(auto_fix.get('buck_v_overshoot', 0.1)), min_value=0.001, step=0.01, key="buck_v_overshoot")
        v_undershoot = st.number_input("Voltage Undershoot (V)", 
                          value=float(auto_fix.get('buck_v_undershoot', 0.1)), min_value=0.001, step=0.01, key="buck_v_undershoot")
        i_loadstep = st.number_input("Load Step (A)", 
                        value=float(auto_fix.get('buck_i_loadstep', 1.0)), min_value=0.01, step=0.1, key="buck_i_loadstep")
    
    # Parameter guidance
    st.info("💡 **Component Availability Tips:**\n"
           "• Use **10-50V** input voltages for best component selection\n"
           "• Keep **output power 10-100W** for standard components\n"
           "• Try **100kHz-1MHz** switching frequency\n"
           "• **Lower ripple** requirements = more component options")
    
    # Input validation with helpful messages
    validation_errors = []
    
    if v_in_min >= v_in_max:
        validation_errors.append(f"⚠️ Min input voltage ({v_in_min}V) must be less than max ({v_in_max}V)")
    if v_out_min >= v_out_max:
        validation_errors.append(f"⚠️ Min output voltage ({v_out_min}V) must be less than max ({v_out_max}V)")
    if v_out_max >= v_in_min:
        validation_errors.append(f"⚠️ Output voltage ({v_out_max}V) must be less than input voltage ({v_in_min}V) for Buck converter")
    # Calculate required current to check against inductor limits
    required_current = p_out_max / v_out_max if v_out_max > 0 else 0
    max_available_current = 4.5  # From inductor database
    max_recommended_power = max_available_current * v_out_max
    
    if p_out_max < 1 or required_current > max_available_current:
        validation_errors.append(f"⚠️ Output power ({p_out_max}W) requires {required_current:.1f}A, but max available inductor current is {max_available_current}A. Try max {max_recommended_power:.1f}W")
    if switching_freq < 10000 or switching_freq > 2000000:
        validation_errors.append(f"⚠️ Switching frequency ({switching_freq/1000:.0f}kHz) should be between 10kHz and 2MHz")
    
    # Display validation errors
    if validation_errors:
        st.error("**Input Validation Errors:**")
        for error in validation_errors:
            st.write(error)
        st.info("💡 **Quick Fix: Click a guaranteed example above, or adjust your parameters**")
        
        # Provide quick fix suggestions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔧 Auto-Fix to Working Values", type="secondary"):
                # Clear all widget states to allow modification
                keys_to_clear = [
                    'buck_v_in_min', 'buck_v_in_max', 'buck_v_out_min', 'buck_v_out_max',
                    'buck_p_out_max', 'buck_efficiency', 'buck_switching_freq',
                    'buck_v_ripple_max', 'buck_v_in_ripple', 'buck_i_out_ripple',
                    'buck_v_overshoot', 'buck_v_undershoot', 'buck_i_loadstep'
                ]
                
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                
                # Set working values in session state (before widget creation)
                # Ensure all values are proper floats to match widget types
                st.session_state['auto_fix_applied'] = {
                    'buck_v_in_min': float(20.0),
                    'buck_v_in_max': float(25.0),
                    'buck_v_out_min': float(11.4),
                    'buck_v_out_max': float(12.6),
                    'buck_p_out_max': float(12.0),
                    'buck_efficiency': float(0.90),
                    'buck_switching_freq': float(300000.0),
                    'buck_v_ripple_max': float(0.1),
                    'buck_v_in_ripple': float(0.3),
                    'buck_i_out_ripple': float(1.0),
                    'buck_v_overshoot': float(0.1),
                    'buck_v_undershoot': float(0.1),
                    'buck_i_loadstep': float(1.0)
                }
                
                st.success("✅ Fixed! The page will reload with working values.")
                st.rerun()
    
    # Calculate button
    st.markdown("---")
    if st.button("🔬 Calculate Component Values", use_container_width=True, type="primary"):
        # Create inputs object
        inputs_dict = {
            'v_in_min': v_in_min,
            'v_in_max': v_in_max,
            'v_out_min': v_out_min,
            'v_out_max': v_out_max,
            'p_out_max': p_out_max,
            'efficiency': efficiency,
            'switching_freq': switching_freq,
            'v_ripple_max': v_ripple_max,
            'v_in_ripple': v_in_ripple,
            'i_out_ripple': i_out_ripple,
            'v_overshoot': v_overshoot,
            'v_undershoot': v_undershoot,
            'i_loadstep': i_loadstep,
        }
        
        if not validate_inputs(inputs_dict):
            st.error("❌ All values must be positive")
            return
        
        inputs = BuckInputs(**inputs_dict)
        
        # Calculate
        calculator = CircuitCalculator()
        results = calculator.calculate_buck(inputs)
        
        # Store in session state
        st.session_state.buck_results = results
        st.session_state.buck_inputs = inputs
        st.success("✅ Calculation complete!")
    
    # Display results if available
    if 'buck_results' in st.session_state:
        results = st.session_state.buck_results
        inputs = st.session_state.buck_inputs
        
        st.markdown("---")
        st.subheader("📊 Calculated Values")
        
        # Display results in metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Inductance",
                value=f"{results.inductance * 1e6:.2f} µH"
            )
        
        with col2:
            st.metric(
                label="Output Capacitance",
                value=f"{results.output_capacitance * 1e6:.2f} µF"
            )
        
        with col3:
            st.metric(
                label="Input Capacitance",
                value=f"{results.input_capacitance * 1e6:.2f} µF"
            )
        
        with col4:
            st.metric(
                label="Max Duty Cycle",
                value=f"{results.duty_cycle_max * 100:.1f}%"
            )
        
        # Component suggestions
        st.markdown("---")
        st.subheader("🎯 Recommended Components")
        
        # Calculate current
        max_current = inputs.p_out_max / inputs.v_out_min
        
        # Check component source preference
        use_web_search = st.session_state.get('component_source', 'local') == 'web'
        
        # Get suggestions with enhanced heuristics
        mosfet_suggestions = suggest_mosfets(
            max_voltage=inputs.v_in_max, 
            max_current=max_current,
            frequency_hz=switching_freq,
            use_web_search=use_web_search
        )
        output_cap_suggestions = suggest_capacitors(
            required_capacitance_uf=results.output_capacitance * 1e6, 
            max_voltage=inputs.v_out_max,
            frequency_hz=switching_freq,
            use_web_search=use_web_search
        )
        inductor_suggestions = suggest_inductors(
            required_inductance_uh=results.inductance * 1e6, 
            max_current=max_current,
            frequency_hz=switching_freq,
            use_web_search=use_web_search
        )
        
        # Get input capacitor suggestions
        # Estimate input ripple current (typical formula for Buck converter)
        input_ripple_current = max_current * (results.duty_cycle_max * (1 - results.duty_cycle_max)) ** 0.5
        input_cap_suggestions = suggest_input_capacitors(
            required_capacitance_uf=results.input_capacitance * 1e6,
            max_voltage=inputs.v_in_max,
            ripple_current_a=input_ripple_current,
            frequency_hz=switching_freq,
            use_web_search=use_web_search
        )
        
        # Enhanced debug information for inductor selection
        st.info(f"🔍 **Inductor Debug:** Required: {results.inductance * 1e6:.1f}µH, Max current: {max_current:.2f}A, "
               f"Switching freq: {switching_freq/1000:.0f}kHz, Found: {len(inductor_suggestions) if inductor_suggestions else 0} inductor(s)")

        # Compute available ranges dynamically based on selected source
        try:
            # Use web-derived suggestions if in web mode, otherwise use local DB
            L_min, L_max, I_min, I_max, inductor_ok = compute_available_inductor_ranges(
                required_inductance_uh=results.inductance * 1e6,
                max_current=max_current,
                inductor_suggestions=inductor_suggestions,
                use_web_search=use_web_search
            )

            if L_min == 0 and L_max == 0 and I_min == 0 and I_max == 0:
                st.info("📊 **Available Inductors:** range data unavailable from component database.")
            else:
                st.info(f"📊 **Available Inductors:** {L_min:.0f}µH-{L_max:.0f}µH, Current: {I_min:.2f}A-{I_max:.2f}A. "
                       f"Your requirements {'✅ match' if inductor_ok else '❌ exceed'} available range.")
        except Exception:
            st.info("📊 **Available Inductors:** range data unavailable from component database.")
        
        # Use new standardized display system
        from lib.component_display import display_component_table, filter_suggestions_by_source
        
        # Filter suggestions based on search mode
        use_web_search = st.session_state.get('component_source', 'local') == 'web'
        
        # Display in tabs with new standardized format
        tab1, tab2, tab3, tab4 = st.tabs(["💻 MOSFETs", "📥 Input Capacitors", "📤 Output Capacitors", "🧲 Inductors"])
        
        with tab1:
            # Filter MOSFETs based on search mode
            filtered_mosfets = filter_suggestions_by_source(mosfet_suggestions, use_web_search) if use_web_search else mosfet_suggestions
            display_component_table(filtered_mosfets, 'mosfet', '💻 MOSFETs')
        
        with tab2:
            # Show analysis info
            st.info(f"🔍 **Input Capacitor Analysis:** Required: {results.input_capacitance * 1e6:.1f}µF, "
                   f"Max voltage: {inputs.v_in_max}V, Ripple current: {input_ripple_current:.2f}A")
            
            # Filter and display input capacitors
            filtered_input_caps = filter_suggestions_by_source(input_cap_suggestions, use_web_search) if use_web_search else input_cap_suggestions
            display_component_table(filtered_input_caps, 'input_capacitor', '📥 Input Capacitors')
        
        with tab3:
            # Filter and display output capacitors
            filtered_output_caps = filter_suggestions_by_source(output_cap_suggestions, use_web_search) if use_web_search else output_cap_suggestions
            display_component_table(filtered_output_caps, 'capacitor', '📤 Output Capacitors')
        
        with tab4:
            # Filter and display inductors
            filtered_inductors = filter_suggestions_by_source(inductor_suggestions, use_web_search) if use_web_search else inductor_suggestions
            display_component_table(filtered_inductors, 'inductor', '🧲 Inductors')

        # 🔬 SIMULATION SECTION
        # Add simulation functionality after component recommendations
        if 'buck_results' in st.session_state and 'buck_inputs' in st.session_state:
            from lib.simulation_service import show_simulation_button, run_and_display_simulation, validate_simulation_inputs
            
            results = st.session_state.buck_results
            inputs = st.session_state.buck_inputs
            
            # Validate component availability
            components_available = check_component_availability(
                mosfet_suggestions, input_cap_suggestions, output_cap_suggestions, inductor_suggestions
            )
            
            if not components_available:
                st.markdown("---")
                st.warning("⚠️ **Simulation Unavailable**: No suitable components found for this design.")
                st.info("💡 **Suggestions:**")
                st.write("• Try adjusting input voltage range")
                st.write("• Reduce output power requirements") 
                st.write("• Change switching frequency")
                st.write("• Relax ripple specifications")
            else:
                # Calculate average values for simulation
                v_in_avg = (inputs.v_in_min + inputs.v_in_max) / 2
                v_out_avg = (inputs.v_out_min + inputs.v_out_max) / 2
                i_out_calc = inputs.p_out_max / v_out_avg  # Calculate load current from power
                
                # Prepare circuit parameters for simulation
                circuit_params = {
                    'input_voltage': v_in_avg,
                    'output_voltage': v_out_avg,
                    'load_current': i_out_calc,
                    'switching_frequency': inputs.switching_freq,
                    'ripple_voltage': inputs.v_ripple_max,
                    'ripple_current': inputs.i_out_ripple
                }
                
                # Prepare calculated components (convert to appropriate units)
                calculated_components = {
                    'inductance': results.inductance * 1e6,  # Convert to µH
                    'output_capacitance': results.output_capacitance * 1e6,  # Convert to µF
                    'input_capacitance': results.input_capacitance * 1e6,  # Convert to µF
                    'duty_cycle': results.duty_cycle_max
                }
                
                # Validate simulation inputs
                validation_result = validate_simulation_inputs(circuit_params, calculated_components)
                
                if not validation_result['valid']:
                    st.error(f"❌ **Simulation Error**: {validation_result['error']}")
                    st.info("💡 Please check your input parameters and try again.")
                else:
                    # Show simulation button and handle simulation
                    if show_simulation_button(circuit_params, calculated_components):
                        # User clicked simulate - run the simulation
                        run_and_display_simulation(circuit_params, calculated_components)
