#!/usr/bin/env python3
"""
Test script to validate Circuit Designer Pro calculations
"""

from lib.calculations import CircuitCalculator, PFCInputs, BuckInputs
from lib.component_suggestions import suggest_mosfets, suggest_capacitors, suggest_inductors

def test_pfc_calculator():
    """Test PFC calculator with default values"""
    print("=" * 60)
    print("Testing PFC Circuit Calculator")
    print("=" * 60)
    
    inputs = PFCInputs(
        v_in_min=100.0,
        v_in_max=240.0,
        v_out_min=380.0,
        v_out_max=400.0,
        p_out_max=3000.0,
        efficiency=0.98,
        switching_freq=65000.0,
        line_freq_min=50.0,
        v_ripple_max=20.0
    )
    
    calc = CircuitCalculator()
    results = calc.calculate_pfc(inputs)
    
    print(f"\nInput Parameters:")
    print(f"  Input Voltage Range: {inputs.v_in_min}V - {inputs.v_in_max}V")
    print(f"  Output Voltage Range: {inputs.v_out_min}V - {inputs.v_out_max}V")
    print(f"  Max Output Power: {inputs.p_out_max}W")
    print(f"  Efficiency: {inputs.efficiency * 100}%")
    print(f"  Switching Frequency: {inputs.switching_freq / 1000:.1f} kHz")
    
    print(f"\nCalculated Results:")
    print(f"  Inductance: {results.inductance * 1000:.2f} mH")
    print(f"  Capacitance: {results.capacitance * 1e6:.2f} µF")
    print(f"  Ripple Current: {results.ripple_current:.2f} A")
    
    # Component suggestions
    max_current = inputs.p_out_max / inputs.v_in_min
    mosfets = suggest_mosfets(inputs.v_out_max, max_current)
    capacitors = suggest_capacitors(results.capacitance * 1e6, inputs.v_out_max)
    inductors = suggest_inductors(results.inductance * 1e6, results.ripple_current)
    
    print(f"\nComponent Suggestions:")
    print(f"  MOSFETs: {len(mosfets)} suitable options")
    print(f"  Capacitors: {len(capacitors)} suitable options")
    print(f"  Inductors: {len(inductors)} suitable options")
    
    if mosfets:
        print(f"\n  Top MOSFET Recommendation:")
        print(f"    {mosfets[0].component.name} ({mosfets[0].component.manufacturer})")
        print(f"    VDS: {mosfets[0].component.vds}V, ID: {mosfets[0].component.id}A")
    
    print()

def test_buck_calculator():
    """Test Buck converter calculator with default values"""
    print("=" * 60)
    print("Testing Buck Converter Calculator")
    print("=" * 60)
    
    inputs = BuckInputs(
        v_in_min=12.0,
        v_in_max=24.0,
        v_out_min=3.3,
        v_out_max=5.0,
        p_out_max=50.0,
        efficiency=0.95,
        switching_freq=500000.0,
        v_ripple_max=0.05,
        v_in_ripple=0.1,
        i_out_ripple=0.5,
        v_overshoot=0.1,
        v_undershoot=0.1,
        i_loadstep=1.0
    )
    
    calc = CircuitCalculator()
    results = calc.calculate_buck(inputs)
    
    print(f"\nInput Parameters:")
    print(f"  Input Voltage Range: {inputs.v_in_min}V - {inputs.v_in_max}V")
    print(f"  Output Voltage Range: {inputs.v_out_min}V - {inputs.v_out_max}V")
    print(f"  Max Output Power: {inputs.p_out_max}W")
    print(f"  Efficiency: {inputs.efficiency * 100}%")
    print(f"  Switching Frequency: {inputs.switching_freq / 1000:.1f} kHz")
    
    print(f"\nCalculated Results:")
    print(f"  Inductance: {results.inductance * 1e6:.2f} µH")
    print(f"  Output Capacitance: {results.output_capacitance * 1e6:.2f} µF")
    print(f"  Input Capacitance: {results.input_capacitance * 1e6:.2f} µF")
    print(f"  Max Duty Cycle: {results.duty_cycle_max * 100:.1f}%")
    
    # Component suggestions
    max_current = inputs.p_out_max / inputs.v_out_min
    mosfets = suggest_mosfets(inputs.v_in_max, max_current)
    output_caps = suggest_capacitors(results.output_capacitance * 1e6, inputs.v_out_max)
    inductors = suggest_inductors(results.inductance * 1e6, max_current)
    
    print(f"\nComponent Suggestions:")
    print(f"  MOSFETs: {len(mosfets)} suitable options")
    print(f"  Output Capacitors: {len(output_caps)} suitable options")
    print(f"  Inductors: {len(inductors)} suitable options")
    
    if mosfets:
        print(f"\n  Top MOSFET Recommendation:")
        print(f"    {mosfets[0].component.name} ({mosfets[0].component.manufacturer})")
        print(f"    VDS: {mosfets[0].component.vds}V, ID: {mosfets[0].component.id}A")
    
    print()

if __name__ == "__main__":
    test_pfc_calculator()
    test_buck_calculator()
    
    print("=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)
    print("\nTo run the Streamlit app:")
    print("  streamlit run app.py")
