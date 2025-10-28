import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ArrowLeft, Download, CheckCircle2, AlertCircle, Info } from 'lucide-react';
import { SimulationResults as SimulationResultsType } from '@/types/simulation';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';

const SimulationResults = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [results, setResults] = useState<SimulationResultsType | null>(null);

  useEffect(() => {
    if (location.state?.results) {
      setResults(location.state.results);
    } else {
      navigate('/');
    }
  }, [location, navigate]);

  if (!results) {
    return null;
  }

  const { data, analysis, netlist, parameters } = results;

  const downloadNetlist = () => {
    const blob = new Blob([netlist], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pfc_netlist_${Date.now()}.cir`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getStatusBadge = (value: number, threshold: number, reverse = false) => {
    const pass = reverse ? value < threshold : value > threshold;
    return pass ? (
      <Badge className="bg-green-500/10 text-green-500 border-green-500/20">
        <CheckCircle2 className="w-3 h-3 mr-1" />
        Pass
      </Badge>
    ) : (
      <Badge className="bg-amber-500/10 text-amber-500 border-amber-500/20">
        <AlertCircle className="w-3 h-3 mr-1" />
        Review
      </Badge>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={() => navigate('/')}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Calculator
            </Button>
            <div>
              <h1 className="text-3xl font-bold">PFC Circuit Simulation Results</h1>
              <p className="text-muted-foreground">
                Generated on {new Date(parameters.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
          <Button onClick={downloadNetlist} variant="secondary">
            <Download className="w-4 h-4 mr-2" />
            Download Netlist
          </Button>
        </div>

        {/* Analysis Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Efficiency</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{analysis.avgEfficiency}%</div>
              <div className="mt-2">{getStatusBadge(analysis.avgEfficiency, 85)}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Power Factor</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{analysis.powerFactor}</div>
              <div className="mt-2">{getStatusBadge(analysis.powerFactor, 0.95)}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">THD</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{analysis.thd}%</div>
              <div className="mt-2">{getStatusBadge(analysis.thd, 5, true)}</div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="waveforms" className="space-y-4">
          <TabsList>
            <TabsTrigger value="waveforms">Waveform Data</TabsTrigger>
            <TabsTrigger value="analysis">Detailed Analysis</TabsTrigger>
            <TabsTrigger value="netlist">SPICE Netlist</TabsTrigger>
            <TabsTrigger value="conclusion">Conclusion</TabsTrigger>
          </TabsList>

          <TabsContent value="waveforms" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Simulation Waveform Data</CardTitle>
                <CardDescription>
                  Time-domain waveforms from LTSpice simulation (first 50 points shown)
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-auto max-h-[600px]">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Time (ms)</TableHead>
                        <TableHead>V_in (V)</TableHead>
                        <TableHead>V_out (V)</TableHead>
                        <TableHead>I_in (A)</TableHead>
                        <TableHead>I_out (A)</TableHead>
                        <TableHead>Efficiency (%)</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {data.time.slice(0, 50).map((time, idx) => (
                        <TableRow key={idx}>
                          <TableCell>{time.toFixed(4)}</TableCell>
                          <TableCell>{data.inputVoltage[idx].toFixed(2)}</TableCell>
                          <TableCell>{data.outputVoltage[idx].toFixed(2)}</TableCell>
                          <TableCell>{data.inputCurrent[idx].toFixed(3)}</TableCell>
                          <TableCell>{data.outputCurrent[idx].toFixed(3)}</TableCell>
                          <TableCell>{data.efficiency[idx].toFixed(2)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
                <p className="text-sm text-muted-foreground mt-4">
                  Showing 50 of {data.time.length} data points
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analysis" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Detailed Performance Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableBody>
                    <TableRow>
                      <TableCell className="font-medium">Average Efficiency</TableCell>
                      <TableCell>{analysis.avgEfficiency}%</TableCell>
                      <TableCell>{getStatusBadge(analysis.avgEfficiency, 85)}</TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        Target: &gt;85%
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Peak Input Current</TableCell>
                      <TableCell>{analysis.peakCurrent.toFixed(3)} A</TableCell>
                      <TableCell>
                        <Badge variant="outline">
                          <Info className="w-3 h-3 mr-1" />
                          Info
                        </Badge>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        Used for component selection
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Output Voltage Ripple</TableCell>
                      <TableCell>{(analysis.voltageRipple * 1000).toFixed(1)} mV</TableCell>
                      <TableCell>{getStatusBadge(analysis.voltageRipple, parameters.inputs.v_ripple_max, true)}</TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        Target: &lt;{(parameters.inputs.v_ripple_max * 1000).toFixed(0)} mV
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Input Current Ripple</TableCell>
                      <TableCell>{analysis.currentRipple.toFixed(3)} A</TableCell>
                      <TableCell>
                        <Badge variant="outline">
                          <Info className="w-3 h-3 mr-1" />
                          Info
                        </Badge>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        Affects inductor design
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Power Factor</TableCell>
                      <TableCell>{analysis.powerFactor}</TableCell>
                      <TableCell>{getStatusBadge(analysis.powerFactor, 0.95)}</TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        Target: &gt;0.95
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Total Harmonic Distortion</TableCell>
                      <TableCell>{analysis.thd}%</TableCell>
                      <TableCell>{getStatusBadge(analysis.thd, 5, true)}</TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        Target: &lt;5%
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Selected Components</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {parameters.selectedComponents.mosfet && (
                    <div className="border rounded-lg p-4">
                      <h4 className="font-semibold mb-2">MOSFET</h4>
                      <p className="text-sm">{parameters.selectedComponents.mosfet.part_number}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {parameters.selectedComponents.mosfet.v_dss}V / {parameters.selectedComponents.mosfet.i_d}A
                      </p>
                    </div>
                  )}
                  {parameters.selectedComponents.inductor && (
                    <div className="border rounded-lg p-4">
                      <h4 className="font-semibold mb-2">Inductor</h4>
                      <p className="text-sm">{parameters.selectedComponents.inductor.part_number}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {parameters.selectedComponents.inductor.inductance}µH / {parameters.selectedComponents.inductor.current_rating}A
                      </p>
                    </div>
                  )}
                  {parameters.selectedComponents.capacitor && (
                    <div className="border rounded-lg p-4">
                      <h4 className="font-semibold mb-2">Capacitor</h4>
                      <p className="text-sm">{parameters.selectedComponents.capacitor.part_number}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {parameters.selectedComponents.capacitor.capacitance}µF / {parameters.selectedComponents.capacitor.voltage_rating}V
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="netlist">
            <Card>
              <CardHeader>
                <CardTitle>LTSpice Netlist</CardTitle>
                <CardDescription>
                  Complete SPICE netlist used for simulation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Textarea
                  value={netlist}
                  readOnly
                  className="font-mono text-xs min-h-[500px]"
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="conclusion">
            <Card>
              <CardHeader>
                <CardTitle>Simulation Conclusion</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="prose prose-sm max-w-none">
                  <h3 className="text-lg font-semibold">Overall Assessment</h3>
                  <p>
                    The PFC circuit simulation has been completed successfully. The design meets 
                    {analysis.avgEfficiency >= 85 && analysis.powerFactor >= 0.95 && analysis.thd <= 5
                      ? ' all key performance targets.'
                      : ' most performance targets with some areas for optimization.'}
                  </p>

                  <h3 className="text-lg font-semibold mt-6">Key Findings</h3>
                  <ul className="list-disc pl-5 space-y-2">
                    <li>
                      <strong>Efficiency ({analysis.avgEfficiency}%):</strong>{' '}
                      {analysis.avgEfficiency >= 85
                        ? 'Excellent efficiency achieved, meeting industry standards for PFC circuits.'
                        : 'Efficiency is below target. Consider using MOSFETs with lower RDS(on) or optimizing the gate drive circuit.'}
                    </li>
                    <li>
                      <strong>Power Factor ({analysis.powerFactor}):</strong>{' '}
                      {analysis.powerFactor >= 0.95
                        ? 'Outstanding power factor correction, ensuring minimal reactive power draw.'
                        : 'Power factor could be improved with better control loop tuning or increased switching frequency.'}
                    </li>
                    <li>
                      <strong>THD ({analysis.thd}%):</strong>{' '}
                      {analysis.thd <= 5
                        ? 'Low harmonic distortion, compliant with most power quality standards.'
                        : 'THD is higher than ideal. Consider adding input filtering or adjusting control algorithm.'}
                    </li>
                    <li>
                      <strong>Output Ripple ({(analysis.voltageRipple * 1000).toFixed(1)} mV):</strong>{' '}
                      {analysis.voltageRipple <= parameters.inputs.v_ripple_max
                        ? 'Output ripple is within specifications.'
                        : 'Output ripple exceeds target. Consider increasing output capacitance or optimizing control loop.'}
                    </li>
                  </ul>

                  <h3 className="text-lg font-semibold mt-6">Recommendations</h3>
                  <ul className="list-disc pl-5 space-y-2">
                    {analysis.avgEfficiency < 85 && (
                      <li>Optimize MOSFET selection for lower switching and conduction losses</li>
                    )}
                    {analysis.powerFactor < 0.95 && (
                      <li>Review control algorithm for better input current shaping</li>
                    )}
                    {analysis.thd > 5 && (
                      <li>Add input EMI filtering to reduce harmonic content</li>
                    )}
                    {analysis.voltageRipple > parameters.inputs.v_ripple_max && (
                      <li>Increase output capacitance or use lower ESR capacitors</li>
                    )}
                    <li>Verify thermal management for all power components</li>
                    <li>Conduct PCB layout review to minimize parasitic inductance</li>
                  </ul>

                  <h3 className="text-lg font-semibold mt-6">Next Steps</h3>
                  <ol className="list-decimal pl-5 space-y-2">
                    <li>Review the detailed waveforms and verify all specifications are met</li>
                    <li>Conduct thermal analysis for the selected components</li>
                    <li>Design PCB layout following best practices for power electronics</li>
                    <li>Plan prototype testing and validation procedures</li>
                    <li>Document design decisions and create test plans</li>
                  </ol>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default SimulationResults;
