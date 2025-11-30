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
    Create a standardized DataFrame for component display
    
    Args:
        suggestions: List of ComponentSuggestion objects
        component_type: Type of component ('mosfet', 'capacitor', 'inductor', 'input_capacitor')
    
    Returns:
        DataFrame with standardized columns
    """
    if not suggestions:
        return pd.DataFrame()
    
    data = []
    
    for i, suggestion in enumerate(suggestions):
        comp = suggestion.component
        
        # Base columns for all components
        row = {
            '#': i + 1,
            'Part Number': getattr(comp, 'part_number', getattr(comp, 'name', 'N/A')),
            'Manufacturer': getattr(comp, 'manufacturer', 'N/A'),
            'Score': f"{suggestion.score:.1f}/10",
            'Source': getattr(comp, 'distributor', 'Local Database'),
            'Price': getattr(comp, 'price', 'See distributor'),
            'Availability': getattr(comp, 'availability', 'Check stock'),
        }
        
        # Component-specific technical specifications
        if component_type == 'mosfet':
            row.update({
                'VDS (V)': getattr(comp, 'vds', 'N/A'),
                'ID (A)': getattr(comp, 'id', 'N/A'), 
                'RDS(on) (mΩ)': getattr(comp, 'rdson', 'N/A'),
                'Package': getattr(comp, 'package', 'N/A'),
                'Efficiency': getattr(comp, 'efficiency_range', 'See datasheet')
            })
            
        elif component_type in ['capacitor', 'output_capacitor']:
            row.update({
                'Capacitance (µF)': getattr(comp, 'capacitance', 'N/A'),
                'Voltage (V)': getattr(comp, 'voltage', 'N/A'),
                'ESR': getattr(comp, 'esr', 'N/A'),
                'Type': getattr(comp, 'type', 'N/A'),
                'Temp Range': getattr(comp, 'temp_range', 'N/A')
            })
            
        elif component_type == 'input_capacitor':
            row.update({
                'Capacitance (µF)': getattr(comp, 'capacitance', 'N/A'),
                'Voltage (V)': getattr(comp, 'voltage', 'N/A'),
                'Category': getattr(comp, 'category', 'N/A'),
                'ESR (mΩ)': getattr(comp, 'esr', 'N/A'),
                'Ripple (A)': getattr(comp, 'ripple_rating', 'N/A')
            })
            
        elif component_type == 'inductor':
            row.update({
                'Inductance (µH)': getattr(comp, 'inductance', 'N/A'),
                'Current (A)': getattr(comp, 'current', 'N/A'),
                'DCR (mΩ)': getattr(comp, 'dcr', 'N/A'),
                'Shielded': 'Yes' if getattr(comp, 'shielded', False) else 'No',
                'Package': getattr(comp, 'package', 'N/A')
            })
        
        # Add reason/explanation
        row['Why Selected'] = suggestion.reason
        
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
    Display components in a clean, standardized table format
    
    Args:
        suggestions: List of ComponentSuggestion objects
        component_type: Type of component
        title: Display title for the section
    """
    if not suggestions:
        st.warning(f"No suitable {title.lower()} found for these specifications")
        return
    
    st.subheader(title)
    
    # Create the standardized table
    df = create_component_table(suggestions, component_type)
    
    if df.empty:
        st.warning(f"No {title.lower()} data available")
        return
    
    # Display summary
    web_count = len([s for s in suggestions if hasattr(s.component, 'distributor') and getattr(s.component, 'distributor', '') in ['Mouser', 'Digikey']])
    local_count = len(suggestions) - web_count
    
    if web_count > 0 and local_count > 0:
        st.info(f"📊 Found {len(suggestions)} components: {web_count} from web search, {local_count} from local database")
    elif web_count > 0:
        st.success(f"🌐 Found {web_count} components from web search")
    else:
        st.info(f"📚 Found {local_count} components from local database")
    
    # Display the table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "#": st.column_config.NumberColumn("#", width="small"),
            "Part Number": st.column_config.TextColumn("Part Number", width="medium"),
            "Manufacturer": st.column_config.TextColumn("Manufacturer", width="medium"),
            "Score": st.column_config.TextColumn("Score", width="small"),
            "Source": st.column_config.TextColumn("Source", width="medium"),
            "Price": st.column_config.TextColumn("Price", width="small"),
            "Availability": st.column_config.TextColumn("Stock", width="small"),
            "Why Selected": st.column_config.TextColumn("Why Selected", width="large")
        }
    )
    
    # Add expandable details for top 3 components with working links
    st.markdown("### 🔗 Component Details & Links")
    
    for i, suggestion in enumerate(suggestions[:3]):
        comp = suggestion.component
        part_number = getattr(comp, 'part_number', getattr(comp, 'name', f'Component_{i+1}'))
        manufacturer = getattr(comp, 'manufacturer', 'Unknown')
        distributor = getattr(comp, 'distributor', None)
        
        # Generate working links
        links = create_component_links(part_number, manufacturer, distributor)
        
        with st.expander(f"#{i+1} {part_number} - {manufacturer}", expanded=(i==0)):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Display technical specifications based on component type
                if component_type == 'mosfet':
                    st.markdown(f"""
                    **Technical Specifications:**
                    - **VDS:** {getattr(comp, 'vds', 'N/A')}V
                    - **ID:** {getattr(comp, 'id', 'N/A')}A  
                    - **RDS(on):** {getattr(comp, 'rdson', 'N/A')}mΩ
                    - **Package:** {getattr(comp, 'package', 'N/A')}
                    - **Efficiency Range:** {getattr(comp, 'efficiency_range', 'See datasheet')}
                    """)
                
                elif component_type in ['capacitor', 'output_capacitor']:
                    st.markdown(f"""
                    **Technical Specifications:**
                    - **Capacitance:** {getattr(comp, 'capacitance', 'N/A')}µF
                    - **Voltage Rating:** {getattr(comp, 'voltage', 'N/A')}V
                    - **ESR:** {getattr(comp, 'esr', 'N/A')}
                    - **Type:** {getattr(comp, 'type', 'N/A')}
                    - **Temperature Range:** {getattr(comp, 'temp_range', 'N/A')}
                    """)
                
                elif component_type == 'input_capacitor':
                    st.markdown(f"""
                    **Technical Specifications:**
                    - **Capacitance:** {getattr(comp, 'capacitance', 'N/A')}µF
                    - **Voltage Rating:** {getattr(comp, 'voltage', 'N/A')}V
                    - **Category:** {getattr(comp, 'category', 'N/A')}
                    - **ESR:** {getattr(comp, 'esr', 'N/A')}mΩ
                    - **Ripple Current:** {getattr(comp, 'ripple_rating', 'N/A')}A
                    """)
                
                elif component_type == 'inductor':
                    st.markdown(f"""
                    **Technical Specifications:**
                    - **Inductance:** {getattr(comp, 'inductance', 'N/A')}µH
                    - **Current Rating:** {getattr(comp, 'current', 'N/A')}A
                    - **DC Resistance:** {getattr(comp, 'dcr', 'N/A')}mΩ
                    - **Shielded:** {'Yes' if getattr(comp, 'shielded', False) else 'No'}
                    - **Package:** {getattr(comp, 'package', 'N/A')}
                    """)
            
            with col2:
                # Working links
                st.markdown("**🔗 Links:**")
                st.markdown(f"[🛒 Buy Component]({links['component']})")
                st.markdown(f"[📄 Datasheet]({links['datasheet']})")
                
                # Price and availability
                price = getattr(comp, 'price', 'See distributor')
                availability = getattr(comp, 'availability', 'Check stock')
                st.markdown(f"**💰 Price:** {price}")
                st.markdown(f"**📦 Stock:** {availability}")
            
            # Selection reasoning
            st.info(f"💡 **Why Selected:** {suggestion.reason}")
            
            # Applied heuristics if available
            if hasattr(suggestion, 'heuristics_applied') and suggestion.heuristics_applied:
                st.markdown("**📋 Applied Design Heuristics:**")
                for heuristic in suggestion.heuristics_applied[:3]:
                    st.markdown(f"- {heuristic}")

def filter_suggestions_by_source(suggestions: List[ComponentSuggestion], use_web_search: bool) -> List[ComponentSuggestion]:
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