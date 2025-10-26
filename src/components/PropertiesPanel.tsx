import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { FabricObject } from "fabric";
import { useState, useEffect } from "react";

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

interface PropertiesPanelProps {
  selectedComponent: ExtendedFabricObject | null;
}

export const PropertiesPanel = ({ selectedComponent }: PropertiesPanelProps) => {
  const [value, setValue] = useState("");
  const [unit, setUnit] = useState("");

  useEffect(() => {
    if (selectedComponent?.data) {
      setValue(selectedComponent.data.value || "");
      setUnit(selectedComponent.data.unit || "");
    }
  }, [selectedComponent]);

  if (!selectedComponent) {
    return (
      <div className="w-80 border-l border-border bg-card p-4">
        <h2 className="text-lg font-bold mb-4 text-primary">Properties</h2>
        <p className="text-sm text-muted-foreground">
          Select a component to view and edit its properties
        </p>
      </div>
    );
  }

  const componentType = selectedComponent.data?.type || "Unknown";

  return (
    <div className="w-80 border-l border-border bg-card p-4 overflow-y-auto">
      <h2 className="text-lg font-bold mb-4 text-primary">Properties</h2>

      <Card className="p-4 mb-4 bg-secondary">
        <div className="text-sm">
          <div className="font-semibold text-accent mb-1">Component Type</div>
          <div className="capitalize text-foreground">{componentType}</div>
        </div>
      </Card>

      <div className="space-y-4">
        <div>
          <Label htmlFor="value" className="text-sm font-medium">
            Value
          </Label>
          <Input
            id="value"
            value={value}
            onChange={(e) => {
              setValue(e.target.value);
              if (selectedComponent.data) {
                selectedComponent.data.value = e.target.value;
              }
            }}
            className="mt-1 font-mono"
            placeholder="Enter value"
          />
        </div>

        {unit && (
          <div>
            <Label htmlFor="unit" className="text-sm font-medium">
              Unit
            </Label>
            <Input
              id="unit"
              value={unit}
              onChange={(e) => {
                setUnit(e.target.value);
                if (selectedComponent.data) {
                  selectedComponent.data.unit = e.target.value;
                }
              }}
              className="mt-1 font-mono"
              placeholder="Unit"
            />
          </div>
        )}

        <div className="pt-4 border-t border-border">
          <h3 className="text-sm font-semibold mb-3 text-muted-foreground">Position</h3>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <Label className="text-xs">X</Label>
              <div className="text-sm font-mono text-foreground mt-1">
                {selectedComponent.left?.toFixed(0)}px
              </div>
            </div>
            <div>
              <Label className="text-xs">Y</Label>
              <div className="text-sm font-mono text-foreground mt-1">
                {selectedComponent.top?.toFixed(0)}px
              </div>
            </div>
          </div>
        </div>

        {componentType === "mosfet" && (
          <Card className="p-3 bg-secondary/50 mt-4">
            <div className="text-xs text-muted-foreground">
              <div className="font-semibold mb-1">MOSFET Specifications</div>
              <div className="space-y-1">
                <div>Model: {selectedComponent.data?.model || "N/A"}</div>
                <div>Type: {selectedComponent.data?.value || "N/A"}</div>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};
