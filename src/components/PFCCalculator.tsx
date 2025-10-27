import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { CircuitCalculator, PFCInputs, validateInputs } from "@/lib/calculations";
import { suggestMOSFETs, suggestCapacitors, suggestInductors } from "@/lib/componentSuggestions";
import { toast } from "sonner";
import { Zap, Cpu, Battery, Codesandbox } from "lucide-react";

export const PFCCalculator = () => {
  const [inputs, setInputs] = useState<PFCInputs>({
    v_in_min: 100,
    v_in_max: 240,
    v_out_min: 380,
    v_out_max: 400,
    p_out_max: 3000,
    efficiency: 0.98,
    v_ripple_max: 20,
    switching_freq: 65000,
    line_freq_min: 50,
  });

  const [results, setResults] = useState<{
    inductance: number;
    capacitance: number;
    ripple_current: number;
  } | null>(null);

  const handleInputChange = (key: keyof PFCInputs, value: number) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  const handleCalculate = () => {
    if (!validateInputs(inputs)) {
      toast.error("All values must be positive");
      return;
    }

    try {
      const calculator = new CircuitCalculator();
      const calculatedResults = calculator.calculatePFC(inputs);
      setResults(calculatedResults);
      toast.success("Calculation complete!");
    } catch (error) {
      toast.error("Calculation error occurred");
    }
  };

  const mosfetSuggestions = results 
    ? suggestMOSFETs(inputs.v_out_max, inputs.p_out_max / inputs.v_in_min)
    : [];
  
  const capacitorSuggestions = results
    ? suggestCapacitors(results.capacitance * 1e6, inputs.v_out_max)
    : [];
  
  const inductorSuggestions = results
    ? suggestInductors(results.inductance * 1e6, results.ripple_current)
    : [];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Voltage Parameters */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="h-5 w-5 text-primary" />
            Voltage Parameters
          </h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="v_in_min">Min Input Voltage (V)</Label>
              <Input
                id="v_in_min"
                type="number"
                value={inputs.v_in_min}
                onChange={(e) => handleInputChange("v_in_min", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="v_in_max">Max Input Voltage (V)</Label>
              <Input
                id="v_in_max"
                type="number"
                value={inputs.v_in_max}
                onChange={(e) => handleInputChange("v_in_max", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="v_out_min">Min Output Voltage (V)</Label>
              <Input
                id="v_out_min"
                type="number"
                value={inputs.v_out_min}
                onChange={(e) => handleInputChange("v_out_min", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="v_out_max">Max Output Voltage (V)</Label>
              <Input
                id="v_out_max"
                type="number"
                value={inputs.v_out_max}
                onChange={(e) => handleInputChange("v_out_max", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
          </div>
        </Card>

        {/* Power Parameters */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Power Parameters</h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="p_out_max">Max Output Power (W)</Label>
              <Input
                id="p_out_max"
                type="number"
                value={inputs.p_out_max}
                onChange={(e) => handleInputChange("p_out_max", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="efficiency">Efficiency (0-1)</Label>
              <Input
                id="efficiency"
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
              <Label htmlFor="v_ripple_max">Max Output Voltage Ripple (V)</Label>
              <Input
                id="v_ripple_max"
                type="number"
                value={inputs.v_ripple_max}
                onChange={(e) => handleInputChange("v_ripple_max", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
          </div>
        </Card>

        {/* Frequency Parameters */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Frequency Parameters</h3>
          <div className="space-y-4">
            <div>
              <Label htmlFor="switching_freq">Switching Frequency (Hz)</Label>
              <Input
                id="switching_freq"
                type="number"
                value={inputs.switching_freq}
                onChange={(e) => handleInputChange("switching_freq", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="line_freq_min">Min Line Frequency (Hz)</Label>
              <Input
                id="line_freq_min"
                type="number"
                value={inputs.line_freq_min}
                onChange={(e) => handleInputChange("line_freq_min", parseFloat(e.target.value))}
                className="mt-1"
              />
            </div>
          </div>
        </Card>
      </div>

      <Button onClick={handleCalculate} size="lg" className="w-full">
        Calculate Component Values
      </Button>

      {results && (
        <>
          <Card className="p-6 bg-gradient-to-br from-primary/5 to-accent/5 border-primary/20">
            <h3 className="text-xl font-bold mb-4 text-primary">Calculated Values</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-card rounded-lg border border-border">
                <div className="text-sm text-muted-foreground mb-1">Inductance</div>
                <div className="text-2xl font-bold text-foreground">
                  {(results.inductance * 1000).toFixed(2)} mH
                </div>
              </div>
              <div className="p-4 bg-card rounded-lg border border-border">
                <div className="text-sm text-muted-foreground mb-1">Capacitance</div>
                <div className="text-2xl font-bold text-foreground">
                  {(results.capacitance * 1e6).toFixed(2)} µF
                </div>
              </div>
              <div className="p-4 bg-card rounded-lg border border-border">
                <div className="text-sm text-muted-foreground mb-1">Ripple Current</div>
                <div className="text-2xl font-bold text-foreground">
                  {results.ripple_current.toFixed(2)} A
                </div>
              </div>
            </div>
          </Card>

          <div className="space-y-6">
            <h3 className="text-xl font-bold text-primary">Recommended Components</h3>
            
            <Card className="p-6">
              <h4 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Cpu className="h-5 w-5 text-primary" />
                MOSFETs
              </h4>
              <div className="space-y-4">
                {mosfetSuggestions.map((suggestion, idx) => (
                  <div key={idx} className="border-l-4 border-primary/40 pl-4 py-2">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <div className="font-semibold text-foreground">{idx + 1}. {suggestion.component.name}</div>
                        <div className="text-sm text-muted-foreground">{suggestion.component.manufacturer}</div>
                      </div>
                      <div className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
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
                <Battery className="h-5 w-5 text-primary" />
                Capacitors
              </h4>
              <div className="space-y-4">
                {capacitorSuggestions.map((suggestion, idx) => (
                  <div key={idx} className="border-l-4 border-primary/40 pl-4 py-2">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <div className="font-semibold text-foreground">{idx + 1}. {suggestion.component.partNumber}</div>
                        <div className="text-sm text-muted-foreground">{suggestion.component.manufacturer}</div>
                      </div>
                      <div className="text-xs bg-accent/20 text-accent-foreground px-2 py-1 rounded">
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
                {capacitorSuggestions.length === 0 && (
                  <div className="text-muted-foreground text-sm">No suitable capacitors found for these specifications</div>
                )}
              </div>
            </Card>

            <Card className="p-6">
              <h4 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Codesandbox className="h-5 w-5 text-primary" />
                Inductors
              </h4>
              <div className="space-y-4">
                {inductorSuggestions.map((suggestion, idx) => (
                  <div key={idx} className="border-l-4 border-primary/40 pl-4 py-2">
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
    </div>
  );
};
