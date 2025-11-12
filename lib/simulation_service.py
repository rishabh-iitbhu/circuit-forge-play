"""
Circuit Simulation Service
Orchestrates the complete simulation workflow from component calculation to results visualization
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple
import numpy as np
import sys
import os
import subprocess

def install_plotly():
    """
    Attempt to install plotly in the current environment
    """
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'plotly'])
        return True
    except Exception:
        return False

def check_plotly_availability():
    """
    Comprehensive plotly availability check with detailed diagnostics
    """
    try:
        # Add current directory to path to ensure proper imports
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Try importing plotly
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Test basic functionality
        test_fig = go.Figure()
        test_fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]))
        
        return True, go, make_subplots, None
        
    except ImportError as e:
        return False, None, None, f"Import error: {str(e)}"
    except Exception as e:
        return False, None, None, f"Plotly test failed: {str(e)}"

# Initial plotly check
PLOTLY_AVAILABLE, go, make_subplots, plotly_error = check_plotly_availability()

from .ltspice_interface import get_simulator
from .netlist_generator import create_buck_simulation

def validate_simulation_inputs(circuit_params: Dict[str, float], calculated_components: Dict[str, float]) -> Dict[str, Any]:
    """
    Validate simulation inputs before running
    """
    try:
        # Check circuit parameters
        required_circuit_params = ['input_voltage', 'output_voltage', 'load_current', 'switching_frequency']
        for param in required_circuit_params:
            if param not in circuit_params or circuit_params[param] <= 0:
                return {'valid': False, 'error': f'Invalid circuit parameter: {param}'}
        
        # Check calculated components
        required_components = ['inductance', 'output_capacitance']
        for component in required_components:
            if component not in calculated_components or calculated_components[component] <= 0:
                return {'valid': False, 'error': f'Invalid component value: {component}'}
        
        # Sanity checks
        if circuit_params['output_voltage'] >= circuit_params['input_voltage']:
            return {'valid': False, 'error': 'Output voltage must be less than input voltage for Buck converter'}
        
        if circuit_params['switching_frequency'] < 1000 or circuit_params['switching_frequency'] > 10e6:
            return {'valid': False, 'error': 'Switching frequency must be between 1kHz and 10MHz'}
        
        return {'valid': True, 'error': None}
        
    except Exception as e:
        return {'valid': False, 'error': f'Validation error: {str(e)}'}

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

def create_simulation_plots_v2(results: Dict[str, Any]) -> Any:
    """
    Create comprehensive plots of simulation results with robust error handling
    """
    
    # Validate input data first
    if not results or 'raw_results' not in results:
        st.error("❌ No simulation data available for plotting")
        return None
    
    raw_results = results['raw_results']
    
    # Check if we have the required data
    required_keys = ['time', 'voltages', 'currents']
    missing_keys = [key for key in required_keys if key not in raw_results]
    if missing_keys:
        st.error(f"❌ Missing simulation data: {', '.join(missing_keys)}")
        return None
    
    st.info("🔄 Loading visualization system...")
    
    # Runtime plotly availability check with detailed diagnostics
    plotly_available, go_runtime, make_subplots_runtime, error_msg = check_plotly_availability()
    
    if not plotly_available:
        st.error("❌ Plotly visualization unavailable")
        st.code(f"Error: {error_msg}")
        
        # Offer auto-installation
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("� Try Auto-Install Plotly", type="primary"):
                with st.spinner("Installing plotly..."):
                    if install_plotly():
                        st.success("✅ Plotly installed! Please refresh the page.")
                        st.balloons()
                    else:
                        st.error("❌ Auto-installation failed. Please install manually.")
        
        with col2:
            st.info("💡 **Manual install:**\n`pip install plotly`")
        
        # Show alternative text-based results
        st.subheader("📊 Text-Based Results Summary")
        try:
            time_data = raw_results['time']
            voltage_data = raw_results['voltages'].get('V(out)', [])
            if len(voltage_data) > 0:
                avg_voltage = np.mean(voltage_data)
                min_voltage = np.min(voltage_data)
                max_voltage = np.max(voltage_data)
                ripple = max_voltage - min_voltage
                st.write(f"• **Average Output Voltage**: {avg_voltage:.3f}V")
                st.write(f"• **Voltage Range**: {min_voltage:.3f}V to {max_voltage:.3f}V")
                st.write(f"• **Voltage Ripple**: {ripple*1000:.1f}mV")
                st.write(f"• **Simulation Duration**: {max(time_data)*1000:.2f}ms")
                st.write(f"• **Data Points**: {len(voltage_data)} samples")
        except Exception as e:
            st.write("Unable to extract summary data")
        
        return None
    
    # Success message
    st.success("✅ Plotly loaded successfully - Interactive charts available!")
    time_ms = np.array(raw_results['time']) * 1000  # Convert to ms
    
    # Create subplots
    fig = make_subplots_runtime(
        rows=3, cols=1,
        subplot_titles=('Output Voltage', 'Inductor Current', 'Switch Voltage'),
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    # Output voltage plot
    fig.add_trace(
        go_runtime.Scatter(
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
        go_runtime.Scatter(
            x=time_ms,
            y=raw_results['currents']['I(L1)'],
            name='Inductor Current',
            line=dict(color='green', width=2)
        ),
        row=2, col=1
    )
    
    # Switch voltage plot
    fig.add_trace(
        go_runtime.Scatter(
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
    Run simulation and display results in Streamlit with comprehensive error handling
    """
    
    # Clear Streamlit cache to ensure fresh imports
    try:
        st.cache_data.clear()
    except:
        pass  # In case cache_data doesn't exist in older versions
    
    # Input validation
    st.info("🔍 Validating simulation parameters...")
    validation = validate_simulation_inputs(circuit_params, calculated_components)
    if not validation['valid']:
        st.error(f"❌ **Validation Failed**: {validation['error']}")
        return
    
    st.success("✅ Parameters validated successfully")
    
    # Add debugging info
    with st.expander("🔧 Debug Info - Simulation Parameters"):
        st.json({
            "Circuit Parameters": circuit_params,
            "Calculated Components": calculated_components,
            "Python Executable": sys.executable
        })
    
    # Add a rerun button to force cache clearing
    if st.button("🔄 Force Refresh (if plots not showing)", type="secondary"):
        st.rerun()
    
    # Initialize simulation service
    try:
        sim_service = SimulationService()
    except Exception as e:
        st.error(f"❌ **Simulation Service Error**: {str(e)}")
        return
    
    # Show progress
    with st.spinner("🔄 Running circuit simulation..."):
        # Add progress bar
        progress_bar = st.progress(0)
        progress_bar.progress(25, text="Generating netlist...")
        
        try:
            # Run simulation
            results = sim_service.run_buck_simulation(
                circuit_params,
                calculated_components
            )
            
            progress_bar.progress(75, text="Analyzing results...")
            
            # Validate results
            if not results or not isinstance(results, dict):
                raise ValueError("Invalid simulation results returned")
            
            progress_bar.progress(100, text="Complete!")
            progress_bar.empty()
            
        except Exception as e:
            progress_bar.empty()
            st.error(f"❌ **Simulation Failed**: {str(e)}")
            st.info("💡 **Troubleshooting:**")
            st.write("• Check your input parameters")
            st.write("• Ensure component values are reasonable")
            st.write("• Try different switching frequency")
            
            # Show debug information
            with st.expander("🔍 Error Details"):
                st.code(f"Error: {str(e)}")
                st.write("**Circuit Parameters:**")
                st.json(circuit_params)
                st.write("**Component Values:**")
                st.json(calculated_components)
            
            return
    
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
        fig = create_simulation_plots_v2(results)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("📊 Visualization requires plotly library. Simulation data is available in the analysis metrics above.")
        
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