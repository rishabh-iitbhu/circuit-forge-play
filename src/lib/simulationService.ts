import { SimulationParameters, SimulationResults, SimulationData } from '@/types/simulation';

export class SimulationService {
  /**
   * Run LTSpice simulation with the provided netlist
   * For now, this generates realistic simulation data
   * TODO: Integrate with actual LTSpice API/backend service
   */
  async runSimulation(params: SimulationParameters, netlist: string): Promise<SimulationResults> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Generate simulation data points
    const numPoints = 1000;
    const data = this.generateSimulationData(params, numPoints);
    
    // Calculate analysis metrics
    const analysis = this.analyzeResults(data, params);

    return {
      parameters: params,
      data,
      analysis,
      netlist,
    };
  }

  private generateSimulationData(params: SimulationParameters, numPoints: number): SimulationData {
    const { inputs } = params;
    const timeStep = 0.02 / numPoints; // 20ms window (one AC cycle at 50Hz)
    
    const data: SimulationData = {
      time: [],
      inputVoltage: [],
      outputVoltage: [],
      inputCurrent: [],
      outputCurrent: [],
      efficiency: [],
      switchingNode: [],
    };

    for (let i = 0; i < numPoints; i++) {
      const t = i * timeStep;
      data.time.push(t * 1000); // Convert to ms

      // Input voltage (rectified sine wave)
      const vinRaw = inputs.v_in_max * 1.414 * Math.abs(Math.sin(2 * Math.PI * inputs.line_freq_min * t));
      data.inputVoltage.push(vinRaw);

      // Output voltage with small ripple
      const voutRipple = inputs.v_ripple_max * Math.sin(2 * Math.PI * inputs.switching_freq * t);
      data.outputVoltage.push(inputs.v_out_min + voutRipple);

      // Input current (PFC tries to follow voltage waveform)
      const iin = (inputs.p_out_max / inputs.v_in_min) * Math.abs(Math.sin(2 * Math.PI * inputs.line_freq_min * t));
      const iinRipple = iin * 0.2 * Math.sin(2 * Math.PI * inputs.switching_freq * t);
      data.inputCurrent.push(iin + iinRipple);

      // Output current (relatively constant)
      const iout = inputs.p_out_max / inputs.v_out_min;
      const ioutRipple = iout * 0.05 * Math.sin(2 * Math.PI * inputs.switching_freq * t);
      data.outputCurrent.push(iout + ioutRipple);

      // Efficiency
      const pIn = vinRaw * (iin + iinRipple);
      const pOut = (inputs.v_out_min + voutRipple) * (iout + ioutRipple);
      data.efficiency.push(pIn > 0 ? (pOut / pIn) * 100 : 0);

      // Switching node (square wave)
      const duty = inputs.v_out_min / (inputs.v_out_min + vinRaw);
      const switchPhase = (t * inputs.switching_freq) % 1;
      data.switchingNode.push(switchPhase < duty ? inputs.v_out_min : 0);
    }

    return data;
  }

  private analyzeResults(data: SimulationData, params: SimulationParameters) {
    const avgEfficiency = data.efficiency.reduce((a, b) => a + b, 0) / data.efficiency.length;
    const peakCurrent = Math.max(...data.inputCurrent);
    
    const voutMax = Math.max(...data.outputVoltage);
    const voutMin = Math.min(...data.outputVoltage);
    const voltageRipple = voutMax - voutMin;
    
    const iinMax = Math.max(...data.inputCurrent);
    const iinMin = Math.min(...data.inputCurrent);
    const currentRipple = iinMax - iinMin;

    // Calculate power factor (simplified)
    const powerFactor = avgEfficiency > 90 ? 0.99 : 0.95;
    
    // Calculate THD (Total Harmonic Distortion) - simplified
    const thd = avgEfficiency > 90 ? 3.5 : 5.2;

    return {
      avgEfficiency: parseFloat(avgEfficiency.toFixed(2)),
      peakCurrent: parseFloat(peakCurrent.toFixed(3)),
      voltageRipple: parseFloat(voltageRipple.toFixed(3)),
      currentRipple: parseFloat(currentRipple.toFixed(3)),
      powerFactor: parseFloat(powerFactor.toFixed(3)),
      thd: parseFloat(thd.toFixed(2)),
    };
  }
}
