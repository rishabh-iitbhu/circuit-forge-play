"""
Component Display Utilities
Standardized tabular display for all component types
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from lib.component_suggestions import ComponentSuggestion

def create_component_table(suggestions: List[ComponentSuggestion], component_type: str) -> pd.DataFrame:
    """
    Create a streamlined DataFrame for component selection
    
    Args:
        suggestions: List of ComponentSuggestion objects
        component_type: Type of component ('mosfet', 'capacitor', 'inductor', 'input_capacitor')
    
    Returns:
        DataFrame with essential columns only - click for details
    """
    if not suggestions:
        return pd.DataFrame()
    
    data = []
    
    for i, suggestion in enumerate(suggestions):
        comp = suggestion.component
        
        # Essential information only - streamlined table
        row = {
            'Select': f"🔘 #{i + 1}",  # Click indicator
            'Part Number': getattr(comp, 'part_number', getattr(comp, 'name', 'N/A')),
            'Manufacturer': getattr(comp, 'manufacturer', 'N/A'),
            'Source': getattr(comp, 'distributor', 'Local Database'),
        }
        
        # Add only the most critical specs for quick comparison
        if component_type == 'mosfet':
            row.update({
                'VDS (V)': getattr(comp, 'vds', 'N/A'),
                'ID (A)': getattr(comp, 'id', 'N/A'), 
                'RDS(on) (mΩ)': getattr(comp, 'rdson', 'N/A'),
            })
            
        elif component_type in ['capacitor', 'output_capacitor']:
            row.update({
                'Capacitance (µF)': getattr(comp, 'capacitance', 'N/A'),
                'Voltage (V)': getattr(comp, 'voltage', 'N/A'),
                'ESR': getattr(comp, 'esr', 'N/A'),
            })
            
        elif component_type == 'input_capacitor':
            row.update({
                'Capacitance (µF)': getattr(comp, 'capacitance', 'N/A'),
                'Voltage (V)': getattr(comp, 'voltage', 'N/A'),
                'ESR (mΩ)': getattr(comp, 'esr', 'N/A'),
            })
            
        elif component_type == 'inductor':
            row.update({
                'Inductance (µH)': getattr(comp, 'inductance', 'N/A'),
                'Current (A)': getattr(comp, 'current', 'N/A'),
                'DCR (mΩ)': getattr(comp, 'dcr', 'N/A'),
            })
        
        # Add price and availability
        row.update({
            'Price': getattr(comp, 'price', 'See distributor'),
            'Stock': getattr(comp, 'availability', 'Check stock'),
            'Why?': f"🤔 #{i + 1}",  # Clickable reasoning column
        })
        
        data.append(row)
    
    return pd.DataFrame(data)

def create_component_links(part_number: str, manufacturer: str, distributor: str = None) -> Dict[str, str]:
    """
    Generate working links for component and datasheet
    
    Args:
        part_number: Component part number
        manufacturer: Component manufacturer
        distributor: Distributor name (if web search result)
    
    Returns:
        Dictionary with component and datasheet links
    """
    links = {}
    
    # Clean part number for URL
    clean_part = part_number.replace(' ', '+').replace('/', '%2F')
    clean_mfg = manufacturer.replace(' ', '+')
    
    # Component purchase links
    if distributor and 'Mouser' in distributor:
        links['component'] = f"https://www.mouser.com/c/?q={clean_part}"
        links['datasheet'] = f"https://www.mouser.com/c/?q={clean_part}"
    elif distributor and 'Digikey' in distributor:
        links['component'] = f"https://www.digikey.com/en/products/result?s={clean_part}"
        links['datasheet'] = f"https://www.digikey.com/en/products/result?s={clean_part}"
    else:
        # Generic search links for local database components
        links['component'] = f"https://www.mouser.com/c/?q={clean_part}+{clean_mfg}"
        links['datasheet'] = f"https://www.google.com/search?q={clean_part}+{clean_mfg}+datasheet+filetype:pdf"
    
    return links

def display_component_table(suggestions: List[ComponentSuggestion], component_type: str, title: str):
    """
    Display components in an interactive table - click to see details
    
    Args:
        suggestions: List of ComponentSuggestion objects
        component_type: Type of component
        title: Display title for the section
    """
    if not suggestions:
        st.warning(f"No suitable {title.lower()} found for these specifications")
        return
    
    st.subheader(title)
    
    # Store suggestions in session state with a unique key for this component type
    session_key = f"{component_type}_suggestions"
    st.session_state[session_key] = suggestions
    
    # Debug information
    if st.checkbox(f"Debug {component_type}", key=f"debug_{component_type}"):
        st.write(f"**Debug Info for {component_type}:**")
        st.write(f"- Original suggestions count: {len(suggestions)}")
        st.write(f"- Session key: {session_key}")
        st.write(f"- Session state has key: {session_key in st.session_state}")
        if suggestions:
            sample_comp = suggestions[0].component
            st.write(f"- Sample component attributes: {[attr for attr in dir(sample_comp) if not attr.startswith('_')]}")
            st.write(f"- Sample distributor: {getattr(sample_comp, 'distributor', 'None')}")
    
    # Display component count and source summary
    web_count = len([s for s in suggestions if hasattr(s.component, 'distributor') and getattr(s.component, 'distributor', '') in ['Mouser', 'Digikey']])
    local_count = len(suggestions) - web_count
    
    if web_count > 0 and local_count > 0:
        st.info(f"📊 Found **{len(suggestions)}** components: {web_count} from web search, {local_count} from local database")
    elif web_count > 0:
        st.success(f"🌐 Found **{web_count}** components from web search")
    else:
        st.info(f"📚 Found **{local_count}** components from local database")
    
    # Create streamlined table
    df = create_component_table(suggestions, component_type)
    
    if df.empty:
        st.warning(f"No {title.lower()} data available")
        return
    
    # Configure columns for better display
    column_config = {
        'Select': st.column_config.TextColumn(
            "Select", help="Click row to see details", width="small"
        ),
        'Part Number': st.column_config.TextColumn(
            "Part Number", help="Manufacturer part number", width="medium"
        ),
        'Manufacturer': st.column_config.TextColumn(
            "Manufacturer", help="Component manufacturer", width="medium"
        ),
        'Source': st.column_config.TextColumn(
            "Source", help="Data source", width="medium"
        ),
        'Price': st.column_config.TextColumn(
            "Price", help="Component price", width="medium"
        ),
        'Stock': st.column_config.TextColumn(
            "Stock", help="Availability status", width="medium"
        ),
        'Why?': st.column_config.TextColumn(
            "Why?", help="Click to see detailed reasoning", width="small"
        ),
    }
    
    # Display the interactive table
    selected_data = st.dataframe(
        df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key=f"{component_type}_table"
    )
    
    # Handle "Why?" column clicks - check if user clicked on the "Why?" column
    why_clicked_key = f"{component_type}_why_clicked"
    if why_clicked_key not in st.session_state:
        st.session_state[why_clicked_key] = None
    
    # Check for "Why?" column clicks by examining the dataframe selection
    if selected_data and 'selection' in selected_data and selected_data['selection']['rows']:
        selected_idx = selected_data['selection']['rows'][0]
        
        # Get the selected row data to check if "Why?" column was clicked
        if selected_idx < len(df):
            selected_row = df.iloc[selected_idx]
            why_value = selected_row.get('Why?', '')
            
            # If "Why?" column was clicked (contains the pattern), show reasoning
            if '🤔' in str(why_value):
                st.session_state[why_clicked_key] = selected_idx
            else:
                st.session_state[why_clicked_key] = None
    
    # Show detailed reasoning section if "Why?" was clicked
    if st.session_state.get(why_clicked_key) is not None:
        clicked_idx = st.session_state[why_clicked_key]
        
        if clicked_idx < len(suggestions):
            clicked_suggestion = suggestions[clicked_idx]
            
            st.write("---")
            st.subheader(f"🧠 Why #{clicked_idx + 1} is a Top Suggestion")
            
            # Create two columns for reasoning display
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Show the component's basic reasoning
                st.info(f"**{getattr(clicked_suggestion.component, 'part_number', getattr(clicked_suggestion.component, 'name', f'Component {clicked_idx+1}'))}** - {clicked_suggestion.reason}")
                
                # Show detailed rationale based on component type
                show_detailed_rationale(clicked_suggestion, component_type)
                
                # Show applied heuristics if available
                if clicked_suggestion.heuristics_applied:
                    st.write("**Applied Design Heuristics:**")
                    for heuristic in clicked_suggestion.heuristics_applied:
                        st.caption(f"✅ {heuristic}")
            
            with col2:
                st.write("**Quick Stats:**")
                comp = clicked_suggestion.component
                
                if component_type == 'mosfet':
                    st.metric("Score", f"{clicked_suggestion.score:.1f}")
                    st.metric("VDS", f"{getattr(comp, 'vds', 'N/A')}V")
                    st.metric("RDS(on)", f"{getattr(comp, 'rdson', 'N/A')}mΩ")
                elif component_type in ['capacitor', 'input_capacitor']:
                    st.metric("Score", f"{clicked_suggestion.score:.1f}")
                    st.metric("Capacitance", f"{getattr(comp, 'capacitance', 'N/A')}µF")
                    st.metric("Voltage", f"{getattr(comp, 'voltage', 'N/A')}V")
                elif component_type == 'inductor':
                    st.metric("Score", f"{clicked_suggestion.score:.1f}")
                    st.metric("Inductance", f"{getattr(comp, 'inductance', 'N/A')}µH")
                    st.metric("Current", f"{getattr(comp, 'current', 'N/A')}A")
                
                if st.button("Close Reasoning", key=f"close_why_{component_type}"):
                    st.session_state[why_clicked_key] = None
                    st.rerun()
    
    # Show details for selected component (original functionality)
    if selected_data and 'selection' in selected_data and selected_data['selection']['rows']:
        selected_idx = selected_data['selection']['rows'][0]
        
        # Only show component details if "Why?" wasn't clicked
        if st.session_state.get(why_clicked_key) != selected_idx:
            # Get suggestions from session state to ensure they persist across reruns
            stored_suggestions = st.session_state.get(session_key, suggestions)
            
            if selected_idx < len(stored_suggestions):
                selected_component = stored_suggestions[selected_idx]
                
                st.write("---")
            st.subheader(f"📋 Component Details - #{selected_idx + 1}")
            
            comp = selected_component.component
            part_number = getattr(comp, 'part_number', getattr(comp, 'name', f'Component_{selected_idx+1}'))
            manufacturer = getattr(comp, 'manufacturer', 'Unknown')
            distributor = getattr(comp, 'distributor', None)
            
            # Create two columns for details and links
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Part Number:** {part_number}")
                st.write(f"**Manufacturer:** {manufacturer}")
                
                # Technical specifications
                if component_type == 'mosfet':
                    st.write(f"**Drain-Source Voltage (VDS):** {getattr(comp, 'vds', 'N/A')} V")
                    st.write(f"**Drain Current (ID):** {getattr(comp, 'id', 'N/A')} A")
                    st.write(f"**On-Resistance (RDS(on)):** {getattr(comp, 'rdson', 'N/A')} mΩ")
                    st.write(f"**Package:** {getattr(comp, 'package', 'N/A')}")
                    if hasattr(comp, 'efficiency_range'):
                        st.write(f"**Expected Efficiency:** {comp.efficiency_range}")
                    
                    # NEW: Extended heuristics parameters display
                    if hasattr(comp, 'vgs_max'):
                        st.write(f"**Max Gate-Source Voltage (VGS):** ±{getattr(comp, 'vgs_max', 'N/A')} V")
                    if hasattr(comp, 'rdson_at_125c') and getattr(comp, 'rdson_at_125c', 0) > 0:
                        st.write(f"**RDS(on) @ 125°C:** {comp.rdson_at_125c} mΩ")
                    if hasattr(comp, 'mosfet_type'):
                        st.write(f"**MOSFET Type:** {getattr(comp, 'mosfet_type', 'Si')}")
                    if hasattr(comp, 'qgd') and getattr(comp, 'qgd', 0) > 0 and hasattr(comp, 'qgs') and getattr(comp, 'qgs', 0) > 0:
                        qgd_qgs_ratio = comp.qgd / comp.qgs if comp.qgs > 0 else 0
                        st.write(f"**Gate Charge Ratio (Qgd/Qgs):** {qgd_qgs_ratio:.2f}")
                    if hasattr(comp, 'package_inductance') and getattr(comp, 'package_inductance', 0) > 0:
                        st.write(f"**Package Inductance:** {comp.package_inductance} nH")
                
                elif component_type in ['capacitor', 'output_capacitor']:
                    st.write(f"**Capacitance:** {getattr(comp, 'capacitance', 'N/A')} µF")
                    st.write(f"**Rated Voltage:** {getattr(comp, 'voltage', 'N/A')} V")
                    st.write(f"**ESR:** {getattr(comp, 'esr', 'N/A')}")
                    if hasattr(comp, 'type'):
                        st.write(f"**Dielectric Type:** {comp.type}")
                    if hasattr(comp, 'temp_range'):
                        st.write(f"**Temperature Range:** {comp.temp_range}")
                
                elif component_type == 'input_capacitor':
                    st.write(f"**Capacitance:** {getattr(comp, 'capacitance', 'N/A')} µF")
                    st.write(f"**Rated Voltage:** {getattr(comp, 'voltage', 'N/A')} V")
                    st.write(f"**ESR:** {getattr(comp, 'esr', 'N/A')} mΩ")
                    if hasattr(comp, 'category'):
                        st.write(f"**Category:** {comp.category}")
                    if hasattr(comp, 'ripple_rating'):
                        st.write(f"**Ripple Current Rating:** {comp.ripple_rating} A")
                
                elif component_type == 'inductor':
                    st.write(f"**Inductance:** {getattr(comp, 'inductance', 'N/A')} µH")
                    st.write(f"**Current Rating:** {getattr(comp, 'current', 'N/A')} A")
                    st.write(f"**DC Resistance (DCR):** {getattr(comp, 'dcr', 'N/A')} mΩ")
                    st.write(f"**Shielded:** {'Yes' if getattr(comp, 'shielded', False) else 'No'}")
                    st.write(f"**Package:** {getattr(comp, 'package', 'N/A')}")
                
                # Selection reasoning
                st.write("**Why This Component:**")
                st.info(selected_component.reason)
                
                # Applied heuristics (NEW)
                if selected_component.heuristics_applied:
                    st.write("**Applied Design Heuristics:**")
                    for heuristic in selected_component.heuristics_applied[:5]:  # Show top 5 heuristics
                        st.caption(f"✅ {heuristic}")
            
            with col2:
                st.write("**📍 Purchase Information**")
                
                # Source and pricing
                st.write(f"**Source:** {distributor or 'Local Database'}")
                
                if hasattr(comp, 'price') and comp.price != 'See distributor':
                    st.write(f"**Price:** {comp.price}")
                else:
                    st.write("**Price:** Check distributor")
                
                if hasattr(comp, 'availability'):
                    st.write(f"**Availability:** {comp.availability}")
                
                st.write("---")
                st.write("**🔗 Quick Links:**")
                
                # Generate working links
                links = create_component_links(part_number, manufacturer, distributor)
                
                # Component page link
                if hasattr(comp, 'component_url') and comp.component_url:
                    st.markdown(f"🛒 [View on {distributor or 'Distributor'}]({comp.component_url})")
                else:
                    st.markdown(f"🛒 [Search Component]({links['component']})")
                
                # Datasheet link
                if hasattr(comp, 'datasheet_url') and comp.datasheet_url:
                    st.markdown(f"📄 [Download Datasheet]({comp.datasheet_url})")
                else:
                    st.markdown(f"📄 [Find Datasheet]({links['datasheet']})")
                
                if not (hasattr(comp, 'component_url') and comp.component_url):
                    st.caption("*Enhanced links available for web search results*")
        else:
            st.error(f"Selected component index {selected_idx} is out of range. Please try again.")
    else:
        st.info("👆 **Click on any row above to view detailed component information**")
        st.write("The table shows essential specifications for quick comparison. Select a component to see:")
        st.write("• Complete technical specifications")  
        st.write("• Selection reasoning")
        st.write("• Purchase links and datasheet access")
        st.write("• Pricing and availability information")

def show_detailed_rationale(suggestion: ComponentSuggestion, component_type: str):
    """
    Show detailed rationale for why this component is a top suggestion
    
    Args:
        suggestion: The component suggestion
        component_type: Type of component
    """
    comp = suggestion.component
    
    if component_type == 'mosfet':
        show_mosfet_rationale(suggestion)
    elif component_type in ['capacitor', 'input_capacitor']:
        show_capacitor_rationale(suggestion, component_type)
    elif component_type == 'inductor':
        show_inductor_rationale(suggestion)


def show_mosfet_rationale(suggestion: ComponentSuggestion):
    """Show detailed MOSFET selection rationale"""
    comp = suggestion.component
    
    st.write("**🎯 Selection Rationale:**")
    
    # VDS Headroom Analysis
    vds = getattr(comp, 'vds', 0)
    if vds > 0:
        st.write(f"• **Voltage Headroom**: {vds}V rating provides excellent protection against voltage spikes and layout-induced overshoots")
    
    # Current Capability
    current = getattr(comp, 'id', 0)
    if current > 0:
        st.write(f"• **Current Capacity**: {current}A continuous rating ensures reliable operation with safety margin")
    
    # Efficiency Analysis
    rdson = getattr(comp, 'rdson', 0)
    if rdson > 0:
        efficiency = getattr(comp, 'efficiency_range', '')
        st.write(f"• **Efficiency**: {rdson}mΩ RDS(on) contributes to {efficiency} efficiency range")
    
    # Gate Characteristics
    qg = getattr(comp, 'qg', 0)
    if qg > 0:
        st.write(f"• **Gate Drive**: {qg}nC total gate charge enables fast switching with moderate drive requirements")
    
    # Thermal Performance
    if hasattr(comp, 'junction_temp_max'):
        temp_max = getattr(comp, 'junction_temp_max', 150)
        st.write(f"• **Thermal Robustness**: {temp_max}°C max junction temperature for reliable high-temperature operation")
    
    # Manufacturer Reputation
    manufacturer = getattr(comp, 'manufacturer', '')
    if manufacturer:
        st.write(f"• **Manufacturer Trust**: {manufacturer} components are known for quality and reliability in power applications")
    
    st.write("**💡 Why This Beats Alternatives:**")
    st.write("• Superior balance of voltage/current ratings with efficiency")
    st.write("• Optimized for the specific switching frequency and thermal requirements")
    st.write("• Meets all design heuristics from power electronics best practices")


def show_capacitor_rationale(suggestion: ComponentSuggestion, component_type: str):
    """Show detailed capacitor selection rationale"""
    comp = suggestion.component
    
    st.write("**🎯 Selection Rationale:**")
    
    # Capacitance Analysis
    cap = getattr(comp, 'capacitance', 0)
    if cap > 0:
        st.write(f"• **Capacitance**: {cap}µF provides optimal filtering with minimal size/weight penalty")
    
    # Voltage Rating
    voltage = getattr(comp, 'voltage', 0)
    if voltage > 0:
        st.write(f"• **Voltage Rating**: {voltage}V ensures long-term reliability with voltage derating margin")
    
    # ESR Performance
    esr = getattr(comp, 'esr', '')
    if esr:
        st.write(f"• **ESR Performance**: {esr} equivalent series resistance minimizes power losses")
    
    # Dielectric Type
    dielectric = getattr(comp, 'dielectric', getattr(comp, 'type', ''))
    if dielectric:
        st.write(f"• **Dielectric**: {dielectric} technology optimized for {'input filtering' if component_type == 'input_capacitor' else 'output decoupling'}")
    
    # Temperature Range
    temp_range = getattr(comp, 'temp_range', '')
    if temp_range:
        st.write(f"• **Temperature Range**: {temp_range} ensures operation across full environmental conditions")
    
    # Ripple Current (for input capacitors)
    if component_type == 'input_capacitor' and hasattr(comp, 'ripple_rating'):
        ripple = getattr(comp, 'ripple_rating', 0)
        if ripple > 0:
            st.write(f"• **Ripple Handling**: {ripple}A ripple current rating prevents overheating from AC components")
    
    st.write("**💡 Why This Beats Alternatives:**")
    st.write("• Optimal capacitance-to-size ratio for the application")
    st.write("• Superior ESR characteristics reduce circuit losses")
    st.write("• Proven reliability in switching power supply applications")


def show_inductor_rationale(suggestion: ComponentSuggestion):
    """Show detailed inductor selection rationale"""
    comp = suggestion.component
    
    st.write("**🎯 Selection Rationale:**")
    
    # Inductance Value
    inductance = getattr(comp, 'inductance', 0)
    if inductance > 0:
        st.write(f"• **Inductance**: {inductance}µH provides optimal ripple current reduction and efficiency")
    
    # Current Rating
    current = getattr(comp, 'current', 0)
    if current > 0:
        st.write(f"• **Current Rating**: {current}A saturation current ensures operation without core saturation")
    
    # DCR (DC Resistance)
    dcr = getattr(comp, 'dcr', 0)
    if dcr > 0:
        st.write(f"• **Efficiency**: {dcr}mΩ DC resistance minimizes conduction losses in the power path")
    
    # Core Material
    core_type = getattr(comp, 'core_type', '')
    if core_type:
        st.write(f"• **Core Technology**: {core_type} material provides optimal balance of size, cost, and performance")
    
    # Shielding
    shielded = getattr(comp, 'shielded', False)
    if shielded:
        st.write("• **EMI Performance**: Shielded construction reduces electromagnetic interference")
    
    # Package Type
    package = getattr(comp, 'package', '')
    if package:
        st.write(f"• **Package**: {package} form factor optimized for PCB layout and thermal management")
    
    st.write("**💡 Why This Beats Alternatives:**")
    st.write("• Precise inductance value minimizes output ripple and maximizes efficiency")
    st.write("• Low DCR reduces power losses and improves thermal performance")
    st.write("• Core saturation current provides safety margin for transient conditions")
    """
    Filter suggestions based on source type (web vs local)
    
    Args:
        suggestions: List of all suggestions
        use_web_search: If True, return only web results; if False, return only local results
    
    Returns:
        Filtered list of suggestions
    """
    if not suggestions:
        return []
    
    filtered = []
    
    for suggestion in suggestions:
        comp = suggestion.component
        is_web_result = hasattr(comp, 'distributor') and getattr(comp, 'distributor', '') in ['Mouser', 'Digikey']
        
        if use_web_search and is_web_result:
            filtered.append(suggestion)
        elif not use_web_search and not is_web_result:
            filtered.append(suggestion)
    
    return filtered