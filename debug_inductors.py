#!/usr/bin/env python3
"""
Debug script to analyze inductor filtering logic
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from component_data import INDUCTOR_LIBRARY
from calculations import CircuitCalculator, BuckInputs

def debug_inductor_filtering():
    print("🔍 Debugging Inductor Filtering Logic")
    print("=" * 50)
    
    # Test with optimized parameters from Buck calculator
    v_in = 22.5  # Volts (average of 20-25V range)
    v_out = 12.0  # Volts
    power = 12.0  # Watts
    frequency = 300_000  # Hz (300 kHz)
    
    print(f"📊 Input Parameters:")
    print(f"   V_in: {v_in}V")
    print(f"   V_out: {v_out}V") 
    print(f"   Power: {power}W")
    print(f"   Frequency: {frequency/1000:.0f}kHz")
    print()
    
    # Calculate required values using our calculations module
    max_current = power / v_out
    
    # Create calculator inputs (using typical values for parameters not directly relevant to inductance)
    calculator = CircuitCalculator()
    inputs = BuckInputs(
        v_in_min=v_in * 0.9,  # Assume 10% variation
        v_in_max=v_in * 1.1,
        v_out_min=v_out * 0.95,  # Assume 5% variation  
        v_out_max=v_out * 1.05,
        p_out_max=power,
        efficiency=0.9,
        switching_freq=frequency,
        v_ripple_max=0.1,  # 100mV typical
        v_in_ripple=0.3,   # 300mV typical
        i_out_ripple=max_current * 0.2,  # 20% ripple current
        v_overshoot=0.1,
        v_undershoot=0.1, 
        i_loadstep=max_current * 0.5
    )
    
    results = calculator.calculate_buck(inputs)
    required_inductance_uh = results.inductance * 1e6
    
    print(f"📐 Calculated Requirements:")
    print(f"   Max Current: {max_current:.2f}A")
    print(f"   Required Inductance: {required_inductance_uh:.1f}µH")
    print()
    
    # Filtering parameters from suggest_inductors function
    current_margin = 1.2
    inductance_tolerance = 4.0
    
    print(f"🎯 Filter Criteria:")
    print(f"   Current Margin: {current_margin:.1f}x")
    print(f"   Required Current Rating: {max_current * current_margin:.2f}A")
    print(f"   Required Saturation Current: {max_current * current_margin:.2f}A")
    print(f"   Inductance Tolerance: ±{inductance_tolerance*100:.0f}%")
    print(f"   Acceptable Inductance Range: {required_inductance_uh*(1-inductance_tolerance):.1f}µH - {required_inductance_uh*(1+inductance_tolerance):.1f}µH")
    print()
    
    print(f"📦 Available Inductors: {len(INDUCTOR_LIBRARY)} total")
    print("-" * 80)
    print(f"{'Part Number':<20} {'L(µH)':<8} {'I(A)':<6} {'Isat(A)':<8} {'DCR(mΩ)':<8} {'Status'}")
    print("-" * 80)
    
    passed_inductors = []
    
    for inductor in INDUCTOR_LIBRARY:
        # Check current rating
        current_check = inductor.current >= max_current * current_margin
        sat_current_check = inductor.sat_current >= max_current * current_margin
        
        # Check inductance tolerance
        ind_ratio = inductor.inductance / required_inductance_uh
        inductance_check = (1 - inductance_tolerance) <= ind_ratio <= (1 + inductance_tolerance)
        
        # Overall status
        status = "✅ PASS" if (current_check and sat_current_check and inductance_check) else "❌ FAIL"
        if status == "✅ PASS":
            passed_inductors.append(inductor)
        
        # Detailed failure reason
        reasons = []
        if not current_check:
            reasons.append(f"I<{max_current * current_margin:.2f}A")
        if not sat_current_check:
            reasons.append(f"Isat<{max_current * current_margin:.2f}A")
        if not inductance_check:
            reasons.append(f"L_ratio={ind_ratio:.2f}")
        
        detail = f" ({'; '.join(reasons)})" if reasons else ""
        
        print(f"{inductor.part_number:<20} {inductor.inductance:<8} {inductor.current:<6} {inductor.sat_current:<8} {inductor.dcr:<8} {status}{detail}")
    
    print("-" * 80)
    print(f"🎯 Results: {len(passed_inductors)}/{len(INDUCTOR_LIBRARY)} inductors passed filtering")
    
    if not passed_inductors:
        print("\n💡 Recommendations to find suitable inductors:")
        print(f"   1. Reduce frequency from {frequency/1000:.0f}kHz (increases acceptable L range)")
        print(f"   2. Increase current margin tolerance (currently {current_margin:.1f}x)")
        print(f"   3. Increase inductance tolerance (currently ±{inductance_tolerance*100:.0f}%)")
        print(f"   4. Add more inductors to database with:")
        print(f"      - Current rating > {max_current * current_margin:.2f}A")
        print(f"      - Saturation current > {max_current * current_margin:.2f}A")
        print(f"      - Inductance {required_inductance_uh*(1-inductance_tolerance):.1f}µH - {required_inductance_uh*(1+inductance_tolerance):.1f}µH")
    
    return passed_inductors

if __name__ == "__main__":
    debug_inductor_filtering()