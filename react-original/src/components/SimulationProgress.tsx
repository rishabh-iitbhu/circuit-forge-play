import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Loader2, Zap, CheckCircle2 } from 'lucide-react';

interface SimulationProgressProps {
  current: number;
  total: number;
  currentPermutation?: string;
}

export default function SimulationProgress({ current, total, currentPermutation }: SimulationProgressProps) {
  const progress = (current / total) * 100;
  const isComplete = current === total;

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50">
      <Card className="p-8 max-w-md w-full mx-4">
        <div className="text-center space-y-6">
          {!isComplete ? (
            <>
              <div className="flex justify-center">
                <div className="relative">
                  <Loader2 className="w-16 h-16 text-primary animate-spin" />
                  <Zap className="w-8 h-8 text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
                </div>
              </div>
              
              <div>
                <h2 className="text-2xl font-bold mb-2">Running SPICE Simulations</h2>
                <p className="text-muted-foreground">
                  Simulating permutation {current} of {total}
                </p>
                {currentPermutation && (
                  <p className="text-sm text-muted-foreground mt-2 font-mono">
                    {currentPermutation}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Progress value={progress} className="h-2" />
                <p className="text-sm text-muted-foreground">
                  {Math.round(progress)}% complete
                </p>
              </div>

              <div className="text-sm text-muted-foreground space-y-1">
                <p>• Generating netlist</p>
                <p>• Running transient analysis</p>
                <p>• Extracting measurements</p>
              </div>
            </>
          ) : (
            <>
              <div className="flex justify-center">
                <CheckCircle2 className="w-16 h-16 text-green-500" />
              </div>
              
              <div>
                <h2 className="text-2xl font-bold mb-2">Simulations Complete!</h2>
                <p className="text-muted-foreground">
                  All {total} permutations analyzed successfully
                </p>
              </div>

              <div className="animate-pulse text-sm text-muted-foreground">
                Preparing report...
              </div>
            </>
          )}
        </div>
      </Card>
    </div>
  );
}
