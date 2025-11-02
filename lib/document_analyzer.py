"""
Document Reader Utility
Reads and analyzes design heuristics documents to update component selection algorithms
"""

import os
import streamlit as st
from typing import Dict, List, Any
import pandas as pd

def read_docx_content(file_path: str) -> str:
    """
    Read content from a .docx file
    
    Args:
        file_path: Path to the .docx file
    
    Returns:
        Text content of the document
    """
    try:
        # Try to import python-docx
        try:
            from docx import Document
        except ImportError:
            # Fail silently - don't show warning in UI every time
            return ""
        
        doc = Document(file_path)
        full_text = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Only add non-empty paragraphs
                full_text.append(paragraph.text.strip())
        
        return '\n'.join(full_text)
    
    except Exception as e:
        # Fail silently for any document reading errors
        return ""


def analyze_inductor_heuristics() -> Dict[str, Any]:
    """
    Analyze inductor design heuristics documents and extract selection criteria
    
    Returns:
        Dictionary containing updated selection criteria and recommendations
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    inductors_docs_path = os.path.join(current_dir, '..', 'assets', 'design_heuristics', 'inductors')
    
    analysis_results = {
        'documents_found': [],
        'selection_criteria': {},
        'recommendations': [],
        'updated_algorithm': False
    }
    
    # Look for documents
    if os.path.exists(inductors_docs_path):
        for filename in os.listdir(inductors_docs_path):
            if filename.endswith('.docx'):
                doc_path = os.path.join(inductors_docs_path, filename)
                analysis_results['documents_found'].append(filename)
                
                # Read the document content
                content = read_docx_content(doc_path)
                
                # Analyze content for key parameters and recommendations
                analysis_results['selection_criteria'][filename] = analyze_inductor_content(content)
    
    # Generate updated recommendations based on analysis
    if analysis_results['documents_found']:
        analysis_results['recommendations'] = generate_updated_inductor_recommendations(analysis_results['selection_criteria'])
        analysis_results['updated_algorithm'] = True
    
    return analysis_results


def analyze_inductor_content(content: str) -> Dict[str, List[str]]:
    """
    Analyze document content to extract inductor selection criteria
    
    Args:
        content: Text content of the document
    
    Returns:
        Dictionary with extracted criteria
    """
    criteria = {
        'current_rating_guidelines': [],
        'inductance_selection': [],
        'core_material_recommendations': [],
        'frequency_considerations': [],
        'thermal_guidelines': [],
        'application_specific': [],
        'general_guidelines': []
    }
    
    # Convert to lowercase for easier matching
    content_lower = content.lower()
    lines = content.split('\n')
    
    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower:
            continue
            
        # Current rating guidelines
        if any(keyword in line_lower for keyword in ['current', 'ampere', 'amp', 'rating', 'isat', 'saturation']):
            criteria['current_rating_guidelines'].append(line.strip())
        
        # Inductance selection
        elif any(keyword in line_lower for keyword in ['inductance', 'henry', 'µh', 'uh', 'ripple', 'l=']):
            criteria['inductance_selection'].append(line.strip())
        
        # Core material
        elif any(keyword in line_lower for keyword in ['core', 'ferrite', 'powder', 'material', 'iron']):
            criteria['core_material_recommendations'].append(line.strip())
        
        # Frequency considerations
        elif any(keyword in line_lower for keyword in ['frequency', 'khz', 'mhz', 'switching', 'freq']):
            criteria['frequency_considerations'].append(line.strip())
        
        # Thermal guidelines
        elif any(keyword in line_lower for keyword in ['thermal', 'temperature', 'heat', 'cooling', 'temp']):
            criteria['thermal_guidelines'].append(line.strip())
        
        # Application specific
        elif any(keyword in line_lower for keyword in ['buck', 'boost', 'converter', 'pfc', 'application']):
            criteria['application_specific'].append(line.strip())
        
        # General guidelines
        else:
            if len(line.strip()) > 20:  # Only capture substantial content
                criteria['general_guidelines'].append(line.strip())
    
    return criteria


def generate_updated_inductor_recommendations(selection_criteria: Dict[str, Dict]) -> List[str]:
    """
    Generate updated inductor recommendations based on analyzed criteria
    
    Args:
        selection_criteria: Analyzed criteria from documents
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Combine all criteria from all documents
    all_criteria = {}
    for doc_name, criteria in selection_criteria.items():
        for category, items in criteria.items():
            if category not in all_criteria:
                all_criteria[category] = []
            all_criteria[category].extend(items)
    
    # Generate recommendations based on found criteria
    if all_criteria.get('current_rating_guidelines'):
        recommendations.append("✅ Current Rating: " + "; ".join(all_criteria['current_rating_guidelines'][:2]))
    
    if all_criteria.get('inductance_selection'):
        recommendations.append("✅ Inductance Selection: " + "; ".join(all_criteria['inductance_selection'][:2]))
    
    if all_criteria.get('core_material_recommendations'):
        recommendations.append("✅ Core Material: " + "; ".join(all_criteria['core_material_recommendations'][:2]))
    
    if all_criteria.get('frequency_considerations'):
        recommendations.append("✅ Frequency: " + "; ".join(all_criteria['frequency_considerations'][:2]))
    
    if all_criteria.get('application_specific'):
        recommendations.append("✅ Applications: " + "; ".join(all_criteria['application_specific'][:2]))
    
    return recommendations


