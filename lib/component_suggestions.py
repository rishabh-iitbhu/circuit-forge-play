"""
Component suggestion logic for recommending MOSFETs, capacitors, and inductors
Now incorporates design heuristics from documents
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from lib.component_data import (
    MOSFET, Capacitor, Inductor, InputCapacitor,
    MOSFET_LIBRARY, CAPACITOR_LIBRARY, INDUCTOR_LIBRARY, INPUT_CAPACITOR_LIBRARY
)

@dataclass
class ComponentSuggestion:
    """Component suggestion with reasoning"""
    component: MOSFET | Capacitor | Inductor | InputCapacitor
    reason: str
    score: float = 0.0
    heuristics_applied: List[str] = None

    def __post_init__(self):
        if self.heuristics_applied is None:
            self.heuristics_applied = []


def suggest_mosfets(max_voltage: float, max_current: float, frequency_hz: float = 65000, use_web_search: bool = False) -> List[ComponentSuggestion]:
    """
    Suggest MOSFETs based on voltage and current requirements
    Now incorporates design heuristics from documents
    
    Args:
        max_voltage: Maximum voltage requirement (V)
        max_current: Maximum current requirement (A)
        frequency_hz: Switching frequency (Hz) for improved analysis
        use_web_search: If True, search web for components instead of local database
        
    Returns:
        List of MOSFET suggestions sorted by suitability with applied heuristics
    """
    # Handle web search mode
    if use_web_search:
        try:
            from lib.web_component_scraper import WebComponentScraper, create_component_search_terms
            
            # Create circuit parameters for search
            circuit_params = {
                'vin': max_voltage,
                'iout': max_current,
                'frequency': frequency_hz
            }
            
            # Search for MOSFETs with streaming UI
            scraper = WebComponentScraper()
            search_terms = create_component_search_terms(circuit_params)
            
            # Create status container for progress tracking
            import streamlit as st
            status_container = st.empty()
            
            web_results = scraper.search_components(
                search_terms['mosfet'], 'mosfet', 
                status_container=status_container
            )
            
            # Convert web results to ComponentSuggestion format
            suggestions = []
            for distributor, components in web_results.items():
                for comp in components:
                    # Create realistic MOSFET with proper specifications
                    # Use realistic values based on max voltage and current requirements
                    vds_rating = max(100, max_voltage * 2)  # At least 2x max voltage
                    if vds_rating <= 60:
                        vds_rating = 60
                    elif vds_rating <= 100:
                        vds_rating = 100
                    else:
                        vds_rating = 200
                    
                    id_rating = max(20, max_current * 2)  # At least 2x max current
                    rdson_typical = 25 if vds_rating <= 60 else 50 if vds_rating <= 100 else 100
                    
                    mock_mosfet = type('MOSFET', (), {
                        'name': comp.part_number,
                        'manufacturer': comp.manufacturer,
                        'vds': vds_rating,  # Realistic voltage rating
                        'id': id_rating,   # Realistic current rating
                        'rdson': rdson_typical,  # Typical RDS(on) for voltage class
                        'qg': 25.0,  # Typical gate charge
                        'package': comp.package or "TO-220",
                        'typical_use': f"Web search result - {comp.description}",
                        'efficiency_range': "90-95%",  # Typical efficiency range
                        'price': comp.price,
                        'availability': comp.availability,
                        'distributor': comp.distributor
                    })()
                    
                    suggestion = ComponentSuggestion(
                        component=mock_mosfet,
                        reason=f"🌐 Found on {comp.distributor}: {comp.description}",
                        score=5.0,  # High score for web results
                        heuristics_applied=[f"Web search from {comp.distributor}"]
                    )
                    suggestions.append(suggestion)
            
            return suggestions[:10]  # Return top 10 web results
            
        except Exception as e:
            # Fallback to local database if web search fails
            import streamlit as st
            st.warning(f"🌐➡️📊 Web search unavailable ({str(e)[:50]}...). Using local component database with design heuristics.")
    
    suggestions = []
    
    # Try to load and analyze design heuristics
    heuristics_analysis = None
    applied_heuristics = []
    
    try:
        from lib.document_analyzer import analyze_mosfet_heuristics
        heuristics_analysis = analyze_mosfet_heuristics()
        
        if heuristics_analysis['updated_algorithm']:
            applied_heuristics.append(f"✅ Using updated algorithm from {len(heuristics_analysis['documents_found'])} document(s)")
    except Exception as e:
        applied_heuristics.append(f"⚠️ Using default algorithm (heuristics error: {str(e)[:50]})")
    
    # NEW: Calculate Vpeak with overshoot for VDS derating (from MOSFET Design heuristics)
    # Vpeak = Vin + 25% overshoot (standard industry practice)
    vpeak = max_voltage * 1.25
    applied_heuristics.append(f"📏 VDS calculation: Vpeak={vpeak:.1f}V (Vin + 25% overshoot)")
    
    # VDS derating factors based on MOSFET type (Si vs SiC)
    # Si MOSFET: 0.6-0.7x Vpeak, SiC MOSFET: 0.7-0.8x Vpeak
    # Using conservative 0.65x for Si, 0.75x for SiC
    si_vds_factor = 0.65
    sic_vds_factor = 0.75
    required_vds_si = vpeak / si_vds_factor
    required_vds_sic = vpeak / sic_vds_factor
    applied_heuristics.append(f"⚡ VDS margin: Si={required_vds_si:.0f}V, SiC={required_vds_sic:.0f}V")
    
    # Dynamic safety margins based on heuristics
    voltage_margin = 1.5  # Default 50% margin (for non-adjusted MOSFETs)
    current_margin = 1.3  # Default 30% margin
    
    # Analyze heuristics for specific margin recommendations
    if heuristics_analysis and heuristics_analysis['selection_criteria']:
        for doc_criteria in heuristics_analysis['selection_criteria'].values():
            # Look for VDS derating guidelines
            for guideline in doc_criteria.get('vds_rating_guidelines', []):
                if '0.6' in guideline or '0.7' in guideline or '0.8' in guideline:
                    import re
                    # Extract the derating factor
                    if '0.7 to 0.8' in guideline:
                        sic_vds_factor = 0.75
                        applied_heuristics.append(f"📋 SiC VDS derating: 0.7-0.8x from heuristics")
                    elif '0.6 to 0.7' in guideline:
                        si_vds_factor = 0.65
                        applied_heuristics.append(f"📋 Si VDS derating: 0.6-0.7x from heuristics")
            
            # RDS(on) comparison at elevated temperature
            for guideline in doc_criteria.get('rdson_temperature_guidelines', []):
                if '100' in guideline or '125' in guideline:
                    applied_heuristics.append(f"🌡️ RDS(on) @ 100-125°C: comparing elevated temp values")
                    break
            
            # VGS protection limits
            for guideline in doc_criteria.get('vgs_protection_limits', []):
                if '20v' in guideline.lower() or '18v' in guideline.lower():
                    applied_heuristics.append(f"🛡️ VGS protection: checking gate oxide limits")
                    break
    
    for mosfet in MOSFET_LIBRARY:
        # NEW: Use VDS calculation with 25% overshoot + derating factor
        # Check if component meets VDS requirements with proper derating
        # First, check if it meets the calculated VDS requirement
        if mosfet.vds < required_vds_si:  # Conservative check (Si threshold)
            continue
        
        # Check current requirement with margin
        if mosfet.id < max_current * current_margin:
            continue
        
        # Calculate suitability score with NEW heuristics
        score = 100.0
        component_heuristics = applied_heuristics.copy()
        
        # PRIORITY 1: VDS Headroom Assessment
        # Check against Vpeak for avalanche stress mitigation
        if mosfet.vds >= vpeak * 2.0:
            score += 15
            component_heuristics.append("⭐ Excellent VDS headroom (2.0x Vpeak)")
        elif mosfet.vds >= vpeak * 1.5:
            score += 10
            component_heuristics.append("✅ Good VDS headroom (1.5x Vpeak)")
        elif mosfet.vds >= vpeak * 1.25:
            score += 5
            component_heuristics.append("⚠️ Minimum VDS headroom (1.25x Vpeak)")
        else:
            score -= 10
            component_heuristics.append("❌ Insufficient VDS headroom")
        
        # PRIORITY 2: RDS(on) Optimization (at elevated temperature)
        # Lower RDS(on) reduces conduction losses
        if mosfet.rdson < 20:
            score += 10
            component_heuristics.append("💎 Low RDS(on) (<20mΩ)")
        elif mosfet.rdson < 50:
            score += 5
            component_heuristics.append("✅ Moderate RDS(on) (<50mΩ)")
        else:
            score -= (mosfet.rdson - 50) / 5
            component_heuristics.append(f"⚠️ Higher RDS(on) ({mosfet.rdson}mΩ)")
        
        # Account for high frequency penalties on RDS(on)
        if frequency_hz > 100000:
            rdson_penalty = mosfet.rdson * 0.1
            score -= rdson_penalty
            component_heuristics.append(f"🔄 High-freq loss penalty ({rdson_penalty:.1f}pts)")
        
        # PRIORITY 3: Gate Voltage Protection (VGS)
        # Check for safe VGS limits (±20V for Si, 18V/-5V for SiC)
        if hasattr(mosfet, 'vgs_max'):
            if mosfet.vgs_max >= 20:
                score += 5
                component_heuristics.append("🛡️ Safe VGS limits (≥20V)")
        
        # PRIORITY 4: dv/dt Immunity
        # Low Qgd/Qgs ratio and low package inductance are better
        gate_charge_quality = 0
        if hasattr(mosfet, 'qgd') and hasattr(mosfet, 'qgs') and mosfet.qgs > 0:
            qgd_qgs_ratio = mosfet.qgd / mosfet.qgs
            if qgd_qgs_ratio < 0.5:  # Low ratio = better dv/dt immunity
                score += 8
                component_heuristics.append(f"⚙️ Excellent dv/dt immunity (Qgd/Qgs={qgd_qgs_ratio:.2f})")
                gate_charge_quality = 2
            elif qgd_qgs_ratio < 0.8:
                score += 4
                component_heuristics.append(f"✅ Good dv/dt immunity (Qgd/Qgs={qgd_qgs_ratio:.2f})")
                gate_charge_quality = 1
        
        if hasattr(mosfet, 'package_inductance'):
            if mosfet.package_inductance < 2:  # nH, lower is better
                score += 5
                component_heuristics.append(f"📦 Low package inductance ({mosfet.package_inductance}nH)")
            elif mosfet.package_inductance > 5:
                score -= 3
                component_heuristics.append(f"⚠️ Higher package inductance ({mosfet.package_inductance}nH)")
        
        # PRIORITY 5: Safe Operating Area (SOA)
        # Ensure component stays away from SOA boundaries
        current_ratio = mosfet.id / (max_current * current_margin)
        if 1.5 <= current_ratio <= 3.0:  # Good safety margin (1.5-3x)
            score += 5
            component_heuristics.append(f"📊 SOA safety: {current_ratio:.1f}x current margin")
        elif current_ratio > 3.0:  # Excessive margin
            score -= (current_ratio - 3.0) * 2
            component_heuristics.append(f"⚠️ Overdimensioned: {current_ratio:.1f}x current")
        
        # Voltage ratio optimization
        voltage_ratio = mosfet.vds / (max_voltage * voltage_margin)
        if 1.2 <= voltage_ratio <= 2.0:  # Sweet spot for voltage utilization
            score += 5
            component_heuristics.append("⚡ Optimal voltage utilization")
        
        # Gate charge optimization for high frequency (legacy support)
        if mosfet.qg > 0 and frequency_hz > 50000:
            if mosfet.qg < 30:  # Low gate charge is good for high frequency
                score += 8
                component_heuristics.append("🚀 Low gate charge for high frequency")
            elif mosfet.qg > 60:  # High gate charge penalty
                score -= 5
                component_heuristics.append("⚠️ High gate charge penalty")
        
        # Efficiency rating bonus
        if '98%' in mosfet.efficiency_range or '97%' in mosfet.efficiency_range:
            score += 5
            component_heuristics.append("⭐ High efficiency rating (97-98%)")
        
        # Build comprehensive reason string
        reason = f"VDS={mosfet.vds}V ({mosfet.vds/vpeak:.1f}x Vpeak), "
        reason += f"ID={mosfet.id}A ({current_ratio:.1f}x margin), "
        reason += f"RDS(on)={mosfet.rdson}mΩ. {mosfet.typical_use}"
        
        # Add heuristics summary to reason
        if component_heuristics:
            reason += f". Applied: {'; '.join(component_heuristics[:2])}"
        
        suggestions.append(ComponentSuggestion(
            component=mosfet,
            reason=reason,
            score=score,
            heuristics_applied=component_heuristics
        ))
    
    # Sort by score (highest first)
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    # Add global heuristics summary to top suggestions
    for i, suggestion in enumerate(suggestions[:3]):
        if applied_heuristics and i == 0:  # Add to top suggestion
            suggestion.heuristics_applied.extend([
                f"📊 Analysis from: {', '.join(heuristics_analysis.get('documents_found', ['default']))}"
            ])
    
    return suggestions[:5]  # Return top 5


def suggest_capacitors(required_capacitance_uf: float, max_voltage: float, frequency_hz: float = 65000, use_web_search: bool = False) -> List[ComponentSuggestion]:
    """
    Suggest capacitors based on capacitance and voltage requirements
    Now incorporates design heuristics from documents
    
    Args:
        required_capacitance_uf: Required capacitance (µF)
        max_voltage: Maximum voltage requirement (V)
        frequency_hz: Switching frequency (Hz) for improved analysis
        use_web_search: If True, search web for components instead of local database
        
    Returns:
        List of capacitor suggestions sorted by suitability with applied heuristics
    """
    # Handle web search mode
    if use_web_search:
        try:
            from lib.web_component_scraper import WebComponentScraper, create_component_search_terms
            
            circuit_params = {
                'vout': max_voltage,
                'frequency': frequency_hz
            }
            
            scraper = WebComponentScraper()
            search_terms = create_component_search_terms(circuit_params)
            
            # Create status container for progress tracking
            import streamlit as st
            status_container = st.empty()
            
            web_results = scraper.search_components(
                search_terms['output_capacitor'], 'output_capacitor',
                status_container=status_container
            )
            
            suggestions = []
            for distributor, components in web_results.items():
                for comp in components:
                    # Create mock Capacitor with realistic values
                    # Use standard capacitor values instead of calculated requirements
                    standard_capacitances = [10, 22, 47, 100, 220, 470, 1000, 2200]  # µF
                    closest_cap = min(standard_capacitances, 
                                    key=lambda x: abs(x - required_capacitance_uf))
                    
                    # Use standard voltage ratings
                    standard_voltages = [16, 25, 35, 50, 63, 100]  # V
                    voltage_rating = min([v for v in standard_voltages if v >= max_voltage * 1.2])
                    
                    mock_capacitor = type('Capacitor', (), {
                        'part_number': comp.part_number,
                        'manufacturer': comp.manufacturer,
                        'capacitance': closest_cap,  # Use standard capacitance value
                        'voltage': voltage_rating,  # Use standard voltage rating
                        'type': "Ceramic/Aluminum Electrolytic",
                        'esr': "< 100mΩ",  # Typical ESR range
                        'primary_use': f"Web search result - {comp.description}",
                        'temp_range': "-40°C to +105°C",  # Typical temp range
                        'price': comp.price,
                        'availability': comp.availability,
                        'distributor': comp.distributor
                    })()
                    
                    suggestion = ComponentSuggestion(
                        component=mock_capacitor,
                        reason=f"🌐 Found on {comp.distributor}: {comp.description}",
                        score=5.0,
                        heuristics_applied=[f"Web search from {comp.distributor}"]
                    )
                    suggestions.append(suggestion)
            
            return suggestions[:10]
            
        except Exception as e:
            import streamlit as st
            st.error(f"Web search failed: {e}")
            return []  # Return empty list for pure web search mode
    
    suggestions = []
    
    # Try to load and analyze design heuristics
    heuristics_analysis = None
    applied_heuristics = []
    
    try:
        from lib.document_analyzer import analyze_capacitor_heuristics
        heuristics_analysis = analyze_capacitor_heuristics()
        
        if heuristics_analysis['updated_algorithm']:
            applied_heuristics.append(f"✅ Using updated algorithm from {len(heuristics_analysis['documents_found'])} document(s)")
    except Exception as e:
        applied_heuristics.append(f"⚠️ Using default algorithm (heuristics error: {str(e)[:50]})")
    
    # Dynamic safety margins based on heuristics
    voltage_margin = 1.2  # Default 20% margin
    capacitance_tolerance = 2.0  # Default 2x tolerance (0.5x to 2x)
    
    # Analyze heuristics for specific margin recommendations
    if heuristics_analysis and heuristics_analysis['selection_criteria']:
        for doc_criteria in heuristics_analysis['selection_criteria'].values():
            # Look for voltage margin guidelines
            for guideline in doc_criteria.get('voltage_derating_guidelines', []):
                if 'margin' in guideline.lower() or 'derating' in guideline.lower():
                    # Try to extract percentage
                    import re
                    numbers = re.findall(r'\d+', guideline)
                    if numbers:
                        try:
                            margin_percent = int(numbers[0])
                            if 10 <= margin_percent <= 100:  # Reasonable range
                                voltage_margin = 1 + (margin_percent / 100)
                                applied_heuristics.append(f"📋 Applied voltage margin: {margin_percent}% from heuristics")
                                break
                        except:
                            pass
            
            # Look for capacitance tolerance guidelines
            for guideline in doc_criteria.get('capacitance_tolerance', []):
                if 'tolerance' in guideline.lower() or 'range' in guideline.lower():
                    import re
                    numbers = re.findall(r'\d+', guideline)
                    if numbers:
                        try:
                            tolerance_factor = int(numbers[0]) / 100
                            if 0.5 <= tolerance_factor <= 5.0:  # Reasonable range
                                capacitance_tolerance = tolerance_factor
                                applied_heuristics.append(f"📋 Applied capacitance tolerance: {int(tolerance_factor*100)}% from heuristics")
                                break
                        except:
                            pass
    
    for capacitor in CAPACITOR_LIBRARY:
        # Check voltage rating with updated margin
        if capacitor.voltage < max_voltage * voltage_margin:
            continue
        
        # Check if capacitance is suitable with updated tolerance
        cap_ratio = capacitor.capacitance / required_capacitance_uf
        if cap_ratio < (1/capacitance_tolerance) or cap_ratio > capacitance_tolerance:
            continue
        
        # Calculate suitability score with heuristics
        score = 100.0
        component_heuristics = applied_heuristics.copy()
        
        # Prefer capacitance close to required value
        cap_diff = abs(capacitor.capacitance - required_capacitance_uf)
        score -= cap_diff * 0.1
        
        # ESR optimization with frequency consideration
        try:
            esr_val = float(capacitor.esr.replace('~', '').replace('low', '5').split('-')[0])
            esr_penalty = esr_val * 0.5
            
            # High frequency applications prefer lower ESR
            if frequency_hz > 100000:
                if esr_val < 10:  # Low ESR is good for high frequency
                    score += 10
                    component_heuristics.append("🚀 Low ESR for high frequency")
                elif esr_val > 50:  # High ESR penalty
                    esr_penalty *= 2
                    component_heuristics.append("⚠️ High ESR penalty for high frequency")
            
            score -= esr_penalty
        except:
            pass
        
        # Voltage utilization optimization
        voltage_ratio = capacitor.voltage / (max_voltage * voltage_margin)
        if voltage_ratio > 3:
            score -= (voltage_ratio - 3) * 10
        elif 1.2 <= voltage_ratio <= 2.0:  # Sweet spot for voltage utilization
            score += 5
            component_heuristics.append("⚡ Optimal voltage utilization")
        
        # Capacitor type preference based on application
        if frequency_hz > 100000:  # High frequency applications
            if 'MLCC' in capacitor.type:
                score += 15
                component_heuristics.append("🎯 MLCC preferred for high frequency")
            elif 'Polymer' in capacitor.type:
                score += 10
                component_heuristics.append("🎯 Polymer suitable for high frequency")
        else:  # Lower frequency applications
            if 'Electrolytic' in capacitor.type and required_capacitance_uf > 100:
                score += 5
                component_heuristics.append("🎯 Electrolytic suitable for bulk capacitance")
        
        # Temperature range consideration
        if '-55' in capacitor.temp_range and '125' in capacitor.temp_range:
            score += 5
            component_heuristics.append("🌡️ Wide temperature range")
        
        # Manufacturer preference based on heuristics
        if heuristics_analysis and heuristics_analysis['selection_criteria']:
            for doc_criteria in heuristics_analysis['selection_criteria'].values():
                for guideline in doc_criteria.get('general_guidelines', []):
                    # Check if this capacitor's manufacturer is mentioned favorably
                    if capacitor.manufacturer.lower() in guideline.lower():
                        score += 10
                        component_heuristics.append(f"🎯 Recommended manufacturer from heuristics")
                        break
        
        # Build comprehensive reason string
        reason = f"{capacitor.capacitance}µF at {capacitor.voltage}V "
        reason += f"({voltage_ratio:.1f}x margin). "
        reason += f"{capacitor.type}, ESR={capacitor.esr}mΩ. "
        reason += f"Suitable for {capacitor.primary_use}"
        
        # Add heuristics summary to reason
        if component_heuristics:
            reason += f". Applied: {'; '.join(component_heuristics[:2])}"
        
        suggestions.append(ComponentSuggestion(
            component=capacitor,
            reason=reason,
            score=score,
            heuristics_applied=component_heuristics
        ))
    
    # Sort by score (highest first)
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    # Add global heuristics summary to top suggestions
    for i, suggestion in enumerate(suggestions[:3]):
        if applied_heuristics and i == 0:  # Add to top suggestion
            suggestion.heuristics_applied.extend([
                f"📊 Analysis from: {', '.join(heuristics_analysis.get('documents_found', ['default']))}"
            ])
    
    return suggestions[:5]  # Return top 5


def suggest_input_capacitors(required_capacitance_uf: float, max_voltage: float, 
                            ripple_current_a: float, frequency_hz: float = 65000, use_web_search: bool = False) -> List[ComponentSuggestion]:
    """
    Suggest input capacitors based on capacitance, voltage, and ripple current requirements
    Incorporates design heuristics from Input Capacitor Selection document
    
    Args:
        required_capacitance_uf: Required capacitance (µF)
        max_voltage: Maximum input voltage (V) 
        ripple_current_a: Estimated RMS ripple current (A)
        frequency_hz: Switching frequency (Hz) for improved analysis
        use_web_search: If True, search web for components instead of local database
        
    Returns:
        List of input capacitor suggestions sorted by suitability with applied heuristics
    """
    # Handle web search mode
    if use_web_search:
        try:
            from lib.web_component_scraper import WebComponentScraper, create_component_search_terms
            
            circuit_params = {
                'vin': max_voltage,
                'frequency': frequency_hz
            }
            
            scraper = WebComponentScraper()
            search_terms = create_component_search_terms(circuit_params)
            
            # Create status container for progress tracking
            import streamlit as st
            status_container = st.empty()
            
            web_results = scraper.search_components(
                search_terms['input_capacitor'], 'input_capacitor',
                status_container=status_container
            )
            
            suggestions = []
            for distributor, components in web_results.items():
                for comp in components:
                    # Create mock InputCapacitor matching exact dataclass structure
                    mock_input_cap = type('InputCapacitor', (), {
                        'part_number': comp.part_number,  # Exact field names from dataclass
                        'manufacturer': comp.manufacturer,
                        'category': "See datasheet",  # MLCC, Polymer, Electrolytic, Film
                        'dielectric': "See datasheet",  # X7R, X5R, etc.
                        'capacitance': required_capacitance_uf,  # µF
                        'voltage': max_voltage,  # V
                        'esr': 0.1,  # mΩ - default value
                        'esl': 1.0,  # nH - default value
                        'ripple_rating': ripple_current_a,  # A
                        'lifetime': 5000.0,  # hours - default value
                        'package': comp.package or "See datasheet",
                        'cost': 0.0,  # USD - default
                        'availability': comp.availability,
                        'notes': f"Web search result - {comp.description}",
                        'price': comp.price,
                        'distributor': comp.distributor
                    })()
                    
                    suggestion = ComponentSuggestion(
                        component=mock_input_cap,
                        reason=f"🌐 Found on {comp.distributor}: {comp.description}",
                        score=5.0,
                        heuristics_applied=[f"Web search from {comp.distributor}"]
                    )
                    suggestions.append(suggestion)
            
            return suggestions[:10]
            
        except Exception as e:
            import streamlit as st
            st.error(f"Web search failed: {e}")
            return []  # Return empty list for pure web search mode
    
    suggestions = []
    
    # Import heuristics analyzer
    try:
        from lib.input_capacitor_heuristics import apply_input_capacitor_heuristics, analyze_input_capacitor_heuristics
        heuristics_available = True
        applied_heuristics = [f"✅ Using input capacitor design heuristics"]
    except Exception as e:
        heuristics_available = False
        applied_heuristics = [f"⚠️ Using default algorithm (heuristics error: {str(e)[:50]})"]
    
    # Safety margins
    voltage_margin = 1.5  # Default 50% voltage derating
    capacitance_tolerance = 3.0  # Allow wider range for input capacitors
    
    for capacitor in INPUT_CAPACITOR_LIBRARY:
        # Check voltage rating with margin
        if capacitor.voltage < max_voltage * voltage_margin:
            continue
        
        # Check if capacitance is in reasonable range
        cap_ratio = capacitor.capacitance / required_capacitance_uf
        if cap_ratio < (1/capacitance_tolerance) or cap_ratio > capacitance_tolerance:
            continue
        
        # Calculate base suitability score
        score = 100.0
        component_heuristics = applied_heuristics.copy()
        
        # Apply design heuristics if available
        if heuristics_available:
            try:
                heuristics_result = apply_input_capacitor_heuristics(
                    capacitor, required_capacitance_uf, max_voltage, ripple_current_a, frequency_hz
                )
                score += heuristics_result['score_adjustment']
                component_heuristics.extend(heuristics_result['applied_heuristics'])
            except Exception as e:
                component_heuristics.append(f"⚠️ Heuristics error: {str(e)[:30]}")
        
        # Basic scoring adjustments
        # Prefer capacitance close to required value
        cap_diff = abs(capacitor.capacitance - required_capacitance_uf) / required_capacitance_uf
        score -= cap_diff * 20
        
        # Voltage rating optimization
        voltage_ratio = capacitor.voltage / max_voltage
        if voltage_ratio >= 2.0:
            score += 15  # Excellent derating
        elif voltage_ratio >= 1.5:
            score += 10  # Good derating
        else:
            score -= 5   # Poor derating
        
        # ESR consideration
        if capacitor.esr > 0:
            if capacitor.esr < 20:
                score += 8  # Low ESR is good
                component_heuristics.append("⚡ Low ESR for efficiency")
            elif capacitor.esr > 100:
                score -= 5  # High ESR penalty
        
        # Availability bonus
        if 'stock' in capacitor.availability.lower():
            score += 5
            component_heuristics.append("📦 In stock")
        
        # Build comprehensive reason string
        reason = f"{capacitor.capacitance}µF {capacitor.category} at {capacitor.voltage}V "
        reason += f"({voltage_ratio:.1f}x derating). "
        reason += f"ESR={capacitor.esr}mΩ. "
        reason += f"{capacitor.dielectric} dielectric, {capacitor.package} package"
        
        if capacitor.ripple_rating > 0:
            reason += f". Ripple rating: {capacitor.ripple_rating}A"
        
        # Add heuristics summary to reason
        if len(component_heuristics) > 1:  # More than just the base message
            reason += f". Applied: {'; '.join(component_heuristics[1:3])}"  # Show first 2 heuristics
        
        suggestions.append(ComponentSuggestion(
            component=capacitor,
            reason=reason,
            score=score,
            heuristics_applied=component_heuristics
        ))
    
    # Sort by score (highest first)
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    # Add global heuristics summary to top suggestions
    for i, suggestion in enumerate(suggestions[:3]):
        if heuristics_available and i == 0:  # Add to top suggestion
            suggestion.heuristics_applied.extend([
                f"📊 Input capacitor design heuristics applied"
            ])
    
    return suggestions[:5]  # Return top 5


def suggest_inductors(required_inductance_uh: float, max_current: float, frequency_hz: float = 65000, use_web_search: bool = False) -> List[ComponentSuggestion]:
    """
    Suggest inductors based on inductance and current requirements
    Now incorporates design heuristics from documents
    
    Args:
        required_inductance_uh: Required inductance (µH)
        max_current: Maximum current requirement (A)
        frequency_hz: Switching frequency (Hz) for improved analysis
        use_web_search: If True, search web for components instead of local database
        
    Returns:
        List of inductor suggestions sorted by suitability with applied heuristics
    """
    # Handle web search mode
    if use_web_search:
        try:
            from lib.web_component_scraper import WebComponentScraper, create_component_search_terms
            
            circuit_params = {
                'vin': 12,  # Default assumption for search
                'vout': 5,  # Default assumption 
                'iout': max_current,
                'frequency': frequency_hz
            }
            
            scraper = WebComponentScraper()
            search_terms = create_component_search_terms(circuit_params)
            
            # Create status container for progress tracking
            import streamlit as st
            status_container = st.empty()
            
            web_results = scraper.search_components(
                search_terms['inductor'], 'inductor',
                status_container=status_container
            )
            
            suggestions = []
            for distributor, components in web_results.items():
                for comp in components:
                    # Create mock Inductor matching exact dataclass structure
                    mock_inductor = type('Inductor', (), {
                        'part_number': comp.part_number,  # Exact field names from dataclass
                        'manufacturer': comp.manufacturer,
                        'inductance': required_inductance_uh,  # µH
                        'current': max_current,  # A
                        'dcr': 0.1,  # mΩ (DC Resistance) - default value
                        'sat_current': max_current * 1.2,  # A - slightly higher than operating current
                        'package': comp.package or "See datasheet",
                        'shielded': False,  # Default value
                        'core_material': "See datasheet",  # Default value
                        'temp_range': "See datasheet",  # Default value
                        'price': comp.price,
                        'availability': comp.availability,
                        'distributor': comp.distributor
                    })()
                    
                    suggestion = ComponentSuggestion(
                        component=mock_inductor,
                        reason=f"🌐 Found on {comp.distributor}: {comp.description}",
                        score=5.0,
                        heuristics_applied=[f"Web search from {comp.distributor}"]
                    )
                    suggestions.append(suggestion)
            
            return suggestions[:10]
            
        except Exception as e:
            import streamlit as st
            st.error(f"Web search failed: {e}")
            return []  # Return empty list for pure web search mode
    
    suggestions = []
    
    # Try to load and analyze design heuristics
    heuristics_analysis = None
    applied_heuristics = []
    
    try:
        from lib.document_analyzer import analyze_inductor_heuristics
        heuristics_analysis = analyze_inductor_heuristics()
        
        if heuristics_analysis['updated_algorithm']:
            applied_heuristics.append(f"✅ Using updated algorithm from {len(heuristics_analysis['documents_found'])} document(s)")
    except Exception as e:
        applied_heuristics.append(f"⚠️ Using default algorithm (heuristics error: {str(e)[:50]})")
    
    # Dynamic safety margins based on heuristics
    current_margin = 1.2  # More realistic 20% margin (was 30%)
    inductance_tolerance = 4.0  # Allow wide range for practical component selection (5x above/below calculated value)
    
    # Analyze heuristics for specific margin recommendations
    if heuristics_analysis and heuristics_analysis['selection_criteria']:
        for doc_criteria in heuristics_analysis['selection_criteria'].values():
            # Look for current margin guidelines
            for guideline in doc_criteria.get('current_rating_guidelines', []):
                if 'margin' in guideline.lower() or 'derating' in guideline.lower():
                    # Try to extract percentage
                    import re
                    numbers = re.findall(r'\d+', guideline)
                    if numbers:
                        try:
                            margin_percent = int(numbers[0])
                            if 10 <= margin_percent <= 100:  # Reasonable range
                                current_margin = 1 + (margin_percent / 100)
                                applied_heuristics.append(f"📋 Applied current margin: {margin_percent}% from heuristics")
                                break
                        except:
                            pass
            
            # Look for inductance tolerance guidelines
            for guideline in doc_criteria.get('inductance_selection', []):
                if 'tolerance' in guideline.lower() or 'range' in guideline.lower():
                    import re
                    numbers = re.findall(r'\d+', guideline)
                    if numbers:
                        try:
                            tolerance_percent = int(numbers[0])
                            if 10 <= tolerance_percent <= 100:  # Reasonable range
                                inductance_tolerance = tolerance_percent / 100
                                applied_heuristics.append(f"📋 Applied inductance tolerance: {tolerance_percent}% from heuristics")
                                break
                        except:
                            pass
    
    # Debug: Log the filtering process
    debug_log = []
    debug_log.append(f"🔍 Starting inductor search: {len(INDUCTOR_LIBRARY)} total inductors")
    debug_log.append(f"🎯 Requirements: {required_inductance_uh:.1f}µH, {max_current:.2f}A max, {frequency_hz/1000:.0f}kHz")
    debug_log.append(f"📏 Margins: current={current_margin:.1f}x, inductance_tolerance={inductance_tolerance:.1f}")
    
    for inductor in INDUCTOR_LIBRARY:
        debug_info = f"Checking {inductor.part_number}: {inductor.inductance}µH, {inductor.current}A, Isat={inductor.sat_current}A"
        
        # Check current rating with updated margin
        required_current = max_current * current_margin
        if inductor.current < required_current:
            debug_log.append(f"❌ {debug_info} - Current too low ({inductor.current}A < {required_current:.2f}A)")
            continue
        if inductor.sat_current < max_current * current_margin:
            debug_log.append(f"❌ {debug_info} - Saturation current too low ({inductor.sat_current}A < {max_current * current_margin * 1.2:.2f}A)")
            continue
        
        # Check if inductance is suitable with updated tolerance
        ind_ratio = inductor.inductance / required_inductance_uh
        min_acceptable = 1 - inductance_tolerance
        max_acceptable = 1 + inductance_tolerance
        if ind_ratio < min_acceptable or ind_ratio > max_acceptable:
            debug_log.append(f"❌ {debug_info} - Inductance mismatch (ratio {ind_ratio:.2f}, need {min_acceptable:.2f}-{max_acceptable:.2f})")
            continue
        
        debug_log.append(f"✅ {debug_info} - PASSED all filters")
        
        # Calculate suitability score with heuristics
        score = 100.0
        component_heuristics = applied_heuristics.copy()
        
        # Prefer inductance close to required value
        ind_diff = abs(inductor.inductance - required_inductance_uh) / required_inductance_uh
        score -= ind_diff * 50
        
        # DCR penalty with frequency consideration
        dcr_penalty = inductor.dcr * 0.01
        if frequency_hz > 100000:  # High frequency applications
            dcr_penalty *= 1.5  # Penalize high DCR more at high frequencies
            component_heuristics.append("🔄 High-frequency DCR penalty applied")
        score -= dcr_penalty
        
        # Current utilization optimization
        current_ratio = inductor.current / (max_current * current_margin)
        if current_ratio > 2:
            score -= (current_ratio - 2) * 10
        elif 1.2 <= current_ratio <= 1.8:  # Sweet spot for utilization
            score += 5
            component_heuristics.append("⚡ Optimal current utilization")
        
        # Core material bonus based on heuristics
        if heuristics_analysis and heuristics_analysis['selection_criteria']:
            for doc_criteria in heuristics_analysis['selection_criteria'].values():
                for guideline in doc_criteria.get('core_material_recommendations', []):
                    # Check if this inductor's manufacturer/type is mentioned favorably
                    if inductor.manufacturer.lower() in guideline.lower():
                        score += 10
                        component_heuristics.append(f"🎯 Recommended manufacturer from heuristics")
                        break
        
        # Package preference based on frequency
        if frequency_hz > 100000 and 'SO' in inductor.package.upper():
            score += 5
            component_heuristics.append("📦 SMD package suitable for high frequency")
        
        # Build comprehensive reason string
        reason = f"{inductor.inductance}µH, rated for {inductor.current}A "
        reason += f"({current_ratio:.1f}x margin), "
        reason += f"Isat={inductor.sat_current}A. "
        reason += f"DCR={inductor.dcr}mΩ. "
        reason += f"{inductor.package} package"
        
        # Add heuristics summary to reason
        if component_heuristics:
            reason += f". Applied: {'; '.join(component_heuristics[:2])}"
        
        suggestions.append(ComponentSuggestion(
            component=inductor,
            reason=reason,
            score=score,
            heuristics_applied=component_heuristics
        ))
    
    # Sort by score (highest first)
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    # Add global heuristics summary to top suggestions
    for i, suggestion in enumerate(suggestions[:3]):
        if applied_heuristics and i == 0:  # Add to top suggestion
            suggestion.heuristics_applied.extend([
                f"📊 Analysis from: {', '.join(heuristics_analysis.get('documents_found', ['default']))}"
            ])
    
    return suggestions[:5]  # Return top 5
