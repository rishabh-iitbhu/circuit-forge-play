import { PFCInputs, PFCResults, BuckInputs, BuckResults } from './calculations';

export interface CircuitComponents {
  mosfet: any;
  capacitor: any;
  inductor: any;
}

// Standard PFC Boost Converter Topology
export function generatePFCBoostNetlist(
  inputs: PFCInputs,
  results: PFCResults,
  components: CircuitComponents
): string {
  const { v_in_min, v_in_max, v_out_min, switching_freq, line_freq_min, p_out_max } = inputs;
  const { inductance, capacitance } = results;
  const { mosfet, capacitor, inductor } = components;

  const L_value = `${(inductance * 1e6).toFixed(2)}u`;
  const C_value = `${(capacitance * 1e6).toFixed(2)}u`;
  const freq_khz = switching_freq / 1000;
  const line_freq = line_freq_min;
  const load_resistance = (v_out_min * v_out_min) / p_out_max;

  return `* PFC Boost Converter - Standard Topology
* Components: ${mosfet?.part_number || 'Generic'}, ${capacitor?.part_number || 'Generic'}, ${inductor?.part_number || 'Generic'}

* AC Input Source (rectified to DC by bridge)
V1 N001 0 SINE(0 ${v_in_max * 1.414} ${line_freq})

* Bridge Rectifier
D1 N001 N002 D1N4148
D2 0 N002 D1N4148
D3 N001 0 D1N4148
D4 N003 N002 D1N4148

* Boost Inductor
L1 N002 N003 ${L_value}
.ic I(L1)=0

* MOSFET Switch (Low-side)
M1 N003 N004 0 0 MOSFET_MODEL
.model MOSFET_MODEL NMOS(Rds=${mosfet?.rds_on || 0.18} Vt=3 Cgs=${mosfet?.qg || 50}n)

* Gate Drive PWM Signal
V2 N004 0 PULSE(0 12 0 50n 50n ${1/(2*switching_freq)} ${1/switching_freq})

* Boost Diode
D5 N003 N005 MUR460
.model MUR460 D(Is=1e-12 Rs=0.05)

* Output Capacitor
C1 N005 0 ${C_value} Rser=${capacitor?.esr || 0.05}
.ic V(N005)=${v_out_min}

* Load Resistor
R1 N005 0 ${load_resistance}

* Simulation Commands
.tran 0 ${10/line_freq} ${5/line_freq} ${1/(switching_freq*100)}
.meas TRAN Vout_avg AVG V(N005)
.meas TRAN Vout_ripple PP V(N005)
.meas TRAN IL_peak MAX I(L1)
.meas TRAN Iin_rms RMS I(V1)
.meas TRAN Pin AVG V(N001)*I(V1)
.meas TRAN Pout AVG V(N005)*I(R1)
.meas TRAN efficiency PARAM Pout/Pin

.backanno
.end
`;
}

// Standard Buck Converter Topology
export function generateBuckNetlist(
  inputs: BuckInputs,
  results: BuckResults,
  components: CircuitComponents
): string {
  const { v_in_min, v_out_max, switching_freq, p_out_max } = inputs;
  const { inductance, output_capacitance, duty_cycle_max } = results;
  const load_current = p_out_max / v_out_max;
  const { mosfet, capacitor, inductor } = components;

  const L_value = `${(inductance * 1e6).toFixed(2)}u`;
  const C_value = `${(output_capacitance * 1e6).toFixed(2)}u`;
  const load_resistance = v_out_max / load_current;

  return `* Buck Converter - Standard Topology
* Components: ${mosfet?.part_number || 'Generic'}, ${capacitor?.part_number || 'Generic'}, ${inductor?.part_number || 'Generic'}

* DC Input Source
V1 N001 0 DC ${v_in_min}

* High-side MOSFET
M1 N001 N002 N003 N001 MOSFET_MODEL
.model MOSFET_MODEL NMOS(Rds=${mosfet?.rds_on || 0.18} Vt=3 Cgs=${mosfet?.qg || 50}n)

* Gate Drive PWM Signal
V2 N002 0 PULSE(0 12 0 50n 50n ${duty_cycle_max/switching_freq} ${1/switching_freq})

* Buck Inductor
L1 N003 N004 ${L_value}
.ic I(L1)=${load_current}

* Freewheeling Diode
D1 0 N003 MUR460
.model MUR460 D(Is=1e-12 Rs=0.05)

* Output Capacitor
C1 N004 0 ${C_value} Rser=${capacitor?.esr || 0.05}
.ic V(N004)=${v_out_max}

* Load Resistor
R1 N004 0 ${load_resistance}

* Simulation Commands
.tran 0 ${10/switching_freq} ${5/switching_freq} ${1/(switching_freq*100)}
.meas TRAN Vout_avg AVG V(N004)
.meas TRAN Vout_ripple PP V(N004)
.meas TRAN IL_avg AVG I(L1)
.meas TRAN IL_ripple PP I(L1)
.meas TRAN Pin AVG V(N001)*I(V1)
.meas TRAN Pout AVG V(N004)*I(R1)
.meas TRAN efficiency PARAM Pout/Pin

.backanno
.end
`;
}