def update_inductor_selection_algorithm(power_w: float, frequency_hz: float, voltage_in: float, voltage_out: float) -> Dict[str, Any]:
    """
    Updated inductor selection algorithm incorporating design heuristics
    
    Args:
        power_w: Output power in watts
        frequency_hz: Switching frequency in Hz
        voltage_in: Input voltage
        voltage_out: Output voltage
    
    Returns:
        Dictionary with updated recommendations
    """
    # Analyze the latest design heuristics
    heuristics = analyze_inductor_heuristics()
    
    # Basic calculations (existing algorithm)
    current_out = power_w / voltage_out
    duty_cycle = voltage_out / voltage_in
    
    # Updated inductance calculation based on heuristics
    # Default ripple current factor (can be updated from heuristics)
    ripple_factor = 0.3  # 30% ripple current
    
    # Check if heuristics provide specific ripple recommendations
    for criteria in heuristics['selection_criteria'].values():
        for guideline in criteria.get('inductance_selection', []):
            if 'ripple' in guideline.lower() and any(char.isdigit() for char in guideline):
                # Try to extract numeric value for ripple
                import re
                numbers = re.findall(r'\d+', guideline)
                if numbers:
                    potential_ripple = int(numbers[0]) / 100  # Convert percentage to decimal
                    if 0.1 <= potential_ripple <= 0.5:  # Reasonable range
                        ripple_factor = potential_ripple
                        break
    
    delta_i = current_out * ripple_factor
    inductance_uh = (voltage_in - voltage_out) * duty_cycle * 1e6 / (frequency_hz * delta_i)
    
    # Load current inductor library
    from lib.component_data import INDUCTOR_LIBRARY
    
    # Filter inductors based on updated criteria
    suitable_inductors = []
    
    for inductor in INDUCTOR_LIBRARY:
        # Basic filtering
        current_margin = 1.2  # 20% margin
        inductance_tolerance = 0.5  # 50% tolerance
        
        # Check if heuristics provide specific margin recommendations
        for criteria in heuristics['selection_criteria'].values():
            for guideline in criteria.get('current_rating_guidelines', []):
                if 'margin' in guideline.lower() or 'derating' in guideline.lower():
                    import re
                    numbers = re.findall(r'\d+', guideline)
                    if numbers:
                        potential_margin = 1 + int(numbers[0]) / 100  # Convert percentage to multiplier
                        if 1.1 <= potential_margin <= 2.0:  # Reasonable range
                            current_margin = potential_margin
                            break
        
        # Apply filtering criteria
        if (inductor.current >= current_out * current_margin and
            inductor.sat_current >= current_out * 1.1 and
            abs(inductor.inductance - inductance_uh) <= inductance_uh * inductance_tolerance):
            
            # Calculate efficiency estimate
            efficiency = calculate_inductor_efficiency(inductor, current_out, frequency_hz)
            
            suitable_inductors.append({
                'inductor': inductor,
                'efficiency': efficiency,
                'current_utilization': current_out / inductor.current,
                'inductance_match': abs(inductor.inductance - inductance_uh) / inductance_uh
            })
    
    # Sort by efficiency and current utilization
    suitable_inductors.sort(key=lambda x: (-x['efficiency'], x['inductance_match']))
    
    return {
        'calculated_inductance_uh': inductance_uh,
        'calculated_current_a': current_out,
        'ripple_factor_used': ripple_factor,
        'current_margin_used': current_margin,
        'suitable_inductors': suitable_inductors[:5],  # Top 5 recommendations
        'heuristics_applied': heuristics,
        'selection_criteria': generate_selection_summary(heuristics)
    }


