"""
Component Library Display
Now loads data from CSV files in assets folder
"""

import streamlit as st
import pandas as pd
from lib.component_data import MOSFET_LIBRARY, CAPACITOR_LIBRARY, INDUCTOR_LIBRARY, reload_component_data
from lib.design_heuristics import show_design_documents_info, refresh_recommendations_with_heuristics


def show():
    """Display full component library page"""
    
    # Back button and reload functionality
    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
    with col1:
        if st.button("← Back"):
            st.session_state.page = None
            st.rerun()
    
    with col3:
        if st.button("🔄 Reload Data", help="Reload component data from CSV files"):
            reload_component_data()
            st.success("Component data reloaded from CSV files!")
            st.rerun()
    
    with col4:
        if st.button("📋 Design Docs", help="View design heuristics documents"):
            st.session_state.show_design_docs = not st.session_state.get('show_design_docs', False)
    
    st.header("📚 Component Library")
    st.markdown("Browse available MOSFETs, capacitors, and inductors for your circuit designs")
    st.markdown("*Data is loaded from CSV files in the `assets/component_data/` folder*")
    
    # Show design documents section if requested
    if st.session_state.get('show_design_docs', False):
        st.markdown("---")
        show_design_documents_info()
        
        if st.button("🔄 Refresh Recommendations with Latest Heuristics"):
            refresh_recommendations_with_heuristics()
    
    st.markdown("---")
    
    # Tabs for different component types
    tab1, tab2, tab3 = st.tabs(["💻 MOSFETs", "🔋 Capacitors", "🧲 Inductors"])
    
    with tab1:
        st.subheader("MOSFET Library")
        
        # Convert to DataFrame for better display
        mosfet_data = []
        for mosfet in MOSFET_LIBRARY:
            mosfet_data.append({
                "Name": mosfet.name,
                "Manufacturer": mosfet.manufacturer,
                "VDS (V)": mosfet.vds,
                "ID (A)": mosfet.id,
                "RDS(on) (mΩ)": mosfet.rdson,
                "Qg (nC)": mosfet.qg if mosfet.qg > 0 else 0,  # Use 0 instead of "N/A"
                "Package": mosfet.package,
                "Efficiency": mosfet.efficiency_range,
                "Typical Use": mosfet.typical_use
            })
        
        df_mosfet = pd.DataFrame(mosfet_data)
        st.dataframe(df_mosfet, width="stretch")
        
        # Detailed view
        st.markdown("---")
        st.subheader("Detailed Information")
        selected_mosfet = st.selectbox("Select MOSFET for details", [m.name for m in MOSFET_LIBRARY])
        
        for mosfet in MOSFET_LIBRARY:
            if mosfet.name == selected_mosfet:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Name:** {mosfet.name}")
                    st.markdown(f"**Manufacturer:** {mosfet.manufacturer}")
                    st.markdown(f"**VDS:** {mosfet.vds}V")
                    st.markdown(f"**ID:** {mosfet.id}A")
                    st.markdown(f"**RDS(on):** {mosfet.rdson}mΩ")
                with col2:
                    st.markdown(f"**Qg:** {mosfet.qg if mosfet.qg > 0 else 'N/A'} nC")
                    st.markdown(f"**Package:** {mosfet.package}")
                    st.markdown(f"**Efficiency Range:** {mosfet.efficiency_range}")
                    st.markdown(f"**Typical Use:** {mosfet.typical_use}")
                break
    
    with tab2:
        st.subheader("Capacitor Library")
        
        # Convert to DataFrame
        cap_data = []
        for cap in CAPACITOR_LIBRARY:
            cap_data.append({
                "Part Number": cap.part_number,
                "Manufacturer": cap.manufacturer,
                "Capacitance (µF)": cap.capacitance,
                "Voltage (V)": cap.voltage,
                "Type": cap.type,
                "ESR (mΩ)": cap.esr,
                "Temp Range (°C)": cap.temp_range,
                "Primary Use": cap.primary_use
            })
        
        df_cap = pd.DataFrame(cap_data)
        st.dataframe(df_cap, width="stretch")
        
        # Detailed view
        st.markdown("---")
        st.subheader("Detailed Information")
        selected_cap = st.selectbox("Select Capacitor for details", [c.part_number for c in CAPACITOR_LIBRARY])
        
        for cap in CAPACITOR_LIBRARY:
            if cap.part_number == selected_cap:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Part Number:** {cap.part_number}")
                    st.markdown(f"**Manufacturer:** {cap.manufacturer}")
                    st.markdown(f"**Capacitance:** {cap.capacitance}µF")
                    st.markdown(f"**Voltage:** {cap.voltage}V")
                with col2:
                    st.markdown(f"**Type:** {cap.type}")
                    st.markdown(f"**ESR:** {cap.esr}mΩ")
                    st.markdown(f"**Temp Range:** {cap.temp_range}°C")
                    st.markdown(f"**Primary Use:** {cap.primary_use}")
                break
    
    with tab3:
        st.subheader("Inductor Library")
        
        # Convert to DataFrame
        ind_data = []
        for ind in INDUCTOR_LIBRARY:
            ind_data.append({
                "Part Number": ind.part_number,
                "Manufacturer": ind.manufacturer,
                "Inductance (µH)": ind.inductance,
                "Current (A)": ind.current,
                "DCR (mΩ)": ind.dcr,
                "Isat (A)": ind.sat_current,
                "Package": ind.package
            })
        
        df_ind = pd.DataFrame(ind_data)
        st.dataframe(df_ind, width="stretch")
        
        # Detailed view
        st.markdown("---")
        st.subheader("Detailed Information")
        selected_ind = st.selectbox("Select Inductor for details", [i.part_number for i in INDUCTOR_LIBRARY])
        
        for ind in INDUCTOR_LIBRARY:
            if ind.part_number == selected_ind:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Part Number:** {ind.part_number}")
                    st.markdown(f"**Manufacturer:** {ind.manufacturer}")
                    st.markdown(f"**Inductance:** {ind.inductance}µH")
                    st.markdown(f"**Current Rating:** {ind.current}A")
                with col2:
                    st.markdown(f"**DCR:** {ind.dcr}mΩ")
                    st.markdown(f"**Saturation Current:** {ind.sat_current}A")
                    st.markdown(f"**Package:** {ind.package}")
                break
