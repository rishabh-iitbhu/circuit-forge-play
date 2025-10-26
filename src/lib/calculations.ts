export interface PFCInputs {
  v_in_min: number;
  v_in_max: number;
  v_out_min: number;
  v_out_max: number;
  p_out_max: number;
  efficiency: number;
  switching_freq: number;
  line_freq_min: number;
  v_ripple_max: number;
}

export interface BuckInputs {
  v_in_min: number;
  v_in_max: number;
  v_out_min: number;
  v_out_max: number;
  p_out_max: number;
  efficiency: number;
  switching_freq: number;
  v_ripple_max: number;
  v_in_ripple: number;
  i_out_ripple: number;
  v_overshoot: number;
  v_undershoot: number;
  i_loadstep: number;
}

export interface PFCResults {
  inductance: number;
  capacitance: number;
  ripple_current: number;
}

export interface BuckResults {
  inductance: number;
  output_capacitance: number;
  input_capacitance: number;
  duty_cycle_max: number;
}

export class CircuitCalculator {
  calculatePFC(inputs: PFCInputs): PFCResults {
    const {
      v_in_min,
      v_out_min,
      p_out_max,
      efficiency,
      switching_freq,
      line_freq_min,
      v_ripple_max,
    } = inputs;

    // Calculate input power
    const p_in_max = p_out_max / efficiency;

    // Calculate maximum input current
    const i_in_max = p_in_max / v_in_min;

    // Calculate inductance (typical formula for PFC)
    // L = (V_in * (V_out - V_in)) / (V_out * f_s * ΔI)
    const delta_i = i_in_max * 0.2; // 20% ripple current
    const inductance = (v_in_min * (v_out_min - v_in_min)) / (v_out_min * switching_freq * delta_i);

    // Calculate output capacitance
    // C = (P_out) / (2 * π * f_line * V_out * ΔV)
    const capacitance = p_out_max / (2 * Math.PI * line_freq_min * v_out_min * v_ripple_max);

    // Calculate ripple current
    const ripple_current = delta_i;

    return {
      inductance,
      capacitance,
      ripple_current,
    };
  }

  calculateBuck(inputs: BuckInputs): BuckResults {
    const {
      v_in_max,
      v_out_max,
      v_out_min,
      p_out_max,
      switching_freq,
      i_out_ripple,
      v_ripple_max,
      v_in_ripple,
    } = inputs;

    // Calculate duty cycle
    const duty_cycle_max = v_out_max / v_in_max;

    // Calculate output current
    const i_out_max = p_out_max / v_out_min;

    // Calculate inductance
    // L = (V_out * (1 - D)) / (f_s * ΔI)
    const inductance = (v_out_max * (1 - duty_cycle_max)) / (switching_freq * i_out_ripple);

    // Calculate output capacitance
    // C_out = ΔI / (8 * f_s * ΔV)
    const output_capacitance = i_out_ripple / (8 * switching_freq * v_ripple_max);

    // Calculate input capacitance
    // C_in = (I_out * D) / (f_s * ΔV_in)
    const input_capacitance = (i_out_max * duty_cycle_max) / (switching_freq * v_in_ripple);

    return {
      inductance,
      output_capacitance,
      input_capacitance,
      duty_cycle_max,
    };
  }
}

export function validateInputs(inputs: PFCInputs | BuckInputs): boolean {
  return Object.values(inputs).every((value) => typeof value === 'number' && value > 0);
}