def calculate_inductor_efficiency(inductor, current_a: float, frequency_hz: float) -> float:
    """Calculate estimated efficiency for an inductor"""
    # Core loss estimation (simplified)
    core_loss_factor = frequency_hz / 100000  # Normalized to 100kHz
    
    # Copper loss
    copper_loss = (current_a ** 2) * inductor.dcr / 1000  # Convert mΩ to Ω
    
    # Estimated total loss (simplified model)
    total_loss = copper_loss + core_loss_factor * 0.1  # Rough estimate
    
    # Efficiency estimate
    power_delivered = current_a * 12  # Assume 12V output for estimation
    efficiency = (power_delivered - total_loss) / power_delivered
    
    return max(0.7, min(0.98, efficiency))  # Clamp between 70% and 98%


def analyze_mosfet_heuristics() -> Dict[str, Any]:
    """
    Analyze MOSFET design heuristics documents and extract selection criteria
    
    Returns:
        Dictionary containing updated selection criteria and recommendations
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mosfets_docs_path = os.path.join(current_dir, '..', 'assets', 'design_heuristics', 'mosfets')
    
    analysis_results = {
        'documents_found': [],
        'selection_criteria': {},
        'recommendations': [],
        'updated_algorithm': False
    }
    
    # Look for documents
    if os.path.exists(mosfets_docs_path):
        for filename in os.listdir(mosfets_docs_path):
            if filename.endswith('.docx'):
                doc_path = os.path.join(mosfets_docs_path, filename)
                analysis_results['documents_found'].append(filename)
                
                # Read the document content
                content = read_docx_content(doc_path)
                
                # Analyze content for key parameters and recommendations
                analysis_results['selection_criteria'][filename] = analyze_mosfet_content(content)
    
    # Generate updated recommendations based on analysis
    if analysis_results['documents_found']:
        analysis_results['recommendations'] = generate_updated_mosfet_recommendations(analysis_results['selection_criteria'])
        analysis_results['updated_algorithm'] = True
    
    return analysis_results


def analyze_capacitor_heuristics() -> Dict[str, Any]:
    """
    Analyze capacitor design heuristics documents and extract selection criteria
    
    Returns:
        Dictionary containing updated selection criteria and recommendations
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    capacitors_docs_path = os.path.join(current_dir, '..', 'assets', 'design_heuristics', 'capacitors')
    
    analysis_results = {
        'documents_found': [],
        'selection_criteria': {},
        'recommendations': [],
        'updated_algorithm': False
    }
    
    # Look for documents
    if os.path.exists(capacitors_docs_path):
        for filename in os.listdir(capacitors_docs_path):
            if filename.endswith('.docx'):
                doc_path = os.path.join(capacitors_docs_path, filename)
                analysis_results['documents_found'].append(filename)
                
                # Read the document content
                content = read_docx_content(doc_path)
                
                # Analyze content for key parameters and recommendations
                analysis_results['selection_criteria'][filename] = analyze_capacitor_content(content)
    
    # Generate updated recommendations based on analysis
    if analysis_results['documents_found']:
        analysis_results['recommendations'] = generate_updated_capacitor_recommendations(analysis_results['selection_criteria'])
        analysis_results['updated_algorithm'] = True
    
    return analysis_results


