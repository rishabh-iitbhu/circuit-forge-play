"""
Circuit calculation functions for PFC and Buck converter designs
"""

from dataclasses import dataclass
from typing import Dict, Any
import math

@dataclass
class PFCInputs:
    """Input parameters for PFC circuit design"""
    v_in_min: float
    v_in_max: float
    v_out_min: float
    v_out_max: float
    p_out_max: float
    efficiency: float
    switching_freq: float
    line_freq_min: float
    v_ripple_max: float

@dataclass
class BuckInputs:
    """Input parameters for Buck converter design"""
    v_in_min: float
    v_in_max: float
    v_out_min: float
    v_out_max: float
    p_out_max: float
    efficiency: float
    switching_freq: float
    v_ripple_max: float
    v_in_ripple: float
    i_out_ripple: float
    v_overshoot: float
    v_undershoot: float
    i_loadstep: float

@dataclass
class PFCResults:
    """Calculation results for PFC circuit"""
    inductance: float
    capacitance: float
    ripple_current: float

@dataclass
class BuckResults:
    """Calculation results for Buck converter"""
    inductance: float
    output_capacitance: float
    input_capacitance: float
    duty_cycle_max: float


class CircuitCalculator:
    """Calculator for circuit component values"""
    
    def calculate_pfc(self, inputs: PFCInputs) -> PFCResults:
        """
        Calculate PFC circuit component values
        
        Args:
            inputs: PFC input parameters
            
        Returns:
            PFCResults with calculated component values
        """
        # Calculate input power
        p_in_max = inputs.p_out_max / inputs.efficiency
        
        # Calculate maximum input current
        i_in_max = p_in_max / inputs.v_in_min
        
        # Calculate inductance (typical formula for PFC)
        # L = (V_in * (V_out - V_in)) / (V_out * f_s * ΔI)
        delta_i = i_in_max * 0.2  # 20% ripple current
        inductance = (inputs.v_in_min * (inputs.v_out_min - inputs.v_in_min)) / (
            inputs.v_out_min * inputs.switching_freq * delta_i
        )
        
        # Calculate output capacitance
        # C = (P_out) / (2 * π * f_line * V_out * ΔV)
        capacitance = inputs.p_out_max / (
            2 * math.pi * inputs.line_freq_min * inputs.v_out_min * inputs.v_ripple_max
        )
        
        # Calculate ripple current
        ripple_current = delta_i
        
        return PFCResults(
            inductance=inductance,
            capacitance=capacitance,
            ripple_current=ripple_current
        )
    
    def calculate_buck(self, inputs: BuckInputs) -> BuckResults:
        """
        Calculate Buck converter component values
        
        Args:
            inputs: Buck converter input parameters
            
        Returns:
            BuckResults with calculated component values
        """
        # Calculate duty cycle
        duty_cycle_max = inputs.v_out_max / inputs.v_in_max
        
        # Calculate output current
        i_out_max = inputs.p_out_max / inputs.v_out_min
        
        # Calculate inductance
        # L = (V_out * (1 - D)) / (f_s * ΔI)
        inductance = (inputs.v_out_max * (1 - duty_cycle_max)) / (
            inputs.switching_freq * inputs.i_out_ripple
        )
        
        # Calculate output capacitance
        # C_out = ΔI / (8 * f_s * ΔV)
        output_capacitance = inputs.i_out_ripple / (
            8 * inputs.switching_freq * inputs.v_ripple_max
        )
        
        # Calculate input capacitance
        # C_in = (I_out * D) / (f_s * ΔV_in)
        input_capacitance = (i_out_max * duty_cycle_max) / (
            inputs.switching_freq * inputs.v_in_ripple
        )
        
        return BuckResults(
            inductance=inductance,
            output_capacitance=output_capacitance,
            input_capacitance=input_capacitance,
            duty_cycle_max=duty_cycle_max
        )


def validate_inputs(inputs: Dict[str, Any]) -> bool:
    """
    Validate that all input values are positive numbers
    
    Args:
        inputs: Dictionary of input values
        
    Returns:
        True if all values are valid, False otherwise
    """
    return all(
        isinstance(value, (int, float)) and value > 0
        for value in inputs.values()
    )
