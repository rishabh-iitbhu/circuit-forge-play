import { Card } from "@/components/ui/card";
import { Zap, Circle, Waves, Box, TrendingUp } from "lucide-react";

interface ComponentLibraryProps {
  onSelectTool: (tool: string) => void;
  selectedTool: string | null;
}

export const ComponentLibrary = ({ onSelectTool, selectedTool }: ComponentLibraryProps) => {
  const components = [
    { id: "resistor", name: "Resistor", icon: Box, color: "hsl(210, 100%, 55%)" },
    { id: "capacitor", name: "Capacitor", icon: Waves, color: "hsl(180, 100%, 50%)" },
    { id: "inductor", name: "Inductor", icon: Circle, color: "hsl(142, 76%, 45%)" },
    { id: "mosfet", name: "MOSFET", icon: Zap, color: "hsl(38, 92%, 50%)" },
    { id: "diode", name: "Diode", icon: TrendingUp, color: "hsl(0, 84%, 60%)" },
  ];

  return (
    <div className="w-64 border-r border-border bg-card p-4 overflow-y-auto">
      <h2 className="text-lg font-bold mb-4 text-primary">Component Library</h2>
      <div className="space-y-2">
        {components.map((comp) => {
          const Icon = comp.icon;
          const isSelected = selectedTool === comp.id;
          return (
            <Card
              key={comp.id}
              className={`p-3 cursor-pointer transition-all hover:border-component-hover ${
                isSelected ? "border-primary bg-secondary" : ""
              }`}
              onClick={() => onSelectTool(comp.id)}
            >
              <div className="flex items-center gap-3">
                <Icon style={{ color: comp.color }} size={24} />
                <span className="font-medium text-sm">{comp.name}</span>
              </div>
            </Card>
          );
        })}
      </div>

      <div className="mt-8">
        <h3 className="text-sm font-semibold mb-2 text-muted-foreground">Instructions</h3>
        <p className="text-xs text-muted-foreground leading-relaxed">
          Select a component from the library, then click on the canvas to place it. Click on
          placed components to edit their properties.
        </p>
      </div>
    </div>
  );
};
