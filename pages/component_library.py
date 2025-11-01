"""
Component Library Display
"""

import streamlit as st
import pandas as pd
from lib.component_data import MOSFET_LIBRARY, CAPACITOR_LIBRARY, INDUCTOR_LIBRARY

def show_sidebar_library():
    """Show component library in sidebar"""
    
    library_type = st.selectbox(
        "Component Type",
        ["MOSFETs", "Capacitors", "Inductors"]
    )
    
    if library_type == "MOSFETs":
        st.markdown("### MOSFETs")
        for mosfet in MOSFET_LIBRARY[:5]:  # Show first 5
            with st.expander(f"{mosfet.name}"):
                st.markdown(f"**Manufacturer:** {mosfet.manufacturer}")
                st.markdown(f"**VDS:** {mosfet.vds}V | **ID:** {mosfet.id}A")
                st.markdown(f"**RDS(on):** {mosfet.rdson}mΩ")
    
    elif library_type == "Capacitors":
        st.markdown("### Capacitors")
        for cap in CAPACITOR_LIBRARY[:5]:  # Show first 5
            with st.expander(f"{cap.part_number}"):
                st.markdown(f"**Manufacturer:** {cap.manufacturer}")
                st.markdown(f"**Cap:** {cap.capacitance}µF | **V:** {cap.voltage}V")
                st.markdown(f"**Type:** {cap.type}")
    
    elif library_type == "Inductors":
        st.markdown("### Inductors")
        for ind in INDUCTOR_LIBRARY:
            with st.expander(f"{ind.part_number}"):
                st.markdown(f"**Manufacturer:** {ind.manufacturer}")
                st.markdown(f"**L:** {ind.inductance}µH | **I:** {ind.current}A")
                st.markdown(f"**Package:** {ind.package}")


def show():
    """Display full component library page"""
    
    st.header("📚 Component Library")
    st.markdown("Browse available MOSFETs, capacitors, and inductors for your circuit designs")
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
                "Qg (nC)": mosfet.qg if mosfet.qg > 0 else "N/A",
                "Package": mosfet.package,
                "Efficiency": mosfet.efficiency_range,
                "Typical Use": mosfet.typical_use
            })
        
        df_mosfet = pd.DataFrame(mosfet_data)
        st.dataframe(df_mosfet, use_container_width=True)
        
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
        st.dataframe(df_cap, use_container_width=True)
        
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
        st.dataframe(df_ind, use_container_width=True)
        
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
