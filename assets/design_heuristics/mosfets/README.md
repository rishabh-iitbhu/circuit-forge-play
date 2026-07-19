# MOSFET Design Heuristics

This folder contains design guidelines and selection criteria for MOSFETs in power electronics applications.

## Recommended Document Topics:

### 1. **Switching MOSFETs Selection**
- Gate charge considerations (Qg, Qgd, Qgs)
- On-resistance (RDS(on)) vs voltage rating trade-offs
- Switching speed and efficiency optimization
- Thermal considerations and package selection

### 2. **Application-Specific Guidelines**
- Buck converter MOSFET selection
- Synchronous rectifier considerations
- High-frequency switching optimization
- Low-side vs high-side driver requirements

### 3. **Design Trade-offs**
- Efficiency vs cost analysis
- Thermal management requirements
- Gate drive design considerations
- Parasitic inductance minimization

## Example Documents to Add:
- `mosfet_selection_guide_v1.docx`
- `switching_efficiency_optimization.pdf`
- `thermal_design_considerations.docx`
- `gate_drive_design_rules.txt`

## Current Selection Logic Captured for the Agent
- The agent applies a drain-current filter using $1.2 \times I_{out,max}$.
- The agent then performs comparative risk assessment for DC SOA, pulsed SOA, avalanche energy, repetitive avalanche, RDS(on) at an elevated-temperature basis, Qgd/Qgs ratio, and package inductance.
- The reasoning output explicitly states the filter journey and the final recommendation reason, including the gate-to-drain-charge / gate-to-source-charge ratio and the package inductance when those values are available from datasheet/package information and calculations.

Place your design heuristics documents in this folder for AI-powered component recommendations.