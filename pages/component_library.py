"""
Component Library Display
Now loads data from CSV files in assets folder
"""

import streamlit as st

# Completely disable pandas for this page to avoid pyarrow issues
pandas_available = False
st.info("📊 **Component Library** - Using optimized display mode (no pandas/pyarrow dependency)")

# Import component libraries
try:
    from lib.component_data import MOSFET_LIBRARY, CAPACITOR_LIBRARY, INPUT_CAPACITOR_LIBRARY, INDUCTOR_LIBRARY
    from lib.design_heuristics import show_design_documents_info, refresh_recommendations_with_heuristics
except ImportError as e:
    st.error(f"❌ Error loading component data: {e}")
    MOSFET_LIBRARY = []
    CAPACITOR_LIBRARY = []
    INPUT_CAPACITOR_LIBRARY = []
    INDUCTOR_LIBRARY = []
    show_design_documents_info = lambda: None
    refresh_recommendations_with_heuristics = lambda: None


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
            try:
                # Force reimport of component data
                import importlib
                import lib.component_data
                importlib.reload(lib.component_data)
                st.success("Component data reloaded from CSV files!")
                st.rerun()
            except Exception as e:
                st.error(f"Error reloading data: {e}")
    
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
    tab1, tab2, tab3, tab4 = st.tabs(["💻 MOSFETs", "⚡ Input Capacitors", "🔋 Output Capacitors", "🧲 Inductors"])
    
    with tab1:
        st.subheader("MOSFET Library")
        
        if not MOSFET_LIBRARY:
            st.warning("⚠️ No MOSFETs loaded. Check if mosfets.csv exists in assets/component_data/")
        else:
            st.info(f"📟 **{len(MOSFET_LIBRARY)} MOSFETs available**")
            
            # Create table headers
            cols = st.columns([2, 1.5, 1, 1, 1, 1, 1.2, 1.2, 2])
            headers = ["Name", "Manufacturer", "VDS (V)", "ID (A)", "RDS(on) (mΩ)", "Qg (nC)", "Package", "Efficiency", "Typical Use"]
            
            for i, header in enumerate(headers):
                with cols[i]:
                    st.write(f"**{header}**")
            
            st.markdown("---")
            
            # Display each MOSFET as a table row
            for mosfet in MOSFET_LIBRARY:
                cols = st.columns([2, 1.5, 1, 1, 1, 1, 1.2, 1.2, 2])
                
                with cols[0]:
                    st.write(mosfet.name)
                with cols[1]:
                    st.write(mosfet.manufacturer)
                with cols[2]:
                    st.write(f"{mosfet.vds}")
                with cols[3]:
                    st.write(f"{mosfet.id}")
                with cols[4]:
                    st.write(f"{mosfet.rdson}")
                with cols[5]:
                    st.write(f"{mosfet.qg if mosfet.qg > 0 else 'N/A'}")
                with cols[6]:
                    st.write(mosfet.package)
                with cols[7]:
                    st.write(mosfet.efficiency_range)
                with cols[8]:
                    st.write(mosfet.typical_use)

    
    with tab2:
        st.subheader("Input Capacitor Library")
        st.info("🎯 **Input capacitors handle ripple current and provide bulk energy storage at the converter input**")
        
        if not INPUT_CAPACITOR_LIBRARY:
            st.warning("⚠️ No input capacitors loaded. Check if input_capacitors.csv exists in assets/component_data/")
        else:
            st.info(f"⚡ **{len(INPUT_CAPACITOR_LIBRARY)} Input Capacitors available**")
            
            # Create table headers
            cols = st.columns([2, 1.5, 1.2, 1.2, 1, 1, 1, 1, 1.5, 1.2])
            headers = ["Part Number", "Manufacturer", "Category", "Dielectric", "Cap (µF)", "Voltage (V)", "ESR (mΩ)", "ESL (nH)", "Ripple (A)", "Package"]
            
            for i, header in enumerate(headers):
                with cols[i]:
                    st.write(f"**{header}**")
            
            st.markdown("---")
            
            # Display each input capacitor as a table row
            for cap in INPUT_CAPACITOR_LIBRARY:
                cols = st.columns([2, 1.5, 1.2, 1.2, 1, 1, 1, 1, 1.5, 1.2])
                
                with cols[0]:
                    st.write(cap.part_number)
                with cols[1]:
                    st.write(cap.manufacturer)
                with cols[2]:
                    st.write(cap.category)
                with cols[3]:
                    st.write(cap.dielectric)
                with cols[4]:
                    st.write(f"{cap.capacitance}")
                with cols[5]:
                    st.write(f"{cap.voltage}")
                with cols[6]:
                    st.write(f"{cap.esr}" if cap.esr > 0 else "N/A")
                with cols[7]:
                    st.write(f"{cap.esl}" if cap.esl > 0 else "N/A")
                with cols[8]:
                    st.write(f"{cap.ripple_rating}" if cap.ripple_rating > 0 else "N/A")
                with cols[9]:
                    st.write(cap.package)


    with tab3:
        st.subheader("Output Capacitor Library")
        st.info("🎯 **Output capacitors filter switching ripple and maintain stable output voltage**")
        
        if not CAPACITOR_LIBRARY:
            st.warning("⚠️ No output capacitors loaded. Check if output_capacitors.csv exists in assets/component_data/")
        else:
            st.info(f"🔋 **{len(CAPACITOR_LIBRARY)} Output Capacitors available**")
            
            # Create table headers
            cols = st.columns([2, 1.5, 1.5, 1, 1, 1, 1.5, 2])
            headers = ["Part Number", "Manufacturer", "Type", "Cap (µF)", "Voltage (V)", "ESR (mΩ)", "Temp Range", "Primary Use"]
            
            for i, header in enumerate(headers):
                with cols[i]:
                    st.write(f"**{header}**")
            
            st.markdown("---")
            
            # Display each output capacitor as a table row
            for cap in CAPACITOR_LIBRARY:
                cols = st.columns([2, 1.5, 1.5, 1, 1, 1, 1.5, 2])
                
                with cols[0]:
                    st.write(cap.part_number)
                with cols[1]:
                    st.write(cap.manufacturer)
                with cols[2]:
                    st.write(cap.type)
                with cols[3]:
                    st.write(f"{cap.capacitance}")
                with cols[4]:
                    st.write(f"{cap.voltage}")
                with cols[5]:
                    st.write(f"{cap.esr}")
                with cols[6]:
                    st.write(cap.temp_range)
                with cols[7]:
                    st.write(cap.primary_use)

    
    with tab4:
        st.subheader("Inductor Library")
        st.info("🎯 **Inductors store energy and control current ripple in switching converters**")
        
        if not INDUCTOR_LIBRARY:
            st.warning("⚠️ No inductors loaded. Check if inductors.csv exists in assets/component_data/")
        else:
            st.info(f"🧲 **{len(INDUCTOR_LIBRARY)} Inductors available**")
            
            # Create table headers
            cols = st.columns([2, 1.5, 1, 1, 1, 1, 1.2, 1, 1.5])
            headers = ["Part Number", "Manufacturer", "L (µH)", "I_rated (A)", "DCR (mΩ)", "I_sat (A)", "Package", "Shielded", "Core Material"]
            
            for i, header in enumerate(headers):
                with cols[i]:
                    st.write(f"**{header}**")
            
            st.markdown("---")
            
            # Display each inductor as a table row
            for ind in INDUCTOR_LIBRARY:
                cols = st.columns([2, 1.5, 1, 1, 1, 1, 1.2, 1, 1.5])
                
                with cols[0]:
                    st.write(ind.part_number)
                with cols[1]:
                    st.write(ind.manufacturer)
                with cols[2]:
                    st.write(f"{ind.inductance}")
                with cols[3]:
                    st.write(f"{ind.current}")
                with cols[4]:
                    st.write(f"{ind.dcr}")
                with cols[5]:
                    st.write(f"{ind.sat_current}")
                with cols[6]:
                    st.write(ind.package)
                with cols[7]:
                    st.write("Yes" if hasattr(ind, 'shielded') and ind.shielded else "No")
                with cols[8]:
                    st.write(getattr(ind, 'core_material', 'N/A'))

