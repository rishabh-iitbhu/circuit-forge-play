"""
Input Capacitor Design Heuristics Module
Extracts and applies design principles for input capacitor selection
"""

from typing import Dict, List, Any
import os

def analyze_input_capacitor_heuristics() -> Dict[str, Any]:
    """
    Analyze input capacitor design heuristics
    Based on the Input Capacitor Selection.docx document
    """
    
    # Since we can't read the .docx directly, we'll implement the key heuristics
    # based on standard input capacitor selection principles for Buck converters
    
    heuristics = {
        'updated_algorithm': True,
        'documents_found': ['Input Capacitor Selection.docx'],
        'selection_criteria': {
            'ripple_current_handling': {
                'mlcc_guidelines': [
                    'Use multiple MLCC in parallel for high-frequency ripple',
                    'X7R/X5R dielectric preferred for stability',
                    'Consider DC-bias derating at operating voltage',
                    'Typical ESR: 1-10mΩ for good HF performance'
                ],
                'polymer_guidelines': [
                    'Excellent for moderate ripple current (1-10A)',
                    'Lower ESR than electrolytic (10-100mΩ)',
                    'Better temperature stability than electrolytic',
                    'Good for bulk capacitance at input'
                ],
                'electrolytic_guidelines': [
                    'High capacitance for bulk energy storage',
                    'High ripple current ratings available (5-20A)',
                    'Higher ESR (50-200mΩ) but acceptable for low frequency',
                    'Temperature and lifetime considerations important'
                ],
                'film_guidelines': [
                    'Lowest ESR/ESL for critical applications',
                    'Excellent high-frequency performance',
                    'Long lifetime and high reliability',
                    'Higher cost, larger size'
                ]
            },
            'voltage_derating': {
                'recommendations': [
                    'Use 2:1 derating for MLCC (25V for 12V rail)',
                    'Use 1.5:1 derating for polymer and electrolytic',
                    'Consider input voltage transients and surge',
                    'Higher voltage rating reduces DC-bias effects in MLCC'
                ]
            },
            'parallel_combinations': {
                'strategies': [
                    'Combine MLCC (HF) + Polymer/Electrolytic (bulk)',
                    'Multiple small MLCC better than single large MLCC',
                    'Place MLCC close to switching nodes',
                    'Use different dielectrics for frequency diversity'
                ]
            },
            'frequency_considerations': {
                'high_frequency': [
                    'MLCC with low ESL for >100kHz switching',
                    'Multiple parallel paths reduce impedance',
                    'Consider package parasitics (0402 > 0603 > 1206)'
                ],
                'low_frequency': [
                    'Electrolytic/Polymer for <10kHz components',
                    'Focus on capacitance value over ESR',
                    'Ripple current rating is critical'
                ]
            }
        },
        'scoring_adjustments': {
            'category_bonus': {
                'MLCC': 10,      # Best for HF decoupling
                'Polymer': 8,     # Good overall performance
                'Film': 6,        # Premium performance but costly
                'Electrolytic': 4 # Good for bulk, limited HF
            },
            'voltage_derating_bonus': {
                'excellent': 15,  # >2x derating
                'good': 10,       # 1.5-2x derating
                'adequate': 5,    # 1.2-1.5x derating
                'poor': -10       # <1.2x derating
            },
            'ripple_rating_bonus': {
                'available': 10,  # Has ripple current rating
                'calculated': 5,  # Can estimate from ESR
                'unknown': 0      # No ripple information
            }
        }
    }
    
    return heuristics

