"""
PFC (Power Factor Correction) Calculator Page
"""

import streamlit as st
from lib.calculations import CircuitCalculator, PFCInputs, validate_inputs
from lib.component_suggestions import suggest_mosfets, suggest_capacitors, suggest_inductors

def show():
    """Display PFC calculator page"""
    
    st.header("⚡ PFC Circuit Designer")
    st.markdown("---")
    
    # Create three columns for input parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Voltage Parameters")
        v_in_min = st.number_input("Min Input Voltage (V)", value=100.0, min_value=0.1, step=10.0, key="pfc_v_in_min")
        v_in_max = st.number_input("Max Input Voltage (V)", value=240.0, min_value=0.1, step=10.0, key="pfc_v_in_max")
        v_out_min = st.number_input("Min Output Voltage (V)", value=380.0, min_value=0.1, step=10.0, key="pfc_v_out_min")
        v_out_max = st.number_input("Max Output Voltage (V)", value=400.0, min_value=0.1, step=10.0, key="pfc_v_out_max")
    
    with col2:
        st.subheader("Power Parameters")
        p_out_max = st.number_input("Max Output Power (W)", value=3000.0, min_value=0.1, step=100.0, key="pfc_p_out_max")
        efficiency = st.number_input("Efficiency (0-1)", value=0.98, min_value=0.01, max_value=1.0, step=0.01, key="pfc_efficiency")
        v_ripple_max = st.number_input("Max Output Voltage Ripple (V)", value=20.0, min_value=0.1, step=1.0, key="pfc_v_ripple_max")
    
    with col3:
        st.subheader("Frequency Parameters")
        switching_freq = st.number_input("Switching Frequency (Hz)", value=65000.0, min_value=1.0, step=1000.0, key="pfc_switching_freq", format="%f")
        line_freq_min = st.number_input("Min Line Frequency (Hz)", value=50.0, min_value=1.0, step=10.0, key="pfc_line_freq_min")
    
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
            'line_freq_min': line_freq_min,
            'v_ripple_max': v_ripple_max,
        }
        
        if not validate_inputs(inputs_dict):
            st.error("❌ All values must be positive")
            return
        
        inputs = PFCInputs(**inputs_dict)
        
        # Calculate
        calculator = CircuitCalculator()
        results = calculator.calculate_pfc(inputs)
        
        # Store in session state
        st.session_state.pfc_results = results
        st.session_state.pfc_inputs = inputs
        st.success("✅ Calculation complete!")
    
    # Display results if available
    if 'pfc_results' in st.session_state:
        results = st.session_state.pfc_results
        inputs = st.session_state.pfc_inputs
        
        st.markdown("---")
        st.subheader("📊 Calculated Values")
        
        # Display results in metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Inductance",
                value=f"{results.inductance * 1000:.2f} mH"
            )
        
        with col2:
            st.metric(
                label="Capacitance",
                value=f"{results.capacitance * 1e6:.2f} µF"
            )
        
        with col3:
            st.metric(
                label="Ripple Current",
                value=f"{results.ripple_current:.2f} A"
            )
        
        # Component suggestions
        st.markdown("---")
        st.subheader("🎯 Recommended Components")
        
        # Calculate current
        max_current = inputs.p_out_max / inputs.v_in_min
        
        # Get suggestions
        mosfet_suggestions = suggest_mosfets(inputs.v_out_max, max_current)
        capacitor_suggestions = suggest_capacitors(results.capacitance * 1e6, inputs.v_out_max)
        inductor_suggestions = suggest_inductors(results.inductance * 1e6, results.ripple_current)
        
        # Display in tabs
        tab1, tab2, tab3 = st.tabs(["💻 MOSFETs", "🔋 Capacitors", "🧲 Inductors"])
        
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
            else:
                st.warning("No suitable MOSFETs found for these specifications")
        
        with tab2:
            if capacitor_suggestions:
                for idx, suggestion in enumerate(capacitor_suggestions):
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
            else:
                st.warning("No suitable inductors found for these specifications")
