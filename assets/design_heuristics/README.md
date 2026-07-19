# Design Heuristics Documents

This folder contains design heuristics documents for various electronic components used in circuit design.

## Folder Structure:
- `capacitors/` - Design guidelines and selection criteria for capacitors
- `inductors/` - Design guidelines and selection criteria for inductors
- `mosfets/` - Design guidelines and selection criteria for MOSFETs, including VDS, current, SOA, RDS(on), Qgd/Qgs, package inductance, gate-drive sensitivity, gm sensitivity, and reverse-recovery heuristics

## Supported File Formats:
- `.docx` - Microsoft Word documents
- `.pdf` - PDF documents
- `.txt` - Plain text documents

## Usage:
Place your design heuristics documents in the appropriate subfolder. The AI agent can read and analyze these documents to provide updated recommendations for component selection and circuit design.

## Document Guidelines:
- Use clear, descriptive filenames
- Include version numbers or dates in filenames when applicable
- Organize content with clear headings and sections
- Include parameter ranges, selection criteria, and design trade-offs
- Keep MOSFET guidance aligned with the implemented logic for VDS survival, current margin, SOA, avalanche, RDS(on), gate-charge behavior, package inductance, and reverse-recovery behavior

## Examples:
- `capacitors/mlcc_selection_guidelines_v2.docx`
- `inductors/power_inductor_design_rules_2024.docx`
- `mosfets/switching_mosfet_efficiency_guide.docx`

The system will automatically scan these folders when generating component recommendations.