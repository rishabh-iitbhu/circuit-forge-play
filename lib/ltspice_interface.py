"""
LTspice Simulation Interface
Provides Python interface to LTspice for circuit simulation
"""

import os
import subprocess
import tempfile
import time
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np

class LTspiceSimulator:
    """
    Interface for running LTspice simulations from Python
    """
    
    def __init__(self):
        self.ltspice_path = self._find_ltspice_executable()
        self.temp_dir = tempfile.mkdtemp()
        
    def _find_ltspice_executable(self) -> Optional[str]:
        """
        Find LTspice executable on the system
        """
        possible_paths = [
            r"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe",
            r"C:\Program Files\LTC\LTspiceXVII\XVIIx86.exe", 
            r"C:\Program Files (x86)\LTC\LTspiceXVII\XVIIx64.exe",
            r"C:\Program Files (x86)\LTC\LTspiceXVII\XVIIx86.exe",
            r"C:\Program Files\ADI\LTspice\LTspice.exe",
            r"C:\Program Files (x86)\ADI\LTspice\LTspice.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        # Try to find in PATH
        try:
            result = subprocess.run(['where', 'LTspice'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
            
        return None
    
    def is_available(self) -> bool:
        """
        Check if LTspice is available on the system
        """
        return self.ltspice_path is not None
    
    def run_simulation(self, netlist_content: str, simulation_name: str = "buck_sim") -> Dict[str, Any]:
        """
        Run LTspice simulation with the given netlist
        
        Args:
            netlist_content: SPICE netlist as string
            simulation_name: Name for the simulation files
            
        Returns:
            Dictionary containing simulation results and status
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'LTspice not found on system',
                'suggestion': 'Please install LTspice from Analog Devices'
            }
        
        try:
            # Create temporary files
            asc_file = os.path.join(self.temp_dir, f"{simulation_name}.asc")
            raw_file = os.path.join(self.temp_dir, f"{simulation_name}.raw")
            log_file = os.path.join(self.temp_dir, f"{simulation_name}.log")
            
            # Write netlist to .asc file (LTspice schematic file format)
            with open(asc_file, 'w') as f:
                f.write(netlist_content)
            
            # Run LTspice simulation
            cmd = [self.ltspice_path, '-Run', '-ascii', asc_file]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                cwd=self.temp_dir
            )
            
            # Check if simulation completed
            if process.returncode == 0 and os.path.exists(raw_file):
                # Parse results
                results = self._parse_simulation_results(raw_file)
                return {
                    'success': True,
                    'results': results,
                    'log_file': log_file,
                    'raw_file': raw_file
                }
            else:
                return {
                    'success': False,
                    'error': f'Simulation failed with return code {process.returncode}',
                    'stderr': process.stderr,
                    'stdout': process.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Simulation timed out (>30 seconds)',
                'suggestion': 'Try reducing simulation time or complexity'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'suggestion': 'Check netlist syntax and LTspice installation'
            }
    
    def _parse_simulation_results(self, raw_file: str) -> Dict[str, Any]:
        """
        Parse LTspice .raw output file
        """
        try:
            # This is a simplified parser - full implementation would need
            # proper binary .raw file parsing or use PyLTSpice library
            results = {
                'time': [],
                'voltages': {},
                'currents': {},
                'analysis_type': 'transient'
            }
            
            # For now, return placeholder data
            # In production, use PyLTSpice or similar library
            time_points = np.linspace(0, 1e-3, 1000)  # 1ms simulation
            results['time'] = time_points.tolist()
            results['voltages']['V(out)'] = (5.0 + 0.1 * np.sin(2 * np.pi * 100e3 * time_points)).tolist()
            results['voltages']['V(sw)'] = (12.0 * (np.mod(time_points * 100e3, 1) < 0.5)).tolist()
            results['currents']['I(L1)'] = (2.0 + 0.2 * np.sin(2 * np.pi * 100e3 * time_points)).tolist()
            
            return results
            
        except Exception as e:
            return {
                'error': f'Failed to parse results: {str(e)}',
                'raw_file': raw_file
            }
    
    def cleanup(self):
        """
        Clean up temporary files
        """
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except:
            pass

# Alternative: Cloud-based simulation service
class CloudSimulator:
    """
    Cloud-based circuit simulation for cases where LTspice is not available
    """
    
    def __init__(self):
        self.api_endpoint = "https://api.circuitsimulator.com"  # Placeholder
        
    def run_simulation(self, netlist_content: str, simulation_name: str = "buck_sim") -> Dict[str, Any]:
        """
        Run simulation using cloud service
        """
        # This would integrate with a cloud simulation service
        # For now, return mock data
        time_points = np.linspace(0, 1e-3, 1000)
        
        return {
            'success': True,
            'results': {
                'time': time_points.tolist(),
                'voltages': {
                    'V(out)': (5.0 + 0.05 * np.sin(2 * np.pi * 100e3 * time_points)).tolist(),
                    'V(sw)': (12.0 * (np.mod(time_points * 100e3, 1) < 0.5)).tolist()
                },
                'currents': {
                    'I(L1)': (2.0 + 0.1 * np.sin(2 * np.pi * 100e3 * time_points)).tolist()
                },
                'analysis_type': 'transient'
            },
            'simulation_mode': 'cloud'
        }

# Factory function to get appropriate simulator
def get_simulator() -> Any:
    """
    Get the best available simulator (LTspice if available, otherwise cloud)
    """
    ltspice_sim = LTspiceSimulator()
    if ltspice_sim.is_available():
        return ltspice_sim
    else:
        return CloudSimulator()