"""
Circuit Simulation Service
Orchestrates the complete simulation workflow from component calculation to results visualization
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from .ltspice_interface import get_simulator
from .netlist_generator import create_buck_simulation

class SimulationService:
    """
    Main service for handling circuit simulations
    """
    
    def __init__(self):
        self.simulator = get_simulator()
        self.current_simulation = None
        
    def run_buck_simulation(self, 
                           circuit_params: Dict[str, float],
                           calculated_components: Dict[str, float],
                           selected_components: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run complete Buck converter simulation
        
        Args:
            circuit_params: Input parameters (voltages, current, frequency)
            calculated_components: Calculated L, C values
            selected_components: Specific component selections
            
        Returns:
            Simulation results and status
        """
        
        try:
            # Generate netlist
            netlist = create_buck_simulation(
                input_voltage=circuit_params['input_voltage'],
                output_voltage=circuit_params['output_voltage'],
                load_current=circuit_params['load_current'],
                switching_frequency=circuit_params['switching_frequency'],
                calculated_components=calculated_components,
                selected_parts=selected_components
            )
            
            # Run simulation
            sim_results = self.simulator.run_simulation(netlist, "buck_converter")
            
            if sim_results['success']:
                # Process and analyze results
                analysis = self._analyze_simulation_results(
                    sim_results['results'],
                    circuit_params
                )
                
                return {
                    'success': True,
                    'netlist': netlist,
                    'raw_results': sim_results['results'],
                    'analysis': analysis,
                    'simulator_type': getattr(self.simulator, '__class__.__name__', 'Unknown')
                }
            else:
                return {
                    'success': False,
                    'error': sim_results.get('error', 'Unknown simulation error'),
                    'suggestion': sim_results.get('suggestion', 'Check component values'),
                    'netlist': netlist  # Include netlist for debugging
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Simulation service error: {str(e)}',
                'suggestion': 'Check input parameters and try again'
            }
    
    def _analyze_simulation_results(self, 
                                  results: Dict[str, Any],
                                  circuit_params: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze simulation results and extract key metrics
        """
        
        try:
            time = np.array(results['time'])
            v_out = np.array(results['voltages']['V(out)'])
            i_inductor = np.array(results['currents']['I(L1)'])
            
            # Find steady-state region (last 50% of simulation)
            steady_start = len(time) // 2
            v_out_steady = v_out[steady_start:]
            i_inductor_steady = i_inductor[steady_start:]
            
            # Calculate key metrics
            analysis = {
                'output_voltage': {
                    'average': np.mean(v_out_steady),
                    'ripple_pk_pk': np.max(v_out_steady) - np.min(v_out_steady),
                    'ripple_percent': (np.max(v_out_steady) - np.min(v_out_steady)) / np.mean(v_out_steady) * 100,
                    'target': circuit_params['output_voltage']
                },
                'inductor_current': {
                    'average': np.mean(i_inductor_steady),
                    'ripple_pk_pk': np.max(i_inductor_steady) - np.min(i_inductor_steady),
                    'peak': np.max(i_inductor_steady),
                    'target': circuit_params['load_current']
                },
                'performance': {},
                'settling_time': self._calculate_settling_time(time, v_out, circuit_params['output_voltage'])
            }
            
            # Calculate efficiency estimate (simplified)
            p_out = analysis['output_voltage']['average'] * analysis['inductor_current']['average']
            p_in = circuit_params['input_voltage'] * analysis['inductor_current']['average']  # Simplified
            analysis['performance']['efficiency_estimate'] = (p_out / p_in) * 100 if p_in > 0 else 0
            
            # Regulation performance
            voltage_error = abs(analysis['output_voltage']['average'] - circuit_params['output_voltage'])
            analysis['performance']['regulation_error'] = (voltage_error / circuit_params['output_voltage']) * 100
            
            # Performance rating
            analysis['performance']['rating'] = self._calculate_performance_rating(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'error': f'Analysis failed: {str(e)}',
                'raw_data_available': True
            }
    
    def _calculate_settling_time(self, time: np.ndarray, voltage: np.ndarray, target: float) -> float:
        """Calculate settling time to within 2% of target"""
        try:
            tolerance = 0.02 * target  # 2% tolerance
            
            # Find where voltage first enters the tolerance band
            within_tolerance = np.abs(voltage - target) <= tolerance
            
            # Find last time it was outside tolerance
            outside_indices = np.where(~within_tolerance)[0]
            
            if len(outside_indices) > 0:
                settling_index = outside_indices[-1] + 1
                if settling_index < len(time):
                    return time[settling_index] * 1000  # Return in ms
            
            return 0.0  # Already settled or no settling detectable
            
        except:
            return 0.0
    
    def _calculate_performance_rating(self, analysis: Dict[str, Any]) -> str:
        """Calculate overall performance rating"""
        try:
            ripple_percent = analysis['output_voltage']['ripple_percent']
            regulation_error = analysis['performance']['regulation_error']
            
            if ripple_percent < 1.0 and regulation_error < 1.0:
                return "Excellent"
            elif ripple_percent < 2.0 and regulation_error < 2.0:
                return "Good"
            elif ripple_percent < 5.0 and regulation_error < 5.0:
                return "Fair"
            else:
                return "Poor"
        except:
            return "Unknown"

def create_simulation_plots(results: Dict[str, Any]) -> go.Figure:
    """
    Create comprehensive plots of simulation results
    """
    
    raw_results = results['raw_results']
    time_ms = np.array(raw_results['time']) * 1000  # Convert to ms
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Output Voltage', 'Inductor Current', 'Switch Voltage'),
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    # Output voltage plot
    fig.add_trace(
        go.Scatter(
            x=time_ms,
            y=raw_results['voltages']['V(out)'],
            name='Output Voltage',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )
    
    # Target voltage line
    if 'analysis' in results and 'output_voltage' in results['analysis']:
        target_v = results['analysis']['output_voltage']['target']
        fig.add_hline(
            y=target_v,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Target: {target_v}V",
            row=1, col=1
        )
    
    # Inductor current plot
    fig.add_trace(
        go.Scatter(
            x=time_ms,
            y=raw_results['currents']['I(L1)'],
            name='Inductor Current',
            line=dict(color='green', width=2)
        ),
        row=2, col=1
    )
    
    # Switch voltage plot
    fig.add_trace(
        go.Scatter(
            x=time_ms,
            y=raw_results['voltages']['V(sw)'],
            name='Switch Voltage',
            line=dict(color='orange', width=2)
        ),
        row=3, col=1
    )
    
    # Update layout
    fig.update_layout(
        title="Buck Converter Simulation Results",
        height=600,
        showlegend=False
    )
    
    fig.update_xaxes(title_text="Time (ms)", row=3, col=1)
    fig.update_yaxes(title_text="Voltage (V)", row=1, col=1)
    fig.update_yaxes(title_text="Current (A)", row=2, col=1)
    fig.update_yaxes(title_text="Voltage (V)", row=3, col=1)
    
    return fig

# Streamlit UI integration functions
def show_simulation_button(circuit_params: Dict[str, float], 
                          calculated_components: Dict[str, float]) -> bool:
    """
    Show simulation button and handle click
    Returns True if simulation should be run
    """
    
    st.markdown("---")
    st.subheader("🔬 Circuit Simulation")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.info("✨ **Verify your design with SPICE simulation**")
        st.write("• Analyze startup behavior")
        st.write("• Check output ripple")
        st.write("• Validate component choices")
    
    with col2:
        simulate_clicked = st.button(
            "🚀 Simulate Circuit",
            type="primary",
            use_container_width=True,
            help="Run LTspice simulation with calculated components"
        )
    
    with col3:
        # Show simulation parameters
        st.write("**Simulation Setup:**")
        st.write(f"• Duration: 2ms")
        st.write(f"• Time step: 1µs")
        st.write(f"• Analysis: Transient")
    
    return simulate_clicked

def run_and_display_simulation(circuit_params: Dict[str, float],
                             calculated_components: Dict[str, float]) -> None:
    """
    Run simulation and display results in Streamlit
    """
    
    # Initialize simulation service
    sim_service = SimulationService()
    
    # Show progress
    with st.spinner("🔄 Running circuit simulation..."):
        # Add progress bar
        progress_bar = st.progress(0)
        progress_bar.progress(25, text="Generating netlist...")
        
        # Run simulation
        results = sim_service.run_buck_simulation(
            circuit_params,
            calculated_components
        )
        
        progress_bar.progress(75, text="Analyzing results...")
        progress_bar.progress(100, text="Complete!")
        progress_bar.empty()
    
    # Display results
    if results['success']:
        st.success("✅ Simulation completed successfully!")
        
        # Show key metrics
        if 'analysis' in results:
            analysis = results['analysis']
            
            # Metrics columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Output Voltage",
                    f"{analysis['output_voltage']['average']:.3f}V",
                    f"{analysis['performance']['regulation_error']:.2f}% error"
                )
            
            with col2:
                st.metric(
                    "Voltage Ripple",
                    f"{analysis['output_voltage']['ripple_pk_pk']*1000:.1f}mV",
                    f"{analysis['output_voltage']['ripple_percent']:.2f}%"
                )
            
            with col3:
                st.metric(
                    "Settling Time",
                    f"{analysis['settling_time']:.2f}ms",
                    None
                )
            
            with col4:
                rating = analysis['performance']['rating']
                rating_color = {
                    'Excellent': '🟢',
                    'Good': '🟡', 
                    'Fair': '🟠',
                    'Poor': '🔴'
                }.get(rating, '⚪')
                
                st.metric(
                    "Performance",
                    f"{rating_color} {rating}",
                    None
                )
        
        # Create and show plots
        fig = create_simulation_plots(results)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show netlist in expander
        with st.expander("📄 View Generated Netlist"):
            st.code(results['netlist'], language='text')
        
    else:
        st.error(f"❌ Simulation failed: {results['error']}")
        if 'suggestion' in results:
            st.info(f"💡 {results['suggestion']}")
        
        # Show netlist for debugging
        if 'netlist' in results:
            with st.expander("🔍 Debug: View Generated Netlist"):
                st.code(results['netlist'], language='text')