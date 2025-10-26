import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { CircuitCalculator, BuckInputs, validateInputs } from "@/lib/calculations";
import { toast } from "sonner";
import { Gauge } from "lucide-react";

export const BuckCalculator = () => {
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

      <Button onClick={handleCalculate} size="lg" className="w-full">
        Calculate Component Values
      </Button>

      {results && (
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
      )}
    </div>
  );
};
