import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { mosfetLibrary, capacitorLibrary, inductorLibrary } from "@/lib/componentData";
import { Cpu, Battery, Codesandbox } from "lucide-react";

export const ComponentLibrary = () => {
  return (
    <div className="w-full">
      <Tabs defaultValue="mosfets" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="mosfets">
            <Cpu className="h-4 w-4 mr-2" />
            MOSFETs
          </TabsTrigger>
          <TabsTrigger value="capacitors">
            <Battery className="h-4 w-4 mr-2" />
            Capacitors
          </TabsTrigger>
          <TabsTrigger value="inductors">
            <Codesandbox className="h-4 w-4 mr-2" />
            Inductors
          </TabsTrigger>
        </TabsList>

        <TabsContent value="mosfets" className="mt-4">
          <div className="rounded-md border overflow-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>MOSFET Name</TableHead>
                  <TableHead>Manufacturer</TableHead>
                  <TableHead className="text-right">V<sub>DS</sub> (V)</TableHead>
                  <TableHead className="text-right">I<sub>D</sub> (A)</TableHead>
                  <TableHead className="text-right">R<sub>DS(on)</sub> (mΩ)</TableHead>
                  <TableHead className="text-right">Q<sub>g</sub> (nC)</TableHead>
                  <TableHead>Package</TableHead>
                  <TableHead>Typical Use</TableHead>
                  <TableHead>Efficiency</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mosfetLibrary.map((mosfet) => (
                  <TableRow key={mosfet.name}>
                    <TableCell className="font-medium">{mosfet.name}</TableCell>
                    <TableCell>{mosfet.manufacturer}</TableCell>
                    <TableCell className="text-right">{mosfet.vds}</TableCell>
                    <TableCell className="text-right">{mosfet.id}</TableCell>
                    <TableCell className="text-right">{mosfet.rdson}</TableCell>
                    <TableCell className="text-right">{mosfet.qg}</TableCell>
                    <TableCell>{mosfet.package}</TableCell>
                    <TableCell className="text-sm text-muted-foreground">{mosfet.typicalUse}</TableCell>
                    <TableCell className="text-sm">{mosfet.efficiencyRange}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </TabsContent>

        <TabsContent value="capacitors" className="mt-4">
          <div className="rounded-md border overflow-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Part Number</TableHead>
                  <TableHead>Manufacturer</TableHead>
                  <TableHead className="text-right">Capacitance (µF)</TableHead>
                  <TableHead className="text-right">Voltage (V)</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead className="text-right">ESR (mΩ)</TableHead>
                  <TableHead>Primary Use</TableHead>
                  <TableHead>Temp Range (°C)</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {capacitorLibrary.map((cap) => (
                  <TableRow key={cap.partNumber}>
                    <TableCell className="font-medium">{cap.partNumber}</TableCell>
                    <TableCell>{cap.manufacturer}</TableCell>
                    <TableCell className="text-right">{cap.capacitance}</TableCell>
                    <TableCell className="text-right">{cap.voltage}</TableCell>
                    <TableCell>{cap.type}</TableCell>
                    <TableCell className="text-right">{cap.esr}</TableCell>
                    <TableCell className="text-sm text-muted-foreground">{cap.primaryUse}</TableCell>
                    <TableCell className="text-sm">{cap.tempRange}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </TabsContent>

        <TabsContent value="inductors" className="mt-4">
          <div className="rounded-md border overflow-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Part Number</TableHead>
                  <TableHead>Manufacturer</TableHead>
                  <TableHead className="text-right">Inductance (µH)</TableHead>
                  <TableHead className="text-right">Current (A)</TableHead>
                  <TableHead className="text-right">DCR (mΩ)</TableHead>
                  <TableHead className="text-right">I<sub>sat</sub> (A)</TableHead>
                  <TableHead>Package</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {inductorLibrary.map((ind) => (
                  <TableRow key={ind.partNumber}>
                    <TableCell className="font-medium">{ind.partNumber}</TableCell>
                    <TableCell>{ind.manufacturer}</TableCell>
                    <TableCell className="text-right">{ind.inductance}</TableCell>
                    <TableCell className="text-right">{ind.current}</TableCell>
                    <TableCell className="text-right">{ind.dcr}</TableCell>
                    <TableCell className="text-right">{ind.satCurrent}</TableCell>
                    <TableCell>{ind.package}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};
