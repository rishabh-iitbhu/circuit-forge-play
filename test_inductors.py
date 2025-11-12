#!/usr/bin/env python3
"""
Test script to verify inductor recommendations work with optimized parameters
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from component_suggestions import suggest_inductors
from calculations import CircuitCalculator, BuckInputs

def test_inductor_recommendations():
    print("🔍 Testing Inductor Recommendations")
    print("=" * 50)
    
    # Test with the optimized default values from Buck calculator
    test_cases = [
        {
            'name': 'Optimized Defaults (Buck Calculator)',
            'v_in': 22.5,  # Average of 20-25V range
            'v_out': 12.0,
            'power': 12.0,
            'frequency': 300_000
        },
        {
            'name': 'Lower Power Test',
            'v_in': 20.0,
            'v_out': 12.0,
            'power': 6.0,
            'frequency': 100_000
        },
        {
            'name': 'Higher Frequency Test',
            'v_in': 24.0,
            'v_out': 5.0,
            'power': 10.0,
            'frequency': 500_000
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {case['name']}")
        print("-" * 40)
        
        # Calculate required inductance
        max_current = case['power'] / case['v_out']
        
        calculator = CircuitCalculator()
        inputs = BuckInputs(
            v_in_min=case['v_in'] * 0.9,
            v_in_max=case['v_in'] * 1.1,
            v_out_min=case['v_out'] * 0.95,
            v_out_max=case['v_out'] * 1.05,
            p_out_max=case['power'],
            efficiency=0.9,
            switching_freq=case['frequency'],
            v_ripple_max=0.1,
            v_in_ripple=0.3,
            i_out_ripple=max_current * 0.2,
            v_overshoot=0.1,
            v_undershoot=0.1,
            i_loadstep=max_current * 0.5
        )
        
        results = calculator.calculate_buck(inputs)
        required_inductance_uh = results.inductance * 1e6
        
        print(f"Parameters: {case['v_in']}V → {case['v_out']}V, {case['power']}W, {case['frequency']/1000:.0f}kHz")
        print(f"Required: {required_inductance_uh:.1f}µH, {max_current:.2f}A max")
        
        # Get inductor suggestions
        suggestions = suggest_inductors(
            required_inductance_uh=required_inductance_uh,
            max_current=max_current,
            frequency_hz=case['frequency']
        )
        
        print(f"Results: {len(suggestions)} inductor(s) found")
        
        if suggestions:
            print("✅ PASS - Found suitable inductors:")
            for j, suggestion in enumerate(suggestions, 1):
                inductor = suggestion.component
                print(f"  {j}. {inductor.part_number} ({inductor.manufacturer})")
                print(f"     {inductor.inductance}µH, {inductor.current}A, Isat={inductor.sat_current}A")
                print(f"     Reason: {suggestion.reason}")
        else:
            print("❌ FAIL - No inductors found")
    
    print("\n" + "=" * 50)
    print("✨ Test Complete!")

if __name__ == "__main__":
    test_inductor_recommendations()