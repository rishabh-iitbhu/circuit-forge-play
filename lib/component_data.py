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
    """Output Capacitor component specification"""
    part_number: str
    manufacturer: str
    capacitance: float  # µF
    voltage: float  # V
    type: str
    esr: str  # mΩ
    primary_use: str
    temp_range: str

@dataclass
class InputCapacitor:
    """Input Capacitor component specification with ripple current handling"""
    part_number: str
    manufacturer: str
    category: str  # MLCC, Polymer, Electrolytic, Film
    dielectric: str  # X7R, X5R, Conductive Polymer, etc.
    capacitance: float  # µF
    voltage: float  # V
    esr: float  # mΩ
    esl: float  # nH (Equivalent Series Inductance)
    ripple_rating: float  # A (if available)
    lifetime: float  # hours (if available)
    package: str
    cost: float  # USD (if available)
    availability: str
    notes: str

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
    shielded: bool = False  # New field
    core_material: str = ""  # New field
    temp_range: str = ""  # New field


def load_mosfets_from_csv() -> List[MOSFET]:
    """Load MOSFETs from CSV file with robust path handling"""
    try:
        # Multiple path resolution strategies for different environments
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try different path combinations
        possible_paths = [
            os.path.join(current_dir, '..', 'assets', 'component_data', 'mosfets.csv'),
            os.path.join(os.getcwd(), 'assets', 'component_data', 'mosfets.csv'),
            os.path.join(current_dir, '..', '..', 'assets', 'component_data', 'mosfets.csv'),
            'assets/component_data/mosfets.csv'  # Relative path for cloud deployment
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            print(f"Warning: MOSFET CSV file not found in any of these locations: {possible_paths}")
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
    """Load Capacitor data from CSV file with robust path handling"""
    try:
        # Multiple path resolution strategies for different environments
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try different path combinations for output capacitors
        possible_paths = [
            os.path.join(current_dir, '..', 'assets', 'component_data', 'output_capacitors.csv'),
            os.path.join(os.getcwd(), 'assets', 'component_data', 'output_capacitors.csv'),
            os.path.join(current_dir, '..', '..', 'assets', 'component_data', 'output_capacitors.csv'),
            'assets/component_data/output_capacitors.csv'  # Relative path for cloud deployment
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            print(f"Warning: Capacitor CSV file not found in any of these locations: {possible_paths}")
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


def load_input_capacitors_from_csv() -> List[InputCapacitor]:
    """Load Input Capacitor data from CSV file with robust path handling"""
    try:
        # Multiple path resolution strategies for different environments
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try different path combinations for input capacitors
        possible_paths = [
            os.path.join(current_dir, '..', 'assets', 'component_data', 'input_capacitors.csv'),
            os.path.join(os.getcwd(), 'assets', 'component_data', 'input_capacitors.csv'),
            os.path.join(current_dir, '..', '..', 'assets', 'component_data', 'input_capacitors.csv'),
            'assets/component_data/input_capacitors.csv'  # Relative path for cloud deployment
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            print(f"Warning: Input Capacitor CSV file not found in any of these locations: {possible_paths}")
            return []  # Return empty list if file not found
        
        df = pd.read_csv(csv_path)
        input_capacitors = []
        
        for _, row in df.iterrows():
            input_capacitor = InputCapacitor(
                part_number=str(row['part_number']),
                manufacturer=str(row['manufacturer']),
                category=str(row['category']),
                dielectric=str(row['dielectric']),
                capacitance=float(row['rated_capacitance_uf']),
                voltage=float(row['rated_voltage_v']),
                esr=float(row['esr_mohm']) if pd.notna(row['esr_mohm']) else 0.0,
                esl=float(row['esl_nh']) if pd.notna(row['esl_nh']) else 0.0,
                ripple_rating=float(row['ripple_rating_a']) if pd.notna(row['ripple_rating_a']) else 0.0,
                lifetime=float(row['lifetime_h']) if pd.notna(row['lifetime_h']) else 0.0,
                package=str(row['package']),
                cost=float(row['cost_usd']) if pd.notna(row['cost_usd']) else 0.0,
                availability=str(row['availability']),
                notes=str(row['notes'])
            )
            input_capacitors.append(input_capacitor)
        
        return input_capacitors
    except Exception as e:
        print(f"Error loading Input Capacitor data from CSV: {e}")
        return []


def load_inductors_from_csv() -> List[Inductor]:
    """Load Inductor data from CSV file with robust path handling"""
    try:
        # Multiple path resolution strategies for different environments
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try different path combinations
        possible_paths = [
            os.path.join(current_dir, '..', 'assets', 'component_data', 'inductors.csv'),
            os.path.join(os.getcwd(), 'assets', 'component_data', 'inductors.csv'),
            os.path.join(current_dir, '..', '..', 'assets', 'component_data', 'inductors.csv'),
            'assets/component_data/inductors.csv'  # Relative path for cloud deployment
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            print(f"Warning: Inductor CSV file not found in any of these locations: {possible_paths}")
            return get_fallback_inductors()
        
        df = pd.read_csv(csv_path)
        inductors = []
        
        for _, row in df.iterrows():
            # Handle both old and new CSV format - check for new format columns first
            if 'l_nom_uh' in df.columns:
                # New PowerCrux format
                inductor = Inductor(
                    part_number=str(row['part_number']),
                    manufacturer=str(row['manufacturer']),
                    inductance=float(row['l_nom_uh']),
                    current=float(row['i_rated_a']),
                    dcr=float(row['dcr_mohm_max']),
                    sat_current=float(row['i_sat_a']),
                    package=str(row['package']),
                    shielded=str(row['shielded']).lower() == 'true' if 'shielded' in df.columns else False,
                    core_material=str(row['core_material']) if 'core_material' in df.columns else "",
                    temp_range=str(row['operating_temp_c']) if 'operating_temp_c' in df.columns else ""
                )
            else:
                # Old format
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
CAPACITOR_LIBRARY: List[Capacitor] = load_capacitors_from_csv()  # Output capacitors
INPUT_CAPACITOR_LIBRARY: List[InputCapacitor] = load_input_capacitors_from_csv()
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
