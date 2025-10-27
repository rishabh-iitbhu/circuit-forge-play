export interface MOSFET {
  partNumber: string;
  manufacturer: string;
  vds: number; // Drain-Source Voltage (V)
  id: number; // Continuous Drain Current (A)
  rdson: number; // On-Resistance (mΩ)
  qg: number; // Total Gate Charge (nC)
  package: string;
}

export interface Capacitor {
  partNumber: string;
  manufacturer: string;
  capacitance: number; // µF
  voltage: number; // V
  type: string; // Ceramic, Electrolytic, Film
  rippleCurrent: number; // A
  esr: number; // mΩ
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
  { partNumber: "IRFB4115PBF", manufacturer: "Infineon", vds: 150, id: 104, rdson: 6.5, qg: 120, package: "TO-220" },
  { partNumber: "IPP60R099C6", manufacturer: "Infineon", vds: 600, id: 50, rdson: 99, qg: 86, package: "TO-220" },
  { partNumber: "C3M0120090D", manufacturer: "Wolfspeed", vds: 900, id: 36, rdson: 120, qg: 35, package: "TO-247" },
  { partNumber: "STW45NM50", manufacturer: "STMicroelectronics", vds: 500, id: 45, rdson: 95, qg: 82, package: "TO-247" },
  { partNumber: "IRFP460", manufacturer: "Infineon", vds: 500, id: 20, rdson: 270, qg: 180, package: "TO-247" },
  { partNumber: "IPW65R041CFD", manufacturer: "Infineon", vds: 650, id: 71, rdson: 41, qg: 150, package: "TO-247" },
];

export const capacitorLibrary: Capacitor[] = [
  { partNumber: "EKMQ451VSN221MR50S", manufacturer: "Nippon Chemi-Con", capacitance: 220, voltage: 450, type: "Electrolytic", rippleCurrent: 2.85, esr: 110 },
  { partNumber: "B43504A5477M", manufacturer: "EPCOS", capacitance: 470, voltage: 450, type: "Electrolytic", rippleCurrent: 3.2, esr: 95 },
  { partNumber: "UVR2W101MHD", manufacturer: "Nichicon", capacitance: 100, voltage: 450, type: "Electrolytic", rippleCurrent: 1.95, esr: 180 },
  { partNumber: "C4532X7R2E105K", manufacturer: "TDK", capacitance: 1, voltage: 250, type: "Ceramic X7R", rippleCurrent: 5.0, esr: 5 },
  { partNumber: "GRM32ER72A106KA35L", manufacturer: "Murata", capacitance: 10, voltage: 100, type: "Ceramic X7R", rippleCurrent: 8.0, esr: 3 },
  { partNumber: "B32778G4105K", manufacturer: "EPCOS", capacitance: 1, voltage: 450, type: "Film MKP", rippleCurrent: 4.5, esr: 8 },
];

export const inductorLibrary: Inductor[] = [
  { partNumber: "SER2915H-472KL", manufacturer: "Coilcraft", inductance: 4700, current: 0.73, dcr: 1850, satCurrent: 0.95, package: "SER2915" },
  { partNumber: "SER2915H-103KL", manufacturer: "Coilcraft", inductance: 10000, current: 0.48, dcr: 4200, satCurrent: 0.62, package: "SER2915" },
  { partNumber: "744 043 22", manufacturer: "Würth Elektronik", inductance: 220, current: 3.2, dcr: 48, satCurrent: 4.5, package: "WE-PD" },
  { partNumber: "744 043 47", manufacturer: "Würth Elektronik", inductance: 470, current: 2.1, dcr: 105, satCurrent: 3.0, package: "WE-PD" },
  { partNumber: "DO3316P-472HC", manufacturer: "Coilcraft", inductance: 4700, current: 1.0, dcr: 1200, satCurrent: 1.3, package: "DO3316P" },
  { partNumber: "78F102J-RC", manufacturer: "Murata", inductance: 1000, current: 1.5, dcr: 280, satCurrent: 2.2, package: "Radial" },
];
