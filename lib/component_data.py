"""
Component library data structures and database
"""

from dataclasses import dataclass
from typing import List

@dataclass
class MOSFET:
    """MOSFET component specification"""
    name: str
    manufacturer: str
    vds: float  # Drain-Source Voltage (V)
    id: float  # Continuous Drain Current (A)
    rdson: float  # On-Resistance (mΩ)
    qg: float  # Total Gate Charge (nC), use 0 for N/A
    package: str
    typical_use: str
    efficiency_range: str

@dataclass
class Capacitor:
    """Capacitor component specification"""
    part_number: str
    manufacturer: str
    capacitance: float  # µF
    voltage: float  # V
    type: str
    esr: str  # mΩ
    primary_use: str
    temp_range: str

@dataclass
class Inductor:
    """Inductor component specification"""
    part_number: str
    manufacturer: str
    inductance: float  # µH
    current: float  # A
    dcr: float  # mΩ (DC Resistance)
    sat_current: float  # A
    package: str


# MOSFET Library
MOSFET_LIBRARY: List[MOSFET] = [
    MOSFET("BSC016N06NS", "Infineon", 60, 150, 1.6, 44, "SuperSO8", "Mid-power buck, low loss", "96–98%"),
    MOSFET("CSD19505KCS", "Texas Instruments", 60, 80, 2.5, 37, "TO-220", "Classic synchronous buck", "95–97%"),
    MOSFET("IPB017N10N5", "Infineon", 100, 120, 1.7, 70, "D²PAK", "48V bus robotics converter", "96–97%"),
    MOSFET("AOZ5311NQI", "Alpha & Omega", 25, 40, 6, 12, "DFN", "Compact logic supply buck", "94–96%"),
    MOSFET("SiSS22DN", "Vishay", 30, 60, 2.2, 15, "PowerPAK", "Small robots, drone logic rail", "95–97%"),
    MOSFET("NVMFS6H824NL", "OnSemi", 80, 50, 4.3, 38, "SO-8FL", "Automotive AGV converter", "95–97%"),
    MOSFET("BSC340N08NS3G", "Infineon", 80, 90, 3.4, 26, "SuperSO8", "Mid-range converter", "96–97%"),
    MOSFET("CSD19536KCS", "Texas Instruments", 100, 100, 2.3, 45, "TO-220", "High-efficiency buck", "95–97%"),
    MOSFET("IPB65R045CFD7", "Infineon", 650, 18, 45, 29, "TO-220", "SiC replacement candidate", "94–96%"),
    MOSFET("AOZ5332QI", "Alpha & Omega", 60, 25, 8, 0, "QFN (Integrated)", "Integrated power stage", "94–96%"),
    MOSFET("IRLZ44N", "Infineon (legacy IR)", 55, 47, 22, 67, "TO-220", "Benchmark reference MOSFET", "90–92%"),
    MOSFET("NTP65N10", "OnSemi", 100, 60, 6.5, 35, "TO-220", "Robust mid-range FET", "93–95%"),
    MOSFET("BSC057N08NS", "Infineon", 80, 70, 5.7, 40, "SuperSO8", "Common industrial buck FET", "94–96%"),
    MOSFET("SiR158DP", "Vishay", 100, 75, 4, 35, "PowerPAK SO-8", "Low gate charge FET", "95–96%"),
    MOSFET("FDBL9402", "OnSemi", 40, 80, 3.6, 18, "Power56", "Low-voltage high-efficiency", "96–98%"),
    MOSFET("TPHR8504PL", "Toshiba", 40, 70, 4.5, 20, "SOP Advance", "Toshiba for 12V rails", "95–97%"),
    MOSFET("AON6522", "Alpha & Omega", 30, 60, 3, 14, "DFN 5x6", "Compact low-side FET", "95–97%"),
    MOSFET("NTMFS5C628NL", "OnSemi", 80, 70, 4.2, 34, "SO-8FL", "High frequency efficiency", "95–97%"),
]

# Capacitor Library
CAPACITOR_LIBRARY: List[Capacitor] = [
    Capacitor("C3216X7R1H106K160AC", "TDK", 10, 50, "MLCC X7R", "~2-5", "HF ripple + local decoupling", "-55..125"),
    Capacitor("C3225X7R1E226M250AB", "TDK", 22, 25, "MLCC X7R", "~2-5", "HF ripple + bulk on 12V", "-55..125"),
    Capacitor("C3216X7R1H106K160AE", "TDK", 10, 50, "MLCC X7R", "~2-5", "HF ripple + local decoupling", "-55..125"),
    Capacitor("CGA6P3X7R1E226M250AE", "TDK", 22, 25, "MLCC X7R", "~2-5", "HF ripple + bulk on 12V", "-55..125"),
    Capacitor("MMASU32MAB7106KPNA01", "Taiyo Yuden", 10, 50, "MLCC X7R", "~2-5", "HF ripple on 24V rail", "-55..125"),
    Capacitor("MMJCU32MLB7106KPPDT1", "Taiyo Yuden", 10, 50, "MLCC X7R", "~2-5", "HF ripple on 24V rail", "-55..125"),
    Capacitor("25SVPF330M", "Panasonic", 330, 25, "Polymer (OS-CON)", "~12-20", "Bulk energy + damping (12V)", "-55..105"),
    Capacitor("63SXV100M", "Panasonic", 100, 63, "Polymer (OS-CON)", "low", "Bulk energy + damping (24V)", "-55..125"),
    Capacitor("A750KW337M1VAAE020", "KEMET", 330, 35, "Polymer Aluminum", "20", "Bulk energy + damping (24V)", "-55..105"),
    Capacitor("A750KS227M1EAAE015", "KEMET", 220, 63, "Polymer Aluminum", "~15", "Bulk energy + damping (24V, high margin)", "-55..105"),
    Capacitor("RPS1C330MCN1GS", "Nichicon", 33, 16, "Polymer Aluminum (SMD)", "40", "Small bulk (12V aux)", "-55..105"),
    Capacitor("EEU-FS1V331LB", "Panasonic", 330, 35, "Aluminum Electrolytic", "low", "Bulk energy (24V), higher life spec", "-55..105"),
]

# Inductor Library
INDUCTOR_LIBRARY: List[Inductor] = [
    Inductor("SER2915H-472KL", "Coilcraft", 4700, 0.73, 1850, 0.95, "SER2915"),
    Inductor("SER2915H-103KL", "Coilcraft", 10000, 0.48, 4200, 0.62, "SER2915"),
    Inductor("744 043 22", "Würth Elektronik", 220, 3.2, 48, 4.5, "WE-PD"),
    Inductor("744 043 47", "Würth Elektronik", 470, 2.1, 105, 3.0, "WE-PD"),
    Inductor("DO3316P-472HC", "Coilcraft", 4700, 1.0, 1200, 1.3, "DO3316P"),
    Inductor("78F102J-RC", "Murata", 1000, 1.5, 280, 2.2, "Radial"),
]
