export interface MOSFET {
  name: string;
  manufacturer: string;
  vds: number; // Drain-Source Voltage (V)
  id: number; // Continuous Drain Current (A)
  rdson: number; // On-Resistance (mΩ)
  qg: number | string; // Total Gate Charge (nC)
  package: string;
  typicalUse: string;
  efficiencyRange: string;
}

export interface Capacitor {
  partNumber: string;
  manufacturer: string;
  capacitance: number; // µF
  voltage: number; // V
  type: string;
  esr: string; // mΩ
  primaryUse: string;
  tempRange: string;
}

export interface Inductor {
  partNumber: string;
  manufacturer: string;
  inductance: number; // µH
  current: number; // A
  dcr: number; // mΩ (DC Resistance)
  satCurrent: number; // A
  package: string;
}

export const mosfetLibrary: MOSFET[] = [
  { name: "BSC016N06NS", manufacturer: "Infineon", vds: 60, id: 150, rdson: 1.6, qg: 44, package: "SuperSO8", typicalUse: "Mid-power buck, low loss", efficiencyRange: "96–98%" },
  { name: "CSD19505KCS", manufacturer: "Texas Instruments", vds: 60, id: 80, rdson: 2.5, qg: 37, package: "TO-220", typicalUse: "Classic synchronous buck", efficiencyRange: "95–97%" },
  { name: "IPB017N10N5", manufacturer: "Infineon", vds: 100, id: 120, rdson: 1.7, qg: 70, package: "D²PAK", typicalUse: "48V bus robotics converter", efficiencyRange: "96–97%" },
  { name: "AOZ5311NQI", manufacturer: "Alpha & Omega", vds: 25, id: 40, rdson: 6, qg: 12, package: "DFN", typicalUse: "Compact logic supply buck", efficiencyRange: "94–96%" },
  { name: "SiSS22DN", manufacturer: "Vishay", vds: 30, id: 60, rdson: 2.2, qg: 15, package: "PowerPAK", typicalUse: "Small robots, drone logic rail", efficiencyRange: "95–97%" },
  { name: "NVMFS6H824NL", manufacturer: "OnSemi", vds: 80, id: 50, rdson: 4.3, qg: 38, package: "SO-8FL", typicalUse: "Automotive AGV converter", efficiencyRange: "95–97%" },
  { name: "BSC340N08NS3G", manufacturer: "Infineon", vds: 80, id: 90, rdson: 3.4, qg: 26, package: "SuperSO8", typicalUse: "Mid-range converter", efficiencyRange: "96–97%" },
  { name: "CSD19536KCS", manufacturer: "Texas Instruments", vds: 100, id: 100, rdson: 2.3, qg: 45, package: "TO-220", typicalUse: "High-efficiency buck", efficiencyRange: "95–97%" },
  { name: "IPB65R045CFD7", manufacturer: "Infineon", vds: 650, id: 18, rdson: 45, qg: 29, package: "TO-220", typicalUse: "SiC replacement candidate", efficiencyRange: "94–96%" },
  { name: "AOZ5332QI", manufacturer: "Alpha & Omega", vds: 60, id: 25, rdson: 8, qg: "N/A", package: "QFN (Integrated)", typicalUse: "Integrated power stage", efficiencyRange: "94–96%" },
  { name: "IRLZ44N", manufacturer: "Infineon (legacy IR)", vds: 55, id: 47, rdson: 22, qg: 67, package: "TO-220", typicalUse: "Benchmark reference MOSFET", efficiencyRange: "90–92%" },
  { name: "NTP65N10", manufacturer: "OnSemi", vds: 100, id: 60, rdson: 6.5, qg: 35, package: "TO-220", typicalUse: "Robust mid-range FET", efficiencyRange: "93–95%" },
  { name: "BSC057N08NS", manufacturer: "Infineon", vds: 80, id: 70, rdson: 5.7, qg: 40, package: "SuperSO8", typicalUse: "Common industrial buck FET", efficiencyRange: "94–96%" },
  { name: "SiR158DP", manufacturer: "Vishay", vds: 100, id: 75, rdson: 4, qg: 35, package: "PowerPAK SO-8", typicalUse: "Low gate charge FET", efficiencyRange: "95–96%" },
  { name: "FDBL9402", manufacturer: "OnSemi", vds: 40, id: 80, rdson: 3.6, qg: 18, package: "Power56", typicalUse: "Low-voltage high-efficiency", efficiencyRange: "96–98%" },
  { name: "TPHR8504PL", manufacturer: "Toshiba", vds: 40, id: 70, rdson: 4.5, qg: 20, package: "SOP Advance", typicalUse: "Toshiba for 12V rails", efficiencyRange: "95–97%" },
  { name: "AON6522", manufacturer: "Alpha & Omega", vds: 30, id: 60, rdson: 3, qg: 14, package: "DFN 5x6", typicalUse: "Compact low-side FET", efficiencyRange: "95–97%" },
  { name: "NTMFS5C628NL", manufacturer: "OnSemi", vds: 80, id: 70, rdson: 4.2, qg: 34, package: "SO-8FL", typicalUse: "High frequency efficiency", efficiencyRange: "95–97%" },
];

