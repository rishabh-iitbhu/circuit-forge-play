# Circuit Designer Pro - Streamlit Version

A Python + Streamlit implementation of the Circuit Forge circuit design tool. This application helps design PFC (Power Factor Correction) and Buck converter circuits with AI-powered component calculations.

## Features

- **PFC Circuit Designer**: Calculate component values for Power Factor Correction circuits
- **Buck Converter Designer**: Calculate component values for DC-DC Buck converters
- **Component Library**: Browse extensive database of MOSFETs, capacitors, and inductors
- **Smart Component Suggestions**: Get recommendations based on your circuit requirements
- **Real-time Calculations**: Instant component value calculations based on input parameters

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd circuit-forge-play
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage

### PFC Circuit Design

1. Select "PFC Circuit" from the main page
2. Enter voltage parameters (input/output voltage ranges)
3. Enter power parameters (max output power, efficiency, voltage ripple)
4. Enter frequency parameters (switching frequency, line frequency)
5. Click "Calculate Component Values"
6. Review calculated inductance, capacitance, and ripple current
7. Browse recommended MOSFETs, capacitors, and inductors

### Buck Converter Design

1. Select "Buck Converter" from the main page
2. Enter voltage parameters (input/output voltage ranges, ripple specifications)
3. Enter power and current parameters
4. Enter transient parameters (switching frequency, overshoot/undershoot, load step)
5. Click "Calculate Component Values"
6. Review calculated inductance, output capacitance, input capacitance, and duty cycle
7. Browse recommended components

## Project Structure

```
circuit-forge-play/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── lib/                        # Core library modules
│   ├── calculations.py         # Circuit calculation functions
│   ├── component_data.py       # Component library database
│   └── component_suggestions.py # Component recommendation logic
└── pages/                      # Streamlit pages
    ├── pfc_calculator.py       # PFC calculator page
    ├── buck_calculator.py      # Buck converter calculator page
    └── component_library.py    # Component library viewer
```

## Calculations

### PFC Circuit

The PFC calculator uses standard boost converter formulas:

- **Inductance**: `L = (V_in × (V_out - V_in)) / (V_out × f_s × ΔI)`
- **Capacitance**: `C = P_out / (2π × f_line × V_out × ΔV)`
- **Ripple Current**: Based on 20% of maximum input current

### Buck Converter

The Buck converter calculator uses standard buck formulas:

- **Inductance**: `L = (V_out × (1 - D)) / (f_s × ΔI)`
- **Output Capacitance**: `C_out = ΔI / (8 × f_s × ΔV)`
- **Input Capacitance**: `C_in = (I_out × D) / (f_s × ΔV_in)`
- **Duty Cycle**: `D = V_out / V_in`

## Component Library

The application includes an extensive database of:

- **18 MOSFETs** from leading manufacturers (Infineon, Texas Instruments, OnSemi, etc.)
- **12 Capacitors** including MLCC, Polymer, and Electrolytic types
- **6 Inductors** from Coilcraft, Würth Elektronik, and Murata

Each component includes detailed specifications and typical use cases.

## Comparison with React Version

This Streamlit version replicates all core functionality of the original React application:

- ✅ PFC and Buck converter calculators
- ✅ Component value calculations using identical formulas
- ✅ Component library with same data
- ✅ Smart component suggestions with reasoning
- ✅ Clean, intuitive user interface
- ⏳ Simulation features (planned for future release)
- ⏳ Report generation (planned for future release)

## Future Enhancements

- NGSPICE integration for circuit simulation
- Permutation analysis for component combinations
- PDF/CSV report generation
- Waveform visualization
- Component cost analysis
- Interactive circuit schematics

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

See the main repository for license information.

## Technical Notes

### Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and display
- **numpy**: Numerical computations
- **plotly**: Interactive visualizations (for future features)

### Design Philosophy

This application prioritizes:
1. **Accuracy**: Uses industry-standard formulas and real component data
2. **Usability**: Clean interface with clear parameter labels
3. **Educational**: Shows reasoning behind component suggestions
4. **Practical**: Focuses on real-world components from major manufacturers