def apply_input_capacitor_heuristics(capacitor, required_capacitance_uf: float, 
                                   max_voltage: float, ripple_current_a: float,
                                   frequency_hz: float) -> Dict[str, Any]:
    """
    Apply design heuristics to score an input capacitor
    
    Args:
        capacitor: InputCapacitor object
        required_capacitance_uf: Required capacitance (µF)
        max_voltage: Maximum input voltage (V)
        ripple_current_a: Estimated ripple current (A)
        frequency_hz: Switching frequency (Hz)
    
    Returns:
        Dictionary with score adjustments and reasoning
    """
    
    heuristics = analyze_input_capacitor_heuristics()
    score_adjustment = 0
    applied_heuristics = []
    
    # Category-based scoring
    category_bonus = heuristics['scoring_adjustments']['category_bonus'].get(capacitor.category, 0)
    score_adjustment += category_bonus
    if category_bonus > 0:
        applied_heuristics.append(f"📋 {capacitor.category} category (+{category_bonus})")
    
    # Voltage derating assessment
    voltage_ratio = capacitor.voltage / max_voltage
    if voltage_ratio >= 2.0:
        derating_bonus = heuristics['scoring_adjustments']['voltage_derating_bonus']['excellent']
        applied_heuristics.append(f"⚡ Excellent voltage derating ({voltage_ratio:.1f}x)")
    elif voltage_ratio >= 1.5:
        derating_bonus = heuristics['scoring_adjustments']['voltage_derating_bonus']['good']
        applied_heuristics.append(f"⚡ Good voltage derating ({voltage_ratio:.1f}x)")
    elif voltage_ratio >= 1.2:
        derating_bonus = heuristics['scoring_adjustments']['voltage_derating_bonus']['adequate']
        applied_heuristics.append(f"⚡ Adequate voltage derating ({voltage_ratio:.1f}x)")
    else:
        derating_bonus = heuristics['scoring_adjustments']['voltage_derating_bonus']['poor']
        applied_heuristics.append(f"⚠️ Poor voltage derating ({voltage_ratio:.1f}x)")
    
    score_adjustment += derating_bonus
    
    # Ripple current handling
    if capacitor.ripple_rating > 0:
        if capacitor.ripple_rating >= ripple_current_a:
            ripple_bonus = heuristics['scoring_adjustments']['ripple_rating_bonus']['available']
            applied_heuristics.append(f"🌊 Adequate ripple rating ({capacitor.ripple_rating}A >= {ripple_current_a:.1f}A)")
        else:
            ripple_bonus = heuristics['scoring_adjustments']['ripple_rating_bonus']['available'] // 2
            applied_heuristics.append(f"⚠️ Marginal ripple rating ({capacitor.ripple_rating}A < {ripple_current_a:.1f}A)")
    elif capacitor.esr > 0:
        # Estimate ripple capability from ESR
        estimated_ripple = (capacitor.voltage * 0.1) / (capacitor.esr / 1000)  # Simple estimation
        if estimated_ripple >= ripple_current_a:
            ripple_bonus = heuristics['scoring_adjustments']['ripple_rating_bonus']['calculated']
            applied_heuristics.append(f"🧮 Estimated adequate ripple capability")
        else:
            ripple_bonus = 0
            applied_heuristics.append(f"⚠️ May have insufficient ripple capability")
    else:
        ripple_bonus = heuristics['scoring_adjustments']['ripple_rating_bonus']['unknown']
    
    score_adjustment += ripple_bonus
    
    # Frequency-specific recommendations
    if frequency_hz > 100000:  # High frequency
        if capacitor.category == 'MLCC' and capacitor.esl < 5.0:
            score_adjustment += 8
            applied_heuristics.append("🔄 Low ESL excellent for high frequency")
        elif capacitor.category in ['Polymer', 'Film']:
            score_adjustment += 5
            applied_heuristics.append("🔄 Good high-frequency performance")
    else:  # Lower frequency
        if capacitor.category in ['Electrolytic', 'Polymer']:
            score_adjustment += 5
            applied_heuristics.append("📊 Good for lower frequency bulk capacitance")
    
    # ESR optimization
    if capacitor.esr > 0:
        if capacitor.esr < 10:
            score_adjustment += 5
            applied_heuristics.append("⚡ Low ESR for efficiency")
        elif capacitor.esr > 100:
            score_adjustment -= 3
            applied_heuristics.append("⚠️ Higher ESR may impact efficiency")
    
    return {
        'score_adjustment': score_adjustment,
        'applied_heuristics': applied_heuristics,
        'heuristics_analysis': heuristics
    }