export const capacitorLibrary: Capacitor[] = [
  { partNumber: "C3216X7R1H106K160AC", manufacturer: "TDK", capacitance: 10, voltage: 50, type: "MLCC X7R", esr: "~2-5", primaryUse: "HF ripple + local decoupling", tempRange: "-55..125" },
  { partNumber: "C3225X7R1E226M250AB", manufacturer: "TDK", capacitance: 22, voltage: 25, type: "MLCC X7R", esr: "~2-5", primaryUse: "HF ripple + bulk on 12V", tempRange: "-55..125" },
  { partNumber: "C3216X7R1H106K160AE", manufacturer: "TDK", capacitance: 10, voltage: 50, type: "MLCC X7R", esr: "~2-5", primaryUse: "HF ripple + local decoupling", tempRange: "-55..125" },
  { partNumber: "CGA6P3X7R1E226M250AE", manufacturer: "TDK", capacitance: 22, voltage: 25, type: "MLCC X7R", esr: "~2-5", primaryUse: "HF ripple + bulk on 12V", tempRange: "-55..125" },
  { partNumber: "MMASU32MAB7106KPNA01", manufacturer: "Taiyo Yuden", capacitance: 10, voltage: 50, type: "MLCC X7R", esr: "~2-5", primaryUse: "HF ripple on 24V rail", tempRange: "-55..125" },
  { partNumber: "MMJCU32MLB7106KPPDT1", manufacturer: "Taiyo Yuden", capacitance: 10, voltage: 50, type: "MLCC X7R", esr: "~2-5", primaryUse: "HF ripple on 24V rail", tempRange: "-55..125" },
  { partNumber: "25SVPF330M", manufacturer: "Panasonic", capacitance: 330, voltage: 25, type: "Polymer (OS-CON)", esr: "~12-20", primaryUse: "Bulk energy + damping (12V)", tempRange: "-55..105" },
  { partNumber: "63SXV100M", manufacturer: "Panasonic", capacitance: 100, voltage: 63, type: "Polymer (OS-CON)", esr: "low", primaryUse: "Bulk energy + damping (24V)", tempRange: "-55..125" },
  { partNumber: "A750KW337M1VAAE020", manufacturer: "KEMET", capacitance: 330, voltage: 35, type: "Polymer Aluminum", esr: "20", primaryUse: "Bulk energy + damping (24V)", tempRange: "-55..105" },
  { partNumber: "A750KS227M1EAAE015", manufacturer: "KEMET", capacitance: 220, voltage: 63, type: "Polymer Aluminum", esr: "~15", primaryUse: "Bulk energy + damping (24V, high margin)", tempRange: "-55..105" },
  { partNumber: "RPS1C330MCN1GS", manufacturer: "Nichicon", capacitance: 33, voltage: 16, type: "Polymer Aluminum (SMD)", esr: "40", primaryUse: "Small bulk (12V aux)", tempRange: "-55..105" },
  { partNumber: "EEU-FS1V331LB", manufacturer: "Panasonic", capacitance: 330, voltage: 35, type: "Aluminum Electrolytic", esr: "low", primaryUse: "Bulk energy (24V), higher life spec", tempRange: "-55..105" },
];

export const inductorLibrary: Inductor[] = [
  { partNumber: "SER2915H-472KL", manufacturer: "Coilcraft", inductance: 4700, current: 0.73, dcr: 1850, satCurrent: 0.95, package: "SER2915" },
  { partNumber: "SER2915H-103KL", manufacturer: "Coilcraft", inductance: 10000, current: 0.48, dcr: 4200, satCurrent: 0.62, package: "SER2915" },
  { partNumber: "744 043 22", manufacturer: "Würth Elektronik", inductance: 220, current: 3.2, dcr: 48, satCurrent: 4.5, package: "WE-PD" },
  { partNumber: "744 043 47", manufacturer: "Würth Elektronik", inductance: 470, current: 2.1, dcr: 105, satCurrent: 3.0, package: "WE-PD" },
  { partNumber: "DO3316P-472HC", manufacturer: "Coilcraft", inductance: 4700, current: 1.0, dcr: 1200, satCurrent: 1.3, package: "DO3316P" },
  { partNumber: "78F102J-RC", manufacturer: "Murata", inductance: 1000, current: 1.5, dcr: 280, satCurrent: 2.2, package: "Radial" },
];
