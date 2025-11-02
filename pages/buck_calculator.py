"""
Buck Converter Calculator Page
"""

import streamlit as st
from lib.calculations import CircuitCalculator, BuckInputs, validate_inputs
from lib.component_suggestions import suggest_mosfets, suggest_capacitors, suggest_inductors

def show():
    """Display Buck converter calculator page"""
    
    st.header("🔋 Buck Converter Designer")
    st.markdown("---")
    
    # Create three columns for input parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("⚡ Voltage Parameters")
        v_in_min = st.number_input("Min Input Voltage (V)", value=12.0, min_value=0.1, step=1.0, key="buck_v_in_min")
        v_in_max = st.number_input("Max Input Voltage (V)", value=24.0, min_value=0.1, step=1.0, key="buck_v_in_max")
        v_out_min = st.number_input("Min Output Voltage (V)", value=3.3, min_value=0.1, step=0.1, key="buck_v_out_min")
        v_out_max = st.number_input("Max Output Voltage (V)", value=5.0, min_value=0.1, step=0.1, key="buck_v_out_max")
        v_ripple_max = st.number_input("Output Voltage Ripple (V)", value=0.05, min_value=0.001, step=0.01, key="buck_v_ripple_max")
        v_in_ripple = st.number_input("Input Voltage Ripple (V)", value=0.1, min_value=0.001, step=0.01, key="buck_v_in_ripple")
    
    with col2:
        st.subheader("⚙️ Power & Current")
        p_out_max = st.number_input("Max Output Power (W)", value=50.0, min_value=0.1, step=5.0, key="buck_p_out_max")
        efficiency = st.number_input("Efficiency (0-1)", value=0.95, min_value=0.01, max_value=1.0, step=0.01, key="buck_efficiency")
        i_out_ripple = st.number_input("Inductor Current Ripple (A)", value=0.5, min_value=0.01, step=0.1, key="buck_i_out_ripple")
    
    with col3:
        st.subheader("📊 Transient Parameters")
        switching_freq = st.number_input("Switching Frequency (Hz)", value=500000.0, min_value=1.0, step=10000.0, key="buck_switching_freq", format="%f")
        v_overshoot = st.number_input("Voltage Overshoot (V)", value=0.1, min_value=0.001, step=0.01, key="buck_v_overshoot")
        v_undershoot = st.number_input("Voltage Undershoot (V)", value=0.1, min_value=0.001, step=0.01, key="buck_v_undershoot")
        i_loadstep = st.number_input("Load Step (A)", value=1.0, min_value=0.01, step=0.1, key="buck_i_loadstep")
    
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
        
        # Get suggestions with enhanced heuristics
        mosfet_suggestions = suggest_mosfets(
            max_voltage=inputs.v_in_max, 
            max_current=max_current,
            frequency_hz=switching_freq
        )
        output_cap_suggestions = suggest_capacitors(
            required_capacitance_uf=results.output_capacitance * 1e6, 
            max_voltage=inputs.v_out_max,
            frequency_hz=switching_freq
        )
        inductor_suggestions = suggest_inductors(
            required_inductance_uh=results.inductance * 1e6, 
            max_current=max_current,
            frequency_hz=switching_freq
        )
        
        # Display in tabs
        tab1, tab2, tab3 = st.tabs(["💻 MOSFETs", "🔋 Output Capacitors", "🧲 Inductors"])
        
        with tab1:
            if mosfet_suggestions:
                for idx, suggestion in enumerate(mosfet_suggestions):
                    mosfet = suggestion.component
                    with st.expander(f"#{idx+1} {mosfet.name} - {mosfet.manufacturer}", expanded=idx==0):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown(f"**VDS:** {mosfet.vds}V | **ID:** {mosfet.id}A | **RDS(on):** {mosfet.rdson}mΩ")
                            st.markdown(f"**Qg:** {mosfet.qg}nC | **Package:** {mosfet.package}")
                            st.markdown(f"**Typical Use:** {mosfet.typical_use}")
                        with col2:
                            st.info(mosfet.efficiency_range)
                        st.caption(f"💡 **Why:** {suggestion.reason}")
                        
                        # Show applied heuristics if available
                        if hasattr(suggestion, 'heuristics_applied') and suggestion.heuristics_applied:
                            st.markdown("**📋 Applied Design Heuristics:**")
                            for heuristic in suggestion.heuristics_applied[:3]:  # Show top 3
                                st.markdown(f"- {heuristic}")
            else:
                st.warning("No suitable MOSFETs found for these specifications")
        
        with tab2:
            if output_cap_suggestions:
                for idx, suggestion in enumerate(output_cap_suggestions):
                    cap = suggestion.component
                    with st.expander(f"#{idx+1} {cap.part_number} - {cap.manufacturer}", expanded=idx==0):
                        st.markdown(f"**Capacitance:** {cap.capacitance}µF | **Voltage:** {cap.voltage}V | **Type:** {cap.type}")
                        st.markdown(f"**ESR:** {cap.esr}mΩ | **Temp Range:** {cap.temp_range}°C")
                        st.markdown(f"**Primary Use:** {cap.primary_use}")
                        st.caption(f"💡 **Why:** {suggestion.reason}")
            else:
                st.warning("No suitable capacitors found for these specifications")
        
        with tab3:
            if inductor_suggestions:
                for idx, suggestion in enumerate(inductor_suggestions):
                    ind = suggestion.component
                    with st.expander(f"#{idx+1} {ind.part_number} - {ind.manufacturer}", expanded=idx==0):
                        st.markdown(f"**Inductance:** {ind.inductance}µH | **Current:** {ind.current}A")
                        st.markdown(f"**DCR:** {ind.dcr}mΩ | **Isat:** {ind.sat_current}A | **Package:** {ind.package}")
                        st.caption(f"💡 **Why:** {suggestion.reason}")
                        
                        # Show applied heuristics if available
                        if hasattr(suggestion, 'heuristics_applied') and suggestion.heuristics_applied:
                            st.markdown("**📋 Applied Design Heuristics:**")
                            for heuristic in suggestion.heuristics_applied[:3]:  # Show top 3
                                st.markdown(f"- {heuristic}")
            else:
                st.warning("No suitable inductors found for these specifications")