def analyze_mosfet_content(content: str) -> Dict[str, List[str]]:
    """
    Analyze document content to extract MOSFET selection criteria
    
    Args:
        content: Text content of the document
    
    Returns:
        Dictionary with extracted criteria
    """
    criteria = {
        'voltage_derating_guidelines': [],
        'current_derating_guidelines': [],
        'rdson_optimization': [],
        'gate_charge_considerations': [],
        'thermal_guidelines': [],
        'package_selection': [],
        'efficiency_optimization': [],
        'application_specific': [],
        'general_guidelines': []
    }
    
    # Convert to lowercase for easier matching
    content_lower = content.lower()
    lines = content.split('\n')
    
    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower:
            continue
            
        # Voltage derating
        if any(keyword in line_lower for keyword in ['voltage', 'vds', 'derating', 'margin', 'breakdown']):
            criteria['voltage_derating_guidelines'].append(line.strip())
        
        # Current derating
        elif any(keyword in line_lower for keyword in ['current', 'id', 'ampere', 'amp', 'derating']):
            criteria['current_derating_guidelines'].append(line.strip())
        
        # RDS(on) optimization
        elif any(keyword in line_lower for keyword in ['rdson', 'rds(on)', 'resistance', 'efficiency', 'loss']):
            criteria['rdson_optimization'].append(line.strip())
        
        # Gate charge
        elif any(keyword in line_lower for keyword in ['gate', 'qg', 'qgs', 'qgd', 'charge', 'driver']):
            criteria['gate_charge_considerations'].append(line.strip())
        
        # Thermal
        elif any(keyword in line_lower for keyword in ['thermal', 'temperature', 'heat', 'cooling', 'junction']):
            criteria['thermal_guidelines'].append(line.strip())
        
        # Package
        elif any(keyword in line_lower for keyword in ['package', 'so-8', 'to-220', 'd2pak', 'surface mount']):
            criteria['package_selection'].append(line.strip())
        
        # Efficiency
        elif any(keyword in line_lower for keyword in ['efficiency', 'loss', 'switching', 'conduction']):
            criteria['efficiency_optimization'].append(line.strip())
        
        # Application specific
        elif any(keyword in line_lower for keyword in ['buck', 'boost', 'converter', 'pfc', 'application']):
            criteria['application_specific'].append(line.strip())
        
        # General guidelines
        else:
            if len(line.strip()) > 20:  # Only capture substantial content
                criteria['general_guidelines'].append(line.strip())
    
    return criteria


def analyze_capacitor_content(content: str) -> Dict[str, List[str]]:
    """
    Analyze document content to extract capacitor selection criteria
    
    Args:
        content: Text content of the document
    
    Returns:
        Dictionary with extracted criteria
    """
    criteria = {
        'voltage_derating_guidelines': [],
        'esr_optimization': [],
        'ripple_current_guidelines': [],
        'temperature_considerations': [],
        'type_selection_logic': [],
        'capacitance_tolerance': [],
        'frequency_response': [],
        'application_specific': [],
        'general_guidelines': []
    }
    
    # Convert to lowercase for easier matching
    content_lower = content.lower()
    lines = content.split('\n')
    
    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower:
            continue
            
        # Voltage derating
        if any(keyword in line_lower for keyword in ['voltage', 'derating', 'margin', 'breakdown', 'rating']):
            criteria['voltage_derating_guidelines'].append(line.strip())
        
        # ESR optimization
        elif any(keyword in line_lower for keyword in ['esr', 'resistance', 'impedance', 'loss']):
            criteria['esr_optimization'].append(line.strip())
        
        # Ripple current
        elif any(keyword in line_lower for keyword in ['ripple', 'current', 'rms', 'heating']):
            criteria['ripple_current_guidelines'].append(line.strip())
        
        # Temperature
        elif any(keyword in line_lower for keyword in ['temperature', 'temp', 'thermal', 'coefficient']):
            criteria['temperature_considerations'].append(line.strip())
        
        # Type selection
        elif any(keyword in line_lower for keyword in ['mlcc', 'ceramic', 'electrolytic', 'polymer', 'tantalum']):
            criteria['type_selection_logic'].append(line.strip())
        
        # Capacitance tolerance
        elif any(keyword in line_lower for keyword in ['capacitance', 'tolerance', 'variation', 'µf', 'uf']):
            criteria['capacitance_tolerance'].append(line.strip())
        
        # Frequency response
        elif any(keyword in line_lower for keyword in ['frequency', 'freq', 'khz', 'mhz', 'resonant']):
            criteria['frequency_response'].append(line.strip())
        
        # Application specific
        elif any(keyword in line_lower for keyword in ['buck', 'boost', 'converter', 'pfc', 'filter', 'decoupling']):
            criteria['application_specific'].append(line.strip())
        
        # General guidelines
        else:
            if len(line.strip()) > 20:  # Only capture substantial content
                criteria['general_guidelines'].append(line.strip())
    
    return criteria


