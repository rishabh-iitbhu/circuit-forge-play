import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { CircuitCalculator, BuckInputs, validateInputs } from "@/lib/calculations";
import { suggestMOSFETs, suggestCapacitors, suggestInductors } from "@/lib/componentSuggestions";
import { toast } from "sonner";
import { Gauge, Cpu, Battery, Codesandbox, Settings } from "lucide-react";
import SimulationConfig from "@/components/SimulationConfig";
import SimulationProgress from "@/components/SimulationProgress";
import { PermutationSimulator } from "@/lib/permutationSimulator";
import { PermutationConfig } from "@/types/permutation";

export const BuckCalculator = () => {
  const navigate = useNavigate();
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationProgress, setSimulationProgress] = useState({ current: 0, total: 0, permutation: '' });
  const [showConfigDialog, setShowConfigDialog] = useState(false);
  const [inputs, setInputs] = useState<BuckInputs>({
    v_in_min: 12,
    v_in_max: 24,
    v_out_min: 3.3,
    v_out_max: 5,
    v_ripple_max: 0.05,
    v_in_ripple: 0.1,
    p_out_max: 50,
    efficiency: 0.95,
    i_out_ripple: 0.5,
    switching_freq: 500000,
    v_overshoot: 0.1,
    v_undershoot: 0.1,
    i_loadstep: 1,
  });

  const [results, setResults] = useState<{
    inductance: number;
    output_capacitance: number;
    input_capacitance: number;
    duty_cycle_max: number;
  } | null>(null);

  const handleInputChange = (key: keyof BuckInputs, value: number) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  const handleCalculate = () => {
    if (!validateInputs(inputs)) {
      toast.error("All values must be positive");
      return;
    }

    try {
      const calculator = new CircuitCalculator();
      const calculatedResults = calculator.calculateBuck(inputs);
      setResults(calculatedResults);
      toast.success("Calculation complete!");
    } catch (error) {
      toast.error("Calculation error occurred");
    }
  };

  const mosfetSuggestions = results 
    ? suggestMOSFETs(inputs.v_in_max, inputs.p_out_max / inputs.v_out_min)
    : [];
  
  const outputCapSuggestions = results
    ? suggestCapacitors(results.output_capacitance * 1e6, inputs.v_out_max)
    : [];
  
  const inductorSuggestions = results
    ? suggestInductors(results.inductance * 1e6, inputs.p_out_max / inputs.v_out_min)
    : [];

  const handleRunSimulation = async (config: PermutationConfig) => {
    if (!results) {
      toast.error("Please calculate component values first");
      return;
    }

    setIsSimulating(true);
    setSimulationProgress({ current: 0, total: 0, permutation: '' });

    try {
      const simulator = new PermutationSimulator();
      
      const permutations = await simulator.runAllPermutations(
        'BUCK',
        inputs,
        results,
        config,
        (current, total, permutation) => {
          setSimulationProgress({ current, total, permutation });
        }
      );

      toast.success(`${permutations.length} simulations complete!`);

      navigate('/simulation/report', {
        state: {
          report: {
            circuitType: 'BUCK',
            timestamp: new Date().toISOString(),
            inputs,
            results,
            permutations,
            bestPermutation: permutations[0],
            priorityMetrics: Object.entries(config.priorityMetrics)
              .filter(([_, v]) => v)
              .map(([k, _]) => k)
          }
        }
      });
    } catch (error) {
      console.error('Simulation error:', error);
      toast.error("Simulation failed. Please try again.");
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Voltage Parameters */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Gauge className="h-5 w-5 text-accent" />
            Voltage Parameters
          </h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="buck_v_in_min">Min Input Voltage (V)</Label>
              <Input
                id="buck_v_in_min"
                type="number"
                value={inputs.v_in_min}
                onChange={(e) => handleInputChange("v_in_min", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_v_in_max">Max Input Voltage (V)</Label>
              <Input
                id="buck_v_in_max"
                type="number"
                value={inputs.v_in_max}
                onChange={(e) => handleInputChange("v_in_max", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_v_out_min">Min Output Voltage (V)</Label>
              <Input
                id="buck_v_out_min"
                type="number"
                value={inputs.v_out_min}
                onChange={(e) => handleInputChange("v_out_min", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_v_out_max">Max Output Voltage (V)</Label>
              <Input
                id="buck_v_out_max"
                type="number"
                value={inputs.v_out_max}
                onChange={(e) => handleInputChange("v_out_max", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_v_ripple_max">Output Voltage Ripple (V)</Label>
              <Input
                id="buck_v_ripple_max"
                type="number"
                step="0.01"
                value={inputs.v_ripple_max}
                onChange={(e) => handleInputChange("v_ripple_max", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_v_in_ripple">Input Voltage Ripple (V)</Label>
              <Input
                id="buck_v_in_ripple"
                type="number"
                step="0.01"
                value={inputs.v_in_ripple}
                onChange={(e) => handleInputChange("v_in_ripple", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
          </div>
        </Card>

        {/* Power & Current Parameters */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Power & Current Parameters</h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="buck_p_out_max">Max Output Power (W)</Label>
              <Input
                id="buck_p_out_max"
                type="number"
                value={inputs.p_out_max}
                onChange={(e) => handleInputChange("p_out_max", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_efficiency">Efficiency (0-1)</Label>
              <Input
                id="buck_efficiency"
                type="number"
                step="0.01"
                min="0"
                max="1"
                value={inputs.efficiency}
                onChange={(e) => handleInputChange("efficiency", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_i_out_ripple">Inductor Current Ripple (A)</Label>
              <Input
                id="buck_i_out_ripple"
                type="number"
                step="0.1"
                value={inputs.i_out_ripple}
                onChange={(e) => handleInputChange("i_out_ripple", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
          </div>
        </Card>

        {/* Transient Parameters */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Transient Parameters</h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="buck_switching_freq">Switching Frequency (Hz)</Label>
              <Input
                id="buck_switching_freq"
                type="number"
                value={inputs.switching_freq}
                onChange={(e) => handleInputChange("switching_freq", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_v_overshoot">Voltage Overshoot (V)</Label>
              <Input
                id="buck_v_overshoot"
                type="number"
                step="0.01"
                value={inputs.v_overshoot}
                onChange={(e) => handleInputChange("v_overshoot", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_v_undershoot">Voltage Undershoot (V)</Label>
              <Input
                id="buck_v_undershoot"
                type="number"
                step="0.01"
                value={inputs.v_undershoot}
                onChange={(e) => handleInputChange("v_undershoot", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="buck_i_loadstep">Load Step (A)</Label>
              <Input
                id="buck_i_loadstep"
                type="number"
                step="0.1"
                value={inputs.i_loadstep}
                onChange={(e) => handleInputChange("i_loadstep", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
          </div>
        </Card>
      </div>

      <div className="space-y-3">
        <Button onClick={handleCalculate} size="lg" className="w-full">
          Calculate Component Values
        </Button>
        
        {results && mosfetSuggestions.length > 0 && outputCapSuggestions.length > 0 && inductorSuggestions.length > 0 && (
          <Button 
            onClick={() => setShowConfigDialog(true)} 
            size="lg"
            className="w-full gap-2" 
            variant="secondary"
            disabled={isSimulating}
          >
            <Settings className="w-4 h-4" />
            Configure & Run Simulation
          </Button>
        )}
      </div>

      {results && (
        <>
          <Card className="p-6 bg-gradient-to-br from-accent/5 to-primary/5 border-accent/20">
            <h3 className="text-xl font-bold mb-4 text-accent">Calculated Values</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="p-4 bg-card rounded-lg border border-border">
                <div className="text-sm text-muted-foreground mb-1">Inductance</div>
                <div className="text-2xl font-bold text-foreground">
                  {(results.inductance * 1e6).toFixed(2)} µH
                </div>
              </div>
              <div className="p-4 bg-card rounded-lg border border-border">
                <div className="text-sm text-muted-foreground mb-1">Output Capacitance</div>
                <div className="text-2xl font-bold text-foreground">
                  {(results.output_capacitance * 1e6).toFixed(2)} µF
                </div>
              </div>
              <div className="p-4 bg-card rounded-lg border border-border">
                <div className="text-sm text-muted-foreground mb-1">Input Capacitance</div>
                <div className="text-2xl font-bold text-foreground">
                  {(results.input_capacitance * 1e6).toFixed(2)} µF
                </div>
              </div>
              <div className="p-4 bg-card rounded-lg border border-border">
                <div className="text-sm text-muted-foreground mb-1">Max Duty Cycle</div>
                <div className="text-2xl font-bold text-foreground">
                  {(results.duty_cycle_max * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </Card>

          <div className="space-y-6">
            <h3 className="text-xl font-bold text-accent">Recommended Components</h3>
            
            <Card className="p-6">
              <h4 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Cpu className="h-5 w-5 text-accent" />
                MOSFETs
              </h4>
              <div className="space-y-4">
                {mosfetSuggestions.map((suggestion, idx) => (
                  <div key={idx} className="border-l-4 border-accent/40 pl-4 py-2">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <div className="font-semibold text-foreground">{idx + 1}. {suggestion.component.name}</div>
                        <div className="text-sm text-muted-foreground">{suggestion.component.manufacturer}</div>
                      </div>
                      <div className="text-xs bg-accent/10 text-accent px-2 py-1 rounded">
                        {suggestion.component.efficiencyRange}
                      </div>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs mb-2">
                      <div><span className="text-muted-foreground">VDS:</span> <span className="font-medium">{suggestion.component.vds}V</span></div>
                      <div><span className="text-muted-foreground">ID:</span> <span className="font-medium">{suggestion.component.id}A</span></div>
                      <div><span className="text-muted-foreground">RDS(on):</span> <span className="font-medium">{suggestion.component.rdson}mΩ</span></div>
                      <div><span className="text-muted-foreground">Qg:</span> <span className="font-medium">{suggestion.component.qg}nC</span></div>
                      <div><span className="text-muted-foreground">Package:</span> <span className="font-medium">{suggestion.component.package}</span></div>
                    </div>
                    <div className="text-sm text-muted-foreground italic">
                      <span className="font-semibold text-foreground">Why: </span>{suggestion.reason}
                    </div>
                  </div>
                ))}
                {mosfetSuggestions.length === 0 && (
                  <div className="text-muted-foreground text-sm">No suitable MOSFETs found for these specifications</div>
                )}
              </div>
            </Card>

            <Card className="p-6">
              <h4 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Battery className="h-5 w-5 text-accent" />
                Output Capacitors
              </h4>
              <div className="space-y-4">
                {outputCapSuggestions.map((suggestion, idx) => (
                  <div key={idx} className="border-l-4 border-accent/40 pl-4 py-2">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <div className="font-semibold text-foreground">{idx + 1}. {suggestion.component.partNumber}</div>
                        <div className="text-sm text-muted-foreground">{suggestion.component.manufacturer}</div>
                      </div>
                      <div className="text-xs bg-primary/20 text-primary px-2 py-1 rounded">
                        {suggestion.component.type}
                      </div>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs mb-2">
                      <div><span className="text-muted-foreground">Capacitance:</span> <span className="font-medium">{suggestion.component.capacitance}µF</span></div>
                      <div><span className="text-muted-foreground">Voltage:</span> <span className="font-medium">{suggestion.component.voltage}V</span></div>
                      <div><span className="text-muted-foreground">ESR:</span> <span className="font-medium">{suggestion.component.esr}mΩ</span></div>
                      <div><span className="text-muted-foreground">Temp:</span> <span className="font-medium">{suggestion.component.tempRange}°C</span></div>
                    </div>
                    <div className="text-sm text-muted-foreground italic">
                      <span className="font-semibold text-foreground">Why: </span>{suggestion.reason}
                    </div>
                  </div>
                ))}
                {outputCapSuggestions.length === 0 && (
                  <div className="text-muted-foreground text-sm">No suitable capacitors found for these specifications</div>
                )}
              </div>
            </Card>

            <Card className="p-6">
              <h4 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Codesandbox className="h-5 w-5 text-accent" />
                Inductors
              </h4>
              <div className="space-y-4">
                {inductorSuggestions.map((suggestion, idx) => (
                  <div key={idx} className="border-l-4 border-accent/40 pl-4 py-2">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <div className="font-semibold text-foreground">{idx + 1}. {suggestion.component.partNumber}</div>
                        <div className="text-sm text-muted-foreground">{suggestion.component.manufacturer}</div>
                      </div>
                      <div className="text-xs bg-secondary/80 text-secondary-foreground px-2 py-1 rounded">
                        {suggestion.component.package}
                      </div>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs mb-2">
                      <div><span className="text-muted-foreground">Inductance:</span> <span className="font-medium">{suggestion.component.inductance}µH</span></div>
                      <div><span className="text-muted-foreground">Current:</span> <span className="font-medium">{suggestion.component.current}A</span></div>
                      <div><span className="text-muted-foreground">DCR:</span> <span className="font-medium">{suggestion.component.dcr}mΩ</span></div>
                      <div><span className="text-muted-foreground">Isat:</span> <span className="font-medium">{suggestion.component.satCurrent}A</span></div>
                    </div>
                    <div className="text-sm text-muted-foreground italic">
                      <span className="font-semibold text-foreground">Why: </span>{suggestion.reason}
                    </div>
                  </div>
                ))}
                {inductorSuggestions.length === 0 && (
                  <div className="text-muted-foreground text-sm">No suitable inductors found for these specifications</div>
                )}
              </div>
            </Card>
          </div>
        </>
      )}

      {/* Simulation Config Dialog */}
      <SimulationConfig
        open={showConfigDialog}
        onOpenChange={setShowConfigDialog}
        mosfetSuggestions={mosfetSuggestions.map(s => s.component)}
        capacitorSuggestions={outputCapSuggestions.map(s => s.component)}
        inductorSuggestions={inductorSuggestions.map(s => s.component)}
        onRunSimulation={handleRunSimulation}
      />

      {/* Simulation Progress */}
      {isSimulating && (
        <SimulationProgress
          current={simulationProgress.current}
          total={simulationProgress.total}
          currentPermutation={simulationProgress.permutation}
        />
      )}
    </div>
  );
};
