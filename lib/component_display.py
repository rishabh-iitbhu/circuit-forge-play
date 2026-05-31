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
            'Select': "🔘",  # Click indicator
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
            'Why?': "🤔 View VDS",  # Clickable VDS reasoning column
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


def filter_suggestions_by_source(suggestions: List[ComponentSuggestion], use_web_search: bool) -> List[ComponentSuggestion]:
    """Filter suggestions by source mode.

    Args:
        suggestions: List of ComponentSuggestion objects
        use_web_search: If True, return only web-sourced suggestions, else local

    Returns:
        Filtered list of ComponentSuggestion objects
    """
    if not suggestions:
        return []

    if use_web_search:
        return [s for s in suggestions if hasattr(s.component, 'distributor') and getattr(s.component, 'distributor', '') in ['Mouser', 'Digikey']]
    else:
        return [s for s in suggestions if not (hasattr(s.component, 'distributor') and getattr(s.component, 'distributor', '') in ['Mouser', 'Digikey'])]


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
            st.subheader("🧠 Why this component is a valid candidate")
            
            # Create two columns for reasoning display
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Show the component's basic reasoning
                st.info(f"**{getattr(clicked_suggestion.component, 'part_number', getattr(clicked_suggestion.component, 'name', f'Component {clicked_idx+1}'))}** - {clicked_suggestion.reason}")
                
                # Show detailed rationale based on component type
                show_detailed_rationale(clicked_suggestion, component_type)
                
                # Applied heuristics display removed
            
            with col2:
                st.write("**Quick Stats:**")
                comp = clicked_suggestion.component
                
                if component_type == 'mosfet':
                    st.metric("VDS", f"{getattr(comp, 'vds', 'N/A')}V")
                    st.metric("RDS(on)", f"{getattr(comp, 'rdson', 'N/A')}mΩ")
                    st.metric("ID", f"{getattr(comp, 'id', 'N/A')}A")
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
            st.subheader("📋 Component Details")
            
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
                
                # Applied heuristics display removed
            
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
    Show detailed rationale for why this component is a valid candidate
    
    Args:
        suggestion: The component suggestion
        component_type: Type of component
    """
    if component_type == 'mosfet':
        show_mosfet_rationale(suggestion)
    elif component_type in ['capacitor', 'input_capacitor']:
        show_capacitor_rationale(suggestion, component_type)
    elif component_type == 'inductor':
        show_inductor_rationale(suggestion)


def show_mosfet_rationale(suggestion: ComponentSuggestion):
    """Show MOSFET candidate validity and VDS reasoning"""
    comp = suggestion.component
    details = suggestion.selection_details or {}
    
    st.write("**VDS Section**")
    st.info(suggestion.reason)

    part_key = getattr(comp, 'part_number', getattr(comp, 'name', 'MOSFET')).replace(' ', '_').replace('/', '_')
    vds_toggle_key = f"show_vds_calc_{part_key}"

    if not st.session_state.get(vds_toggle_key, False):
        if st.button("Show VDS calculation logic", key=vds_toggle_key):
            st.session_state[vds_toggle_key] = True
    else:
        st.write("**VDS Calculation Logic**")
        st.write(f"- Vin max: {details.get('vin_max', 'N/A')} V")
        if details.get('voltage_margin'):
            st.write(f"- Derating factor: {details['voltage_margin']:.2f}")
        if details.get('required_vds'):
            st.write(f"- Required VDS threshold: {details['required_vds']:.1f} V")
        if details.get('vds_headroom_ratio'):
            st.write(f"- VDS headroom ratio: {details['vds_headroom_ratio']:.2f}x")
        if details.get('overshoot_guidance'):
            st.write("**Heuristic VDS overshoot guidance**")
            for guidance in details['overshoot_guidance'][:3]:
                st.write(f"- {guidance}")
        if details.get('heuristics_documents'):
            st.write(f"- Source document(s): {', '.join(details['heuristics_documents'])}")
        if st.button("Hide VDS calculation logic", key=f"hide_{vds_toggle_key}"):
            st.session_state[vds_toggle_key] = False


def show_capacitor_rationale(suggestion: ComponentSuggestion, component_type: str):
    """Capacitor rationale display removed to simplify component details."""
    return


def show_inductor_rationale(suggestion: ComponentSuggestion):
    """Inductor rationale display removed to simplify component details."""
    return