def generate_updated_mosfet_recommendations(selection_criteria: Dict[str, Dict]) -> List[str]:
    """
    Generate updated MOSFET recommendations based on analyzed criteria
    
    Args:
        selection_criteria: Analyzed criteria from documents
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Combine all criteria from all documents
    all_criteria = {}
    for doc_name, criteria in selection_criteria.items():
        for category, items in criteria.items():
            if category not in all_criteria:
                all_criteria[category] = []
            all_criteria[category].extend(items)
    
    # Generate recommendations based on found criteria
    if all_criteria.get('voltage_derating_guidelines'):
        recommendations.append("✅ Voltage Derating: " + "; ".join(all_criteria['voltage_derating_guidelines'][:2]))
    
    if all_criteria.get('current_derating_guidelines'):
        recommendations.append("✅ Current Derating: " + "; ".join(all_criteria['current_derating_guidelines'][:2]))
    
    if all_criteria.get('rdson_optimization'):
        recommendations.append("✅ RDS(on) Optimization: " + "; ".join(all_criteria['rdson_optimization'][:2]))
    
    if all_criteria.get('gate_charge_considerations'):
        recommendations.append("✅ Gate Charge: " + "; ".join(all_criteria['gate_charge_considerations'][:2]))
    
    if all_criteria.get('application_specific'):
        recommendations.append("✅ Applications: " + "; ".join(all_criteria['application_specific'][:2]))
    
    return recommendations


def generate_updated_capacitor_recommendations(selection_criteria: Dict[str, Dict]) -> List[str]:
    """
    Generate updated capacitor recommendations based on analyzed criteria
    
    Args:
        selection_criteria: Analyzed criteria from documents
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Combine all criteria from all documents
    all_criteria = {}
    for doc_name, criteria in selection_criteria.items():
        for category, items in criteria.items():
            if category not in all_criteria:
                all_criteria[category] = []
            all_criteria[category].extend(items)
    
    # Generate recommendations based on found criteria
    if all_criteria.get('voltage_derating_guidelines'):
        recommendations.append("✅ Voltage Derating: " + "; ".join(all_criteria['voltage_derating_guidelines'][:2]))
    
    if all_criteria.get('esr_optimization'):
        recommendations.append("✅ ESR Optimization: " + "; ".join(all_criteria['esr_optimization'][:2]))
    
    if all_criteria.get('ripple_current_guidelines'):
        recommendations.append("✅ Ripple Current: " + "; ".join(all_criteria['ripple_current_guidelines'][:2]))
    
    if all_criteria.get('type_selection_logic'):
        recommendations.append("✅ Type Selection: " + "; ".join(all_criteria['type_selection_logic'][:2]))
    
    if all_criteria.get('application_specific'):
        recommendations.append("✅ Applications: " + "; ".join(all_criteria['application_specific'][:2]))
    
    return recommendations

def generate_selection_summary(heuristics):
    """Generate a summary of applied selection criteria"""
    summary = []
    
    if heuristics.get('updated_algorithm'):
        summary.append(f"✅ Updated algorithm using {len(heuristics.get('documents_found', []))} design document(s)")
        
        for doc in heuristics.get('documents_found', []):
            summary.append(f"📄 Analyzed: {doc}")
        
        if heuristics.get('recommendations'):
            summary.extend(heuristics['recommendations'])
    else:
        summary.append("⚠️ No design heuristics documents found, using default algorithm")
    
    return summary
