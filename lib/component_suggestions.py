"""
Component suggestion logic for recommending MOSFETs, capacitors, and inductors
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from lib.component_data import (
    MOSFET, Capacitor, Inductor,
    MOSFET_LIBRARY, CAPACITOR_LIBRARY, INDUCTOR_LIBRARY
)

@dataclass
class ComponentSuggestion:
    """Component suggestion with reasoning"""
    component: MOSFET | Capacitor | Inductor
    reason: str
    score: float = 0.0


def suggest_mosfets(max_voltage: float, max_current: float) -> List[ComponentSuggestion]:
    """
    Suggest MOSFETs based on voltage and current requirements
    
    Args:
        max_voltage: Maximum voltage requirement (V)
        max_current: Maximum current requirement (A)
        
    Returns:
        List of MOSFET suggestions sorted by suitability
    """
    suggestions = []
    
    # Safety margin
    voltage_margin = 1.5
    current_margin = 1.3
    
    for mosfet in MOSFET_LIBRARY:
        # Check if component meets requirements
        if mosfet.vds < max_voltage * voltage_margin:
            continue
        if mosfet.id < max_current * current_margin:
            continue
        
        # Calculate suitability score
        score = 100.0
        
        # Prefer lower RDS(on) for efficiency
        score -= mosfet.rdson * 2
        
        # Prefer appropriate voltage rating (not too high)
        voltage_ratio = mosfet.vds / (max_voltage * voltage_margin)
        if voltage_ratio > 2:
            score -= (voltage_ratio - 2) * 10
        
        # Prefer appropriate current rating
        current_ratio = mosfet.id / (max_current * current_margin)
        if current_ratio > 2:
            score -= (current_ratio - 2) * 5
        
        # Build reason string
        reason = f"VDS={mosfet.vds}V ({voltage_ratio:.1f}x margin), "
        reason += f"ID={mosfet.id}A ({current_ratio:.1f}x margin), "
        reason += f"RDS(on)={mosfet.rdson}mΩ. {mosfet.typical_use}"
        
        suggestions.append(ComponentSuggestion(
            component=mosfet,
            reason=reason,
            score=score
        ))
    
    # Sort by score (highest first)
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    return suggestions[:5]  # Return top 5


def suggest_capacitors(required_capacitance_uf: float, max_voltage: float) -> List[ComponentSuggestion]:
    """
    Suggest capacitors based on capacitance and voltage requirements
    
    Args:
        required_capacitance_uf: Required capacitance (µF)
        max_voltage: Maximum voltage requirement (V)
        
    Returns:
        List of capacitor suggestions sorted by suitability
    """
    suggestions = []
    
    # Safety margin
    voltage_margin = 1.2
    
    for capacitor in CAPACITOR_LIBRARY:
        # Check voltage rating
        if capacitor.voltage < max_voltage * voltage_margin:
            continue
        
        # Check if capacitance is suitable (within reasonable range)
        cap_ratio = capacitor.capacitance / required_capacitance_uf
        if cap_ratio < 0.5 or cap_ratio > 5:
            continue
        
        # Calculate suitability score
        score = 100.0
        
        # Prefer capacitance close to required value
        cap_diff = abs(capacitor.capacitance - required_capacitance_uf)
        score -= cap_diff * 0.1
        
        # Prefer lower ESR
        try:
            esr_val = float(capacitor.esr.replace('~', '').replace('low', '5').split('-')[0])
            score -= esr_val * 0.5
        except:
            pass
        
        # Prefer appropriate voltage rating (not too high)
        voltage_ratio = capacitor.voltage / (max_voltage * voltage_margin)
        if voltage_ratio > 2:
            score -= (voltage_ratio - 2) * 10
        
        # Build reason string
        reason = f"{capacitor.capacitance}µF at {capacitor.voltage}V "
        reason += f"({voltage_ratio:.1f}x margin). "
        reason += f"{capacitor.type}, ESR={capacitor.esr}mΩ. "
        reason += f"Suitable for {capacitor.primary_use}"
        
        suggestions.append(ComponentSuggestion(
            component=capacitor,
            reason=reason,
            score=score
        ))
    
    # Sort by score (highest first)
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    return suggestions[:5]  # Return top 5


def suggest_inductors(required_inductance_uh: float, max_current: float) -> List[ComponentSuggestion]:
    """
    Suggest inductors based on inductance and current requirements
    
    Args:
        required_inductance_uh: Required inductance (µH)
        max_current: Maximum current requirement (A)
        
    Returns:
        List of inductor suggestions sorted by suitability
    """
    suggestions = []
    
    # Safety margin
    current_margin = 1.3
    
    for inductor in INDUCTOR_LIBRARY:
        # Check current rating
        if inductor.current < max_current * current_margin:
            continue
        if inductor.sat_current < max_current * current_margin * 1.2:
            continue
        
        # Check if inductance is suitable (within reasonable range)
        ind_ratio = inductor.inductance / required_inductance_uh
        if ind_ratio < 0.5 or ind_ratio > 5:
            continue
        
        # Calculate suitability score
        score = 100.0
        
        # Prefer inductance close to required value
        ind_diff = abs(inductor.inductance - required_inductance_uh) / required_inductance_uh
        score -= ind_diff * 50
        
        # Prefer lower DCR for efficiency
        score -= inductor.dcr * 0.01
        
        # Prefer appropriate current rating (not too high)
        current_ratio = inductor.current / (max_current * current_margin)
        if current_ratio > 2:
            score -= (current_ratio - 2) * 10
        
        # Build reason string
        reason = f"{inductor.inductance}µH, rated for {inductor.current}A "
        reason += f"({current_ratio:.1f}x margin), "
        reason += f"Isat={inductor.sat_current}A. "
        reason += f"DCR={inductor.dcr}mΩ. "
        reason += f"{inductor.package} package"
        
        suggestions.append(ComponentSuggestion(
            component=inductor,
            reason=reason,
            score=score
        ))
    
    # Sort by score (highest first)
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    return suggestions[:5]  # Return top 5
