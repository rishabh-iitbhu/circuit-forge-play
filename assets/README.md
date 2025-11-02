# Assets Directory

This directory contains all data and resources for the Circuit Designer Pro application.

## Directory Structure

```
assets/
├── component_data/          # CSV files with component specifications
│   ├── mosfets.csv         # MOSFET component library
│   ├── capacitors.csv      # Capacitor component library
│   └── inductors.csv       # Inductor component library
│
└── design_heuristics/      # Design guidelines and documentation
    ├── mosfets/            # MOSFET design documents
    ├── capacitors/         # Capacitor design documents
    └── inductors/          # Inductor design documents
```

## Component Data CSV Files

The application now dynamically loads component data from CSV files instead of hardcoded values. This allows for easy updates and additions to the component library.

### CSV File Format:

#### MOSFETs (`mosfets.csv`):
- `name`: Component name/part number
- `manufacturer`: Manufacturer name
- `vds`: Drain-Source voltage rating (V)
- `id`: Continuous drain current (A)
- `rdson`: On-resistance (mΩ)
- `qg`: Gate charge (nC), use 0 for N/A
- `package`: Package type
- `typical_use`: Application description
- `efficiency_range`: Efficiency range

#### Capacitors (`capacitors.csv`):
- `part_number`: Component part number
- `manufacturer`: Manufacturer name
- `capacitance`: Capacitance value (µF)
- `voltage`: Voltage rating (V)
- `type`: Capacitor type (MLCC, Electrolytic, etc.)
- `esr`: ESR value (mΩ)
- `primary_use`: Primary application
- `temp_range`: Temperature range (°C)

#### Inductors (`inductors.csv`):
- `part_number`: Component part number
- `manufacturer`: Manufacturer name
- `inductance`: Inductance value (µH)
- `current`: Current rating (A)
- `dcr`: DC resistance (mΩ)
- `sat_current`: Saturation current (A)
- `package`: Package type

## Design Heuristics Documents

The `design_heuristics/` folder contains component-specific design guidelines and selection criteria. Supported file formats:
- `.docx` - Microsoft Word documents
- `.pdf` - PDF documents
- `.txt` - Plain text documents
- `.md` - Markdown documents

### Usage:
1. **Add Documents**: Place design documents in the appropriate subfolder
2. **View Documents**: Use the "📋 Design Docs" button in the Component Library
3. **Refresh Recommendations**: Click "🔄 Refresh Recommendations" to analyze latest documents

## Updating Component Data

1. **Edit CSV Files**: Modify the CSV files in `component_data/` folder
2. **Add New Components**: Add rows to the appropriate CSV file
3. **Reload in App**: Use the "🔄 Reload Data" button in the Component Library

## AI-Powered Recommendations

When you ask the AI agent to renew calculations and recommendations, it will:
1. Read the latest component data from CSV files
2. Analyze design heuristics documents in the respective folders
3. Provide updated component recommendations based on current specifications and design guidelines

## Notes:
- CSV files are automatically loaded when the application starts
- Changes to CSV files require clicking the "Reload Data" button
- Design heuristics documents are scanned when the "Design Docs" button is clicked
- The system provides fallback data if CSV files are missing or corrupted