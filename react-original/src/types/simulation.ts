export interface SimulationParameters {
  circuitType: 'PFC' | 'BUCK';
  inputs: any;
  results: any;
  selectedComponents: {
    mosfet?: any;
    capacitor?: any;
    inductor?: any;
  };
  timestamp: string;
}

export interface SimulationData {
  time: number[];
  inputVoltage: number[];
  outputVoltage: number[];
  inputCurrent: number[];
  outputCurrent: number[];
  efficiency: number[];
  switchingNode: number[];
}

export interface SimulationResults {
  parameters: SimulationParameters;
  data: SimulationData;
  analysis: {
    avgEfficiency: number;
    peakCurrent: number;
    voltageRipple: number;
    currentRipple: number;
    powerFactor: number;
    thd: number;
  };
  netlist: string;
}
