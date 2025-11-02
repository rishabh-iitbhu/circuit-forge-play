# ⚡ Circuit Designer Pro# Circuit Designer Pro - Streamlit Version



A sophisticated **Streamlit-based** web application for power electronics circuit design with AI-powered component selection and design heuristics.A Python + Streamlit implementation of the Circuit Forge circuit design tool. This application helps design PFC (Power Factor Correction) and Buck converter circuits with AI-powered component calculations.



## 🌟 Features## Features



- **🔌 Buck Converter Calculator** - Complete design calculations with component recommendations- **PFC Circuit Designer**: Calculate component values for Power Factor Correction circuits

- **📚 Component Library** - Extensive database of MOSFETs, capacitors, and inductors- **Buck Converter Designer**: Calculate component values for DC-DC Buck converters

- **🤖 AI-Powered Suggestions** - Intelligent component selection using design heuristics- **Component Library**: Browse extensive database of MOSFETs, capacitors, and inductors

- **📊 Interactive Interface** - Clean, professional Streamlit UI- **Smart Component Suggestions**: Get recommendations based on your circuit requirements

- **☁️ Cloud Deployment** - Deployed on Streamlit Cloud for instant access- **Real-time Calculations**: Instant component value calculations based on input parameters



## 🚀 Live Demo## Installation



**Visit the live app**: [circuit-forge-play.streamlit.app](https://circuit-forge-play-dhyftvfmelcyhbpuwiuf75.streamlit.app/)### Prerequisites



## 📁 Project Structure- Python 3.8 or higher

- pip (Python package manager)

```

circuit-forge-play/### Setup

├── app.py                 # Main Streamlit application

├── requirements.txt       # Python dependencies1. Clone the repository:

├── lib/                   # Core libraries```bash

│   ├── calculations.py    # Circuit calculationsgit clone <repository-url>

│   ├── component_data.py  # Component databasecd circuit-forge-play

│   └── component_suggestions.py # AI recommendations```

├── pages/                 # Streamlit pages

│   ├── buck_calculator.py # Buck converter interface2. Install dependencies:

│   └── component_library.py # Component browser```bash

├── assets/               # Data and documentspip install -r requirements.txt

│   ├── component_data/   # CSV component databases```

│   └── design_heuristics/ # AI training documents

└── react-original/       # Original React implementation (archived)## Running the Application

```

To start the Streamlit application:

## 🛠️ Local Development

```bash

### Prerequisitesstreamlit run app.py

- Python 3.8+```

- pip

The application will open in your default web browser at `http://localhost:8501`

### Setup

```bash## Usage

# Clone the repository

git clone https://github.com/rishabh-iitbhu/circuit-forge-play.git### PFC Circuit Design

cd circuit-forge-play

1. Select "PFC Circuit" from the main page

# Install dependencies2. Enter voltage parameters (input/output voltage ranges)

pip install -r requirements.txt3. Enter power parameters (max output power, efficiency, voltage ripple)

4. Enter frequency parameters (switching frequency, line frequency)

# Run the application5. Click "Calculate Component Values"

streamlit run app.py6. Review calculated inductance, capacitance, and ripple current

```7. Browse recommended MOSFETs, capacitors, and inductors



The app will be available at `http://localhost:8501`### Buck Converter Design



## 🧠 AI-Powered Features1. Select "Buck Converter" from the main page

2. Enter voltage parameters (input/output voltage ranges, ripple specifications)

### Design Heuristics3. Enter power and current parameters

The application uses document analysis to provide intelligent component recommendations:4. Enter transient parameters (switching frequency, overshoot/undershoot, load step)

- **MOSFET Selection** - Based on switching frequency, voltage, and current requirements5. Click "Calculate Component Values"

- **Capacitor Selection** - Optimized for ripple current, ESR, and voltage ratings6. Review calculated inductance, output capacitance, input capacitance, and duty cycle

- **Inductor Selection** - Considers saturation current, DCR, and size constraints7. Browse recommended components



### Component Database## Project Structure

- **3000+ Components** from major manufacturers

- **Real specifications** with part numbers and ratings```

- **CSV-based** for easy updates and maintenancecircuit-forge-play/

├── app.py                      # Main Streamlit application

## 📈 Technology Stack├── requirements.txt            # Python dependencies

├── lib/                        # Core library modules

- **Frontend**: Streamlit (Python web framework)│   ├── calculations.py         # Circuit calculation functions

- **Backend**: Python with pandas, numpy│   ├── component_data.py       # Component library database

- **Data**: CSV databases, Document analysis│   └── component_suggestions.py # Component recommendation logic

- **Deployment**: Streamlit Cloud└── pages/                      # Streamlit pages

- **AI**: Custom heuristics engine with document processing    ├── pfc_calculator.py       # PFC calculator page

    ├── buck_calculator.py      # Buck converter calculator page

## 🎯 Use Cases    └── component_library.py    # Component library viewer

```

- **Power Electronics Design** - Buck converters, PFC circuits

- **Component Selection** - Find optimal components for your design## Calculations

- **Educational Tool** - Learn power electronics principles

- **Rapid Prototyping** - Quick calculations and component recommendations### PFC Circuit



## 📄 LicenseThe PFC calculator uses standard boost converter formulas:



This project is licensed under the MIT License.- **Inductance**: `L = (V_in × (V_out - V_in)) / (V_out × f_s × ΔI)`

- **Capacitance**: `C = P_out / (2π × f_line × V_out × ΔV)`

## 🤝 Contributing- **Ripple Current**: Based on 20% of maximum input current



Contributions are welcome! Please feel free to submit a Pull Request.### Buck Converter



---The Buck converter calculator uses standard buck formulas:



**Built with ❤️ using Streamlit and Python**- **Inductance**: `L = (V_out × (1 - D)) / (f_s × ΔI)`
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
