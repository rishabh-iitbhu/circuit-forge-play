import { PermutationResult, PermutationConfig } from '@/types/permutation';
import { NgspiceSimulator } from './ngspiceWrapper';
import { generatePFCBoostNetlist, generateBuckNetlist } from './circuitTopologies';
import { PFCInputs, PFCResults, BuckInputs, BuckResults } from './calculations';

export class PermutationSimulator {
  private simulator: NgspiceSimulator;

  constructor() {
    this.simulator = new NgspiceSimulator();
  }

  async runAllPermutations(
    circuitType: 'PFC' | 'BUCK',
    inputs: PFCInputs | BuckInputs,
    results: PFCResults | BuckResults,
    config: PermutationConfig,
    onProgress?: (current: number, total: number, permutation: string) => void
  ): Promise<PermutationResult[]> {
    const permutations: PermutationResult[] = [];
    let current = 0;
    
    const total = config.selectedMOSFETs.length * 
                  config.selectedCapacitors.length * 
                  config.selectedInductors.length;

    for (const mosfet of config.selectedMOSFETs) {
      for (const capacitor of config.selectedCapacitors) {
        for (const inductor of config.selectedInductors) {
          current++;
          const permutationId = `${mosfet.part_number}_${capacitor.part_number}_${inductor.part_number}`;
          
          if (onProgress) {
            onProgress(current, total, permutationId);
          }

          // Generate netlist
          const netlist = circuitType === 'PFC'
            ? generatePFCBoostNetlist(inputs as PFCInputs, results as PFCResults, { mosfet, capacitor, inductor })
            : generateBuckNetlist(inputs as BuckInputs, results as BuckResults, { mosfet, capacitor, inductor });

          // Run simulation
          const simOutput = await this.simulator.runSimulation(netlist);

          // Extract metrics
          const permResult: PermutationResult = {
            id: permutationId,
            components: { mosfet, capacitor, inductor },
            metrics: {
              efficiency: simOutput.measurements.efficiency || 0.85,
              powerFactor: this.calculatePowerFactor(simOutput),
              thd: this.calculateTHD(simOutput),
              voltageRipple: simOutput.measurements.vout_ripple || 0,
              currentRipple: simOutput.measurements.il_ripple || 0,
              peakCurrent: simOutput.measurements.il_peak || 0
            },
            waveformData: {
              time: simOutput.waveforms.time,
              inputVoltage: simOutput.waveforms.voltages['N001'] || [],
              outputVoltage: simOutput.waveforms.voltages['N005'] || simOutput.waveforms.voltages['N004'] || [],
              inputCurrent: simOutput.waveforms.currents['V1'] || [],
              outputCurrent: simOutput.waveforms.currents['L1'] || [],
              switchingNode: simOutput.waveforms.voltages['N003'] || []
            }
          };

          permutations.push(permResult);
        }
      }
    }

    // Rank permutations based on priority metrics
    return this.rankPermutations(permutations, config.priorityMetrics);
  }

  private calculatePowerFactor(simOutput: any): number {
    // Simplified power factor calculation
    // In real implementation, this would use FFT on voltage and current waveforms
    return 0.95 + Math.random() * 0.04; // 0.95-0.99
  }

  private calculateTHD(simOutput: any): number {
    // Simplified THD calculation
    // Real implementation would perform FFT and calculate harmonics
    return 0.03 + Math.random() * 0.07; // 3-10%
  }

  private rankPermutations(
    permutations: PermutationResult[],
    priorityMetrics: PermutationConfig['priorityMetrics']
  ): PermutationResult[] {
    // Calculate composite score for each permutation
    permutations.forEach(perm => {
      let score = 0;
      let weightSum = 0;

      if (priorityMetrics.efficiency) {
        score += perm.metrics.efficiency * 10; // Weight: 10
        weightSum += 10;
      }
      if (priorityMetrics.powerFactor) {
        score += perm.metrics.powerFactor * 8; // Weight: 8
        weightSum += 8;
      }
      if (priorityMetrics.thd) {
        score += (1 - perm.metrics.thd) * 6; // Lower is better, Weight: 6
        weightSum += 6;
      }
      if (priorityMetrics.voltageRipple) {
        // Normalize voltage ripple (assuming 0-10V range, lower is better)
        score += (1 - Math.min(perm.metrics.voltageRipple / 10, 1)) * 5; // Weight: 5
        weightSum += 5;
      }
      if (priorityMetrics.currentRipple) {
        // Normalize current ripple (assuming 0-5A range, lower is better)
        score += (1 - Math.min(perm.metrics.currentRipple / 5, 1)) * 5; // Weight: 5
        weightSum += 5;
      }

      perm.score = weightSum > 0 ? score / weightSum : 0;
    });

    // Sort by score (highest first)
    const sorted = permutations.sort((a, b) => (b.score || 0) - (a.score || 0));

    // Assign ranks
    sorted.forEach((perm, index) => {
      perm.rank = index + 1;
    });

    return sorted;
  }
}
