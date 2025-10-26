import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { CircuitCalculator, PFCInputs, validateInputs } from "@/lib/calculations";
import { toast } from "sonner";
import { Zap } from "lucide-react";

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
      )}
    </div>
  );
};
