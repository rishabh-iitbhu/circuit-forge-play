import { useState } from "react";
import { FabricObject } from "fabric";
import { Toolbar } from "@/components/Toolbar";
import { ComponentLibrary } from "@/components/ComponentLibrary";
import { CircuitCanvas } from "@/components/CircuitCanvas";
import { PropertiesPanel } from "@/components/PropertiesPanel";

interface ComponentData {
  isGrid?: boolean;
  type?: string;
  value?: string;
  unit?: string;
  model?: string;
}

interface ExtendedFabricObject extends FabricObject {
  data?: ComponentData;
}

const Index = () => {
  const [selectedTool, setSelectedTool] = useState<string | null>(null);
  const [selectedComponent, setSelectedComponent] = useState<ExtendedFabricObject | null>(null);

  return (
    <div className="h-screen flex flex-col bg-background text-foreground">
      <Toolbar />
      <div className="flex-1 flex overflow-hidden">
        <ComponentLibrary onSelectTool={setSelectedTool} selectedTool={selectedTool} />
        <CircuitCanvas onComponentSelect={setSelectedComponent} selectedTool={selectedTool} />
        <PropertiesPanel selectedComponent={selectedComponent} />
      </div>
    </div>
  );
};

export default Index;
