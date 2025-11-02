import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Settings, Zap } from 'lucide-react';

interface SimulationConfigProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  mosfetSuggestions: any[];
  capacitorSuggestions: any[];
  inductorSuggestions: any[];
  onRunSimulation: (config: {
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
  }) => void;
}

export default function SimulationConfig({
  open,
  onOpenChange,
  mosfetSuggestions,
  capacitorSuggestions,
  inductorSuggestions,
  onRunSimulation
}: SimulationConfigProps) {
  const [selectedMOSFETs, setSelectedMOSFETs] = useState<string[]>(
    mosfetSuggestions.slice(0, 3).map(m => m.part_number)
  );
  const [selectedCapacitors, setSelectedCapacitors] = useState<string[]>(
    capacitorSuggestions.slice(0, 3).map(c => c.part_number)
  );
  const [selectedInductors, setSelectedInductors] = useState<string[]>(
    inductorSuggestions.slice(0, 3).map(i => i.part_number)
  );
  const [metrics, setMetrics] = useState({
    efficiency: true,
    powerFactor: true,
    thd: true,
    voltageRipple: false,
    currentRipple: false
  });

  const toggleMOSFET = (partNumber: string) => {
    setSelectedMOSFETs(prev =>
      prev.includes(partNumber)
        ? prev.filter(p => p !== partNumber)
        : [...prev, partNumber]
    );
  };

  const toggleCapacitor = (partNumber: string) => {
    setSelectedCapacitors(prev =>
      prev.includes(partNumber)
        ? prev.filter(p => p !== partNumber)
        : [...prev, partNumber]
    );
  };

  const toggleInductor = (partNumber: string) => {
    setSelectedInductors(prev =>
      prev.includes(partNumber)
        ? prev.filter(p => p !== partNumber)
        : [...prev, partNumber]
    );
  };

  const totalPermutations = selectedMOSFETs.length * selectedCapacitors.length * selectedInductors.length;

  const handleRunSimulation = () => {
    const config = {
      selectedMOSFETs: mosfetSuggestions.filter(m => selectedMOSFETs.includes(m.part_number)),
      selectedCapacitors: capacitorSuggestions.filter(c => selectedCapacitors.includes(c.part_number)),
      selectedInductors: inductorSuggestions.filter(i => selectedInductors.includes(i.part_number)),
      priorityMetrics: metrics
    };
    onRunSimulation(config);
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            Configure SPICE Simulation
          </DialogTitle>
          <DialogDescription>
            Select components to test and metrics to prioritize. Total permutations: <strong>{totalPermutations}</strong>
          </DialogDescription>
        </DialogHeader>

        <ScrollArea className="max-h-[60vh] pr-4">
          <div className="space-y-6">
            {/* MOSFETs Selection */}
            <div>
              <h3 className="font-semibold mb-3">MOSFETs ({mosfetSuggestions.length} available)</h3>
              <div className="space-y-2">
                {mosfetSuggestions.map(mosfet => (
                  <Card key={mosfet.part_number} className="p-3">
                    <div className="flex items-start gap-3">
                      <Checkbox
                        id={`mosfet-${mosfet.part_number}`}
                        checked={selectedMOSFETs.includes(mosfet.part_number)}
                        onCheckedChange={() => toggleMOSFET(mosfet.part_number)}
                      />
                      <div className="flex-1">
                        <Label htmlFor={`mosfet-${mosfet.part_number}`} className="font-medium cursor-pointer">
                          {mosfet.part_number}
                        </Label>
                        <p className="text-sm text-muted-foreground">
                          {mosfet.voltage_rating}V, {mosfet.current_rating}A, RDS(on): {mosfet.rds_on}Ω
                        </p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            <Separator />

            {/* Capacitors Selection */}
            <div>
              <h3 className="font-semibold mb-3">Capacitors ({capacitorSuggestions.length} available)</h3>
              <div className="space-y-2">
                {capacitorSuggestions.map(cap => (
                  <Card key={cap.part_number} className="p-3">
                    <div className="flex items-start gap-3">
                      <Checkbox
                        id={`cap-${cap.part_number}`}
                        checked={selectedCapacitors.includes(cap.part_number)}
                        onCheckedChange={() => toggleCapacitor(cap.part_number)}
                      />
                      <div className="flex-1">
                        <Label htmlFor={`cap-${cap.part_number}`} className="font-medium cursor-pointer">
                          {cap.part_number}
                        </Label>
                        <p className="text-sm text-muted-foreground">
                          {cap.capacitance}µF, {cap.voltage_rating}V, ESR: {cap.esr}Ω
                        </p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            <Separator />

            {/* Inductors Selection */}
            <div>
              <h3 className="font-semibold mb-3">Inductors ({inductorSuggestions.length} available)</h3>
              <div className="space-y-2">
                {inductorSuggestions.map(ind => (
                  <Card key={ind.part_number} className="p-3">
                    <div className="flex items-start gap-3">
                      <Checkbox
                        id={`ind-${ind.part_number}`}
                        checked={selectedInductors.includes(ind.part_number)}
                        onCheckedChange={() => toggleInductor(ind.part_number)}
                      />
                      <div className="flex-1">
                        <Label htmlFor={`ind-${ind.part_number}`} className="font-medium cursor-pointer">
                          {ind.part_number}
                        </Label>
                        <p className="text-sm text-muted-foreground">
                          {ind.inductance}µH, {ind.current_rating}A, DCR: {ind.dcr}Ω
                        </p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            <Separator />

            {/* Priority Metrics */}
            <div>
              <h3 className="font-semibold mb-3">Priority Metrics (for ranking)</h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Checkbox
                    id="metric-efficiency"
                    checked={metrics.efficiency}
                    onCheckedChange={(checked) => setMetrics(prev => ({ ...prev, efficiency: !!checked }))}
                  />
                  <Label htmlFor="metric-efficiency" className="cursor-pointer">
                    Efficiency
                  </Label>
                </div>
                <div className="flex items-center gap-3">
                  <Checkbox
                    id="metric-pf"
                    checked={metrics.powerFactor}
                    onCheckedChange={(checked) => setMetrics(prev => ({ ...prev, powerFactor: !!checked }))}
                  />
                  <Label htmlFor="metric-pf" className="cursor-pointer">
                    Power Factor
                  </Label>
                </div>
                <div className="flex items-center gap-3">
                  <Checkbox
                    id="metric-thd"
                    checked={metrics.thd}
                    onCheckedChange={(checked) => setMetrics(prev => ({ ...prev, thd: !!checked }))}
                  />
                  <Label htmlFor="metric-thd" className="cursor-pointer">
                    Total Harmonic Distortion (THD)
                  </Label>
                </div>
                <div className="flex items-center gap-3">
                  <Checkbox
                    id="metric-vripple"
                    checked={metrics.voltageRipple}
                    onCheckedChange={(checked) => setMetrics(prev => ({ ...prev, voltageRipple: !!checked }))}
                  />
                  <Label htmlFor="metric-vripple" className="cursor-pointer">
                    Voltage Ripple
                  </Label>
                </div>
                <div className="flex items-center gap-3">
                  <Checkbox
                    id="metric-iripple"
                    checked={metrics.currentRipple}
                    onCheckedChange={(checked) => setMetrics(prev => ({ ...prev, currentRipple: !!checked }))}
                  />
                  <Label htmlFor="metric-iripple" className="cursor-pointer">
                    Current Ripple
                  </Label>
                </div>
              </div>
            </div>
          </div>
        </ScrollArea>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleRunSimulation}
            disabled={totalPermutations === 0}
            className="gap-2"
          >
            <Zap className="w-4 h-4" />
            Run {totalPermutations} Simulation{totalPermutations !== 1 ? 's' : ''}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
