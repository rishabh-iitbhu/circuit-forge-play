export interface PermutationConfig {
  selectedMOSFETs: any[];
  selectedCapacitors: any[];
  selectedInductors: any[];
  priorityMetrics: {
    efficiency: boolean;
    powerFactor: boolean;
    thd: boolean;
    voltageRipple: boolean;
    currentRipple: boolean;
  };
}

export interface PermutationResult {
  id: string;
  components: {
    mosfet: any;
    capacitor: any;
    inductor: any;
  };
  metrics: {
    efficiency: number;
    powerFactor: number;
    thd: number;
    voltageRipple: number;
    currentRipple: number;
    peakCurrent: number;
  };
  waveformData: {
    time: number[];
    inputVoltage: number[];
    outputVoltage: number[];
    inputCurrent: number[];
    outputCurrent: number[];
    switchingNode: number[];
  };
  rank?: number;
  score?: number;
}

export interface SimulationReport {
  circuitType: 'PFC' | 'BUCK';
  timestamp: string;
  inputs: any;
  results: any;
  permutations: PermutationResult[];
  bestPermutation: PermutationResult;
  priorityMetrics: string[];
}
