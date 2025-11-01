# Quick Start Guide - Circuit Designer Pro (Streamlit)

## Installation & Running

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## Quick Test

Run the test script to verify calculations:
```bash
python3 test_calculations.py
```

## Features Overview

### PFC Circuit Designer
- Calculate inductance, capacitance, and ripple current for PFC circuits
- Get component recommendations (MOSFETs, capacitors, inductors)
- All calculations based on industry-standard formulas

### Buck Converter Designer
- Calculate inductance, input/output capacitance, and duty cycle
- Get component recommendations for your power requirements
- Transient analysis parameters included

### Component Library
- 18 MOSFETs from leading manufacturers
- 12 Capacitors (MLCC, Polymer, Electrolytic)
- 6 Power Inductors
- View detailed specifications and typical use cases

## Example Usage

### PFC Circuit
1. Select "PFC Circuit" from the main page
2. Default values are pre-filled (100-240V input, 380-400V output, 3kW)
3. Click "Calculate Component Values"
4. Review results and component recommendations

### Buck Converter
1. Select "Buck Converter" from the main page
2. Default values are pre-filled (12-24V input, 3.3-5V output, 50W)
3. Click "Calculate Component Values"
4. Review results and component recommendations

## Calculation Formulas

### PFC (Boost Converter)
- **Inductance:** L = (V_in × (V_out - V_in)) / (V_out × f_s × ΔI)
- **Capacitance:** C = P_out / (2π × f_line × V_out × ΔV)
- **Ripple Current:** ΔI = I_in_max × 0.2 (20% ripple)

### Buck Converter
- **Duty Cycle:** D = V_out / V_in
- **Inductance:** L = (V_out × (1 - D)) / (f_s × ΔI)
- **Output Cap:** C_out = ΔI / (8 × f_s × ΔV)
- **Input Cap:** C_in = (I_out × D) / (f_s × ΔV_in)

## Tips

- Use realistic values for switching frequency (typically 50kHz - 1MHz)
- Higher efficiency values (0.95-0.98) are typical for modern designs
- The app suggests components with appropriate safety margins
- Lower RDS(on) MOSFETs provide better efficiency
- Lower ESR capacitors reduce ripple and heating

## Troubleshooting

**No component suggestions found:**
- Your requirements may exceed available components in the library
- Try adjusting power levels or voltage ranges
- The library focuses on common industrial components

**Calculations seem incorrect:**
- Verify all input values are positive
- Check units: V for volts, W for watts, Hz for frequency
- Ensure efficiency is between 0 and 1 (not percentage)

## Next Steps

After getting component values:
1. Review recommended components
2. Check datasheets for selected components
3. Consider thermal requirements
4. Design PCB layout with proper traces
5. Implement control circuitry

## Support

For issues or questions, please refer to:
- README_STREAMLIT.md for detailed documentation
- Original React version for feature comparison
- Component datasheets for detailed specifications
