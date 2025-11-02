"""
Component library data structures and database
Now loads data from CSV files in the assets folder
"""

import os
import pandas as pd
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


def load_mosfets_from_csv() -> List[MOSFET]:
    """Load MOSFET data from CSV file"""
    try:
        # Get the directory of this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to reach the project root, then into assets
        csv_path = os.path.join(current_dir, '..', 'assets', 'component_data', 'mosfets.csv')
        
        if not os.path.exists(csv_path):
            print(f"Warning: MOSFET CSV file not found at {csv_path}, using fallback data")
            return get_fallback_mosfets()
        
        df = pd.read_csv(csv_path)
        mosfets = []
        
        for _, row in df.iterrows():
            mosfet = MOSFET(
                name=str(row['name']),
                manufacturer=str(row['manufacturer']),
                vds=float(row['vds']),
                id=float(row['id']),
                rdson=float(row['rdson']),
                qg=float(row['qg']),
                package=str(row['package']),
                typical_use=str(row['typical_use']),
                efficiency_range=str(row['efficiency_range'])
            )
            mosfets.append(mosfet)
        
        return mosfets
    except Exception as e:
        print(f"Error loading MOSFET data from CSV: {e}")
        return get_fallback_mosfets()


def load_capacitors_from_csv() -> List[Capacitor]:
    """Load Capacitor data from CSV file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, '..', 'assets', 'component_data', 'capacitors.csv')
        
        if not os.path.exists(csv_path):
            print(f"Warning: Capacitor CSV file not found at {csv_path}, using fallback data")
            return get_fallback_capacitors()
        
        df = pd.read_csv(csv_path)
        capacitors = []
        
        for _, row in df.iterrows():
            capacitor = Capacitor(
                part_number=str(row['part_number']),
                manufacturer=str(row['manufacturer']),
                capacitance=float(row['capacitance']),
                voltage=float(row['voltage']),
                type=str(row['type']),
                esr=str(row['esr']),
                primary_use=str(row['primary_use']),
                temp_range=str(row['temp_range'])
            )
            capacitors.append(capacitor)
        
        return capacitors
    except Exception as e:
        print(f"Error loading Capacitor data from CSV: {e}")
        return get_fallback_capacitors()


def load_inductors_from_csv() -> List[Inductor]:
    """Load Inductor data from CSV file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, '..', 'assets', 'component_data', 'inductors.csv')
        
        if not os.path.exists(csv_path):
            print(f"Warning: Inductor CSV file not found at {csv_path}, using fallback data")
            return get_fallback_inductors()
        
        df = pd.read_csv(csv_path)
        inductors = []
        
        for _, row in df.iterrows():
            inductor = Inductor(
                part_number=str(row['part_number']),
                manufacturer=str(row['manufacturer']),
                inductance=float(row['inductance']),
                current=float(row['current']),
                dcr=float(row['dcr']),
                sat_current=float(row['sat_current']),
                package=str(row['package'])
            )
            inductors.append(inductor)
        
        return inductors
    except Exception as e:
        print(f"Error loading Inductor data from CSV: {e}")
        return get_fallback_inductors()


def get_fallback_mosfets() -> List[MOSFET]:
    """Fallback MOSFET data if CSV loading fails"""
    return [
        MOSFET("BSC016N06NS", "Infineon", 60, 150, 1.6, 44, "SuperSO8", "Mid-power buck, low loss", "96–98%"),
        MOSFET("CSD19505KCS", "Texas Instruments", 60, 80, 2.5, 37, "TO-220", "Classic synchronous buck", "95–97%"),
        MOSFET("IPB017N10N5", "Infineon", 100, 120, 1.7, 70, "D²PAK", "48V bus robotics converter", "96–97%"),
    ]


def get_fallback_capacitors() -> List[Capacitor]:
    """Fallback Capacitor data if CSV loading fails"""
    return [
        Capacitor("C3216X7R1H106K160AC", "TDK", 10, 50, "MLCC X7R", "~2-5", "HF ripple + local decoupling", "-55..125"),
        Capacitor("C3225X7R1E226M250AB", "TDK", 22, 25, "MLCC X7R", "~2-5", "HF ripple + bulk on 12V", "-55..125"),
    ]


def get_fallback_inductors() -> List[Inductor]:
    """Fallback Inductor data if CSV loading fails"""
    return [
        Inductor("SER2915H-472KL", "Coilcraft", 4700, 0.73, 1850, 0.95, "SER2915"),
        Inductor("SER2915H-103KL", "Coilcraft", 10000, 0.48, 4200, 0.62, "SER2915"),
    ]


# Load data from CSV files
MOSFET_LIBRARY: List[MOSFET] = load_mosfets_from_csv()
CAPACITOR_LIBRARY: List[Capacitor] = load_capacitors_from_csv()
INDUCTOR_LIBRARY: List[Inductor] = load_inductors_from_csv()


def reload_component_data():
    """Reload all component data from CSV files"""
    global MOSFET_LIBRARY, CAPACITOR_LIBRARY, INDUCTOR_LIBRARY
    MOSFET_LIBRARY = load_mosfets_from_csv()
    CAPACITOR_LIBRARY = load_capacitors_from_csv()
    INDUCTOR_LIBRARY = load_inductors_from_csv()
    print("Component data reloaded from CSV files")


def get_design_heuristics_path() -> str:
    """Get the path to the design heuristics folder"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '..', 'assets', 'design_heuristics')
