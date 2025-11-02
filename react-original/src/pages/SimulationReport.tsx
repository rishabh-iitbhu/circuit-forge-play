import { useEffect, useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { ArrowLeft, Download, FileText, TrendingUp, Award, AlertCircle } from 'lucide-react';
import { SimulationReport } from '@/types/permutation';
import { generatePDFReport, generateCSVReport } from '@/lib/reportGenerator';

export default function SimulationReportPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [report, setReport] = useState<SimulationReport | null>(null);

  useEffect(() => {
    if (location.state?.report) {
      setReport(location.state.report);
    } else {
      navigate('/');
    }
  }, [location.state, navigate]);

  if (!report) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="p-6">
          <p className="text-muted-foreground">Loading report...</p>
        </Card>
      </div>
    );
  }

  const best = report.bestPermutation;

  const getRankBadge = (rank: number) => {
    if (rank === 1) return <Badge className="bg-yellow-500">🥇 Best</Badge>;
    if (rank === 2) return <Badge className="bg-gray-400">🥈 2nd</Badge>;
    if (rank === 3) return <Badge className="bg-orange-600">🥉 3rd</Badge>;
    return <Badge variant="outline">#{rank}</Badge>;
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="outline" size="icon" asChild>
                <Link to="/">
                  <ArrowLeft className="w-4 h-4" />
                </Link>
              </Button>
              <div>
                <h1 className="text-3xl font-bold">{report.circuitType} Simulation Report</h1>
                <p className="text-sm text-muted-foreground mt-1">
                  Generated {new Date(report.timestamp).toLocaleString()} • {report.permutations.length} permutations tested
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => generateCSVReport(report)} className="gap-2">
                <FileText className="w-4 h-4" />
                Download CSV
              </Button>
              <Button onClick={() => generatePDFReport(report)} className="gap-2">
                <Download className="w-4 h-4" />
                Download PDF
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Best Configuration Card */}
        <Card className="mb-8 border-2 border-primary">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Award className="w-5 h-5 text-primary" />
              Recommended Configuration
            </CardTitle>
            <CardDescription>
              Best performing combination based on: {report.priorityMetrics.join(', ')}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div>
                <h3 className="font-semibold mb-2">Components</h3>
                <div className="space-y-1 text-sm">
                  <p><strong>MOSFET:</strong> {best.components.mosfet.part_number}</p>
                  <p><strong>Capacitor:</strong> {best.components.capacitor.part_number}</p>
                  <p><strong>Inductor:</strong> {best.components.inductor.part_number}</p>
                </div>
              </div>
              <div>
                <h3 className="font-semibold mb-2">Efficiency</h3>
                <p className="text-3xl font-bold text-primary">{(best.metrics.efficiency * 100).toFixed(2)}%</p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">Power Factor</h3>
                <p className="text-3xl font-bold">{best.metrics.powerFactor.toFixed(3)}</p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">THD</h3>
                <p className="text-3xl font-bold">{(best.metrics.thd * 100).toFixed(2)}%</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Tabs */}
        <Tabs defaultValue="summary" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="summary">Summary</TabsTrigger>
            <TabsTrigger value="detailed">All Permutations</TabsTrigger>
            <TabsTrigger value="analysis">Analysis & Recommendations</TabsTrigger>
          </TabsList>

          {/* Summary Tab */}
          <TabsContent value="summary" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Top 5 Configurations</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Rank</TableHead>
                      <TableHead>MOSFET</TableHead>
                      <TableHead>Capacitor</TableHead>
                      <TableHead>Inductor</TableHead>
                      <TableHead>Efficiency</TableHead>
                      <TableHead>Power Factor</TableHead>
                      <TableHead>THD</TableHead>
                      <TableHead>Score</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {report.permutations.slice(0, 5).map((perm) => (
                      <TableRow key={perm.id}>
                        <TableCell>{getRankBadge(perm.rank || 0)}</TableCell>
                        <TableCell className="font-mono text-sm">{perm.components.mosfet.part_number}</TableCell>
                        <TableCell className="font-mono text-sm">{perm.components.capacitor.part_number}</TableCell>
                        <TableCell className="font-mono text-sm">{perm.components.inductor.part_number}</TableCell>
                        <TableCell>{(perm.metrics.efficiency * 100).toFixed(2)}%</TableCell>
                        <TableCell>{perm.metrics.powerFactor.toFixed(3)}</TableCell>
                        <TableCell>{(perm.metrics.thd * 100).toFixed(2)}%</TableCell>
                        <TableCell className="font-semibold">{perm.score?.toFixed(4)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          {/* All Permutations Tab */}
          <TabsContent value="detailed" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>All {report.permutations.length} Permutations</CardTitle>
                <CardDescription>Complete comparison of all tested component combinations</CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[600px]">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Rank</TableHead>
                        <TableHead>MOSFET</TableHead>
                        <TableHead>Capacitor</TableHead>
                        <TableHead>Inductor</TableHead>
                        <TableHead>Efficiency</TableHead>
                        <TableHead>PF</TableHead>
                        <TableHead>THD</TableHead>
                        <TableHead>V Ripple</TableHead>
                        <TableHead>I Ripple</TableHead>
                        <TableHead>Peak I</TableHead>
                        <TableHead>Score</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {report.permutations.map((perm) => (
                        <TableRow key={perm.id} className={perm.rank === 1 ? 'bg-primary/5' : ''}>
                          <TableCell>{getRankBadge(perm.rank || 0)}</TableCell>
                          <TableCell className="font-mono text-xs">{perm.components.mosfet.part_number}</TableCell>
                          <TableCell className="font-mono text-xs">{perm.components.capacitor.part_number}</TableCell>
                          <TableCell className="font-mono text-xs">{perm.components.inductor.part_number}</TableCell>
                          <TableCell>{(perm.metrics.efficiency * 100).toFixed(2)}%</TableCell>
                          <TableCell>{perm.metrics.powerFactor.toFixed(3)}</TableCell>
                          <TableCell>{(perm.metrics.thd * 100).toFixed(2)}%</TableCell>
                          <TableCell>{perm.metrics.voltageRipple.toFixed(2)}V</TableCell>
                          <TableCell>{perm.metrics.currentRipple.toFixed(2)}A</TableCell>
                          <TableCell>{perm.metrics.peakCurrent.toFixed(2)}A</TableCell>
                          <TableCell className="font-semibold">{perm.score?.toFixed(4)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Analysis Tab */}
          <TabsContent value="analysis" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  Performance Analysis
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="font-semibold text-lg mb-3">Key Findings</h3>
                  <ul className="space-y-2">
                    <li className="flex items-start gap-2">
                      <span className="text-primary mt-1">•</span>
                      <span>Best efficiency achieved: <strong>{(best.metrics.efficiency * 100).toFixed(2)}%</strong> with {best.components.mosfet.part_number}</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-primary mt-1">•</span>
                      <span>Highest power factor: <strong>{best.metrics.powerFactor.toFixed(3)}</strong></span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-primary mt-1">•</span>
                      <span>Lowest THD: <strong>{(best.metrics.thd * 100).toFixed(2)}%</strong></span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-primary mt-1">•</span>
                      <span>Peak current: <strong>{best.metrics.peakCurrent.toFixed(2)}A</strong></span>
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-lg mb-3">Recommendations</h3>
                  <div className="space-y-3">
                    <Card className="border-l-4 border-l-green-500">
                      <CardContent className="pt-4">
                        <p className="font-semibold text-green-700 dark:text-green-400 mb-1">✓ Recommended</p>
                        <p className="text-sm">
                          Use <strong>{best.components.mosfet.part_number}</strong>, <strong>{best.components.capacitor.part_number}</strong>, 
                          and <strong>{best.components.inductor.part_number}</strong> for optimal performance based on your priority metrics.
                        </p>
                      </CardContent>
                    </Card>

                    {report.permutations.length > 1 && (
                      <Card className="border-l-4 border-l-blue-500">
                        <CardContent className="pt-4">
                          <p className="font-semibold text-blue-700 dark:text-blue-400 mb-1">ℹ Alternative</p>
                          <p className="text-sm">
                            Rank #2 configuration achieves {((report.permutations[1].score || 0) / (best.score || 1) * 100).toFixed(1)}% 
                            of best performance and may be considered if cost or availability is a concern.
                          </p>
                        </CardContent>
                      </Card>
                    )}

                    <Card className="border-l-4 border-l-orange-500">
                      <CardContent className="pt-4">
                        <p className="font-semibold text-orange-700 dark:text-orange-400 mb-1 flex items-center gap-1">
                          <AlertCircle className="w-4 h-4" />
                          Important
                        </p>
                        <p className="text-sm">
                          These simulations use idealized models. Always verify performance with physical prototypes 
                          and consider thermal management, EMI, and safety margins in your final design.
                        </p>
                      </CardContent>
                    </Card>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-lg mb-3">Next Steps</h3>
                  <ol className="space-y-2 list-decimal list-inside">
                    <li>Order components for the recommended configuration</li>
                    <li>Design PCB layout with proper thermal and EMI considerations</li>
                    <li>Build prototype and validate performance under real-world conditions</li>
                    <li>Perform thermal testing and adjust heatsinking as needed</li>
                    <li>Conduct EMC testing and add filtering if necessary</li>
                  </ol>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
