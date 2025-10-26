import { useEffect, useRef, useState } from "react";
import { Canvas as FabricCanvas, FabricObject, Circle, Rect, Line } from "fabric";
import { toast } from "sonner";

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

interface CircuitCanvasProps {
  onComponentSelect: (component: ExtendedFabricObject | null) => void;
  selectedTool: string | null;
}

export const CircuitCanvas = ({ onComponentSelect, selectedTool }: CircuitCanvasProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [fabricCanvas, setFabricCanvas] = useState<FabricCanvas | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    // Prevent double initialization in strict mode
    if (fabricCanvas) return;

    const canvas = new FabricCanvas(canvasRef.current, {
      width: window.innerWidth - 400,
      height: window.innerHeight - 80,
      backgroundColor: "hsl(220, 15%, 15%)",
    });

    // Draw grid
    drawGrid(canvas);

    setFabricCanvas(canvas);

    canvas.on("selection:created", (e) => {
      if (e.selected && e.selected[0]) {
        onComponentSelect(e.selected[0] as ExtendedFabricObject);
      }
    });

    canvas.on("selection:updated", (e) => {
      if (e.selected && e.selected[0]) {
        onComponentSelect(e.selected[0] as ExtendedFabricObject);
      }
    });

    canvas.on("selection:cleared", () => {
      onComponentSelect(null);
    });

    const handleResize = () => {
      canvas.setDimensions({
        width: window.innerWidth - 400,
        height: window.innerHeight - 80,
      });
      drawGrid(canvas);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      canvas.dispose();
    };
  }, [onComponentSelect]);

  const drawGrid = (canvas: FabricCanvas) => {
    const gridSize = 20;
    const width = canvas.width || 0;
    const height = canvas.height || 0;

    // Clear existing grid lines
    canvas.getObjects().forEach((obj) => {
      const extObj = obj as ExtendedFabricObject;
      if (extObj.data?.isGrid) {
        canvas.remove(obj);
      }
    });

    // Vertical lines
    for (let i = 0; i < width; i += gridSize) {
      const line = new Line([i, 0, i, height], {
        stroke: "hsl(220, 20%, 25%)",
        strokeWidth: i % 100 === 0 ? 1 : 0.5,
        selectable: false,
        evented: false,
        opacity: i % 100 === 0 ? 0.3 : 0.1,
      }) as ExtendedFabricObject;
      line.data = { isGrid: true };
      canvas.add(line);
    }

    // Horizontal lines
    for (let i = 0; i < height; i += gridSize) {
      const line = new Line([0, i, width, i], {
        stroke: "hsl(220, 20%, 25%)",
        strokeWidth: i % 100 === 0 ? 1 : 0.5,
        selectable: false,
        evented: false,
        opacity: i % 100 === 0 ? 0.3 : 0.1,
      }) as ExtendedFabricObject;
      line.data = { isGrid: true };
      canvas.add(line);
    }

    const gridObjects = canvas.getObjects().filter((obj) => (obj as ExtendedFabricObject).data?.isGrid);
    gridObjects.forEach((obj) => canvas.sendObjectToBack(obj));
  };

  useEffect(() => {
    if (!fabricCanvas || !selectedTool) return;

    const addComponent = (e: any) => {
      const pointer = fabricCanvas.getPointer(e.e);
      let component: FabricObject | null = null;

      switch (selectedTool) {
        case "resistor":
          component = createResistor(pointer.x, pointer.y);
          break;
        case "capacitor":
          component = createCapacitor(pointer.x, pointer.y);
          break;
        case "inductor":
          component = createInductor(pointer.x, pointer.y);
          break;
        case "mosfet":
          component = createMOSFET(pointer.x, pointer.y);
          break;
        case "diode":
          component = createDiode(pointer.x, pointer.y);
          break;
      }

      if (component) {
        fabricCanvas.add(component);
        fabricCanvas.setActiveObject(component);
        toast.success(`${selectedTool} added`);
      }
    };

    fabricCanvas.on("mouse:down", addComponent);

    return () => {
      fabricCanvas.off("mouse:down", addComponent);
    };
  }, [fabricCanvas, selectedTool]);

  const createResistor = (x: number, y: number) => {
    const rect = new Rect({
      left: x,
      top: y,
      width: 80,
      height: 30,
      fill: "transparent",
      stroke: "hsl(210, 100%, 55%)",
      strokeWidth: 3,
      rx: 5,
      ry: 5,
    }) as ExtendedFabricObject;
    rect.data = { type: "resistor", value: "1k", unit: "Ω" };
    return rect;
  };

  const createCapacitor = (x: number, y: number) => {
    const rect = new Rect({
      left: x,
      top: y,
      width: 60,
      height: 40,
      fill: "transparent",
      stroke: "hsl(180, 100%, 50%)",
      strokeWidth: 3,
      rx: 3,
      ry: 3,
    }) as ExtendedFabricObject;
    rect.data = { type: "capacitor", value: "10", unit: "µF" };
    return rect;
  };

  const createInductor = (x: number, y: number) => {
    const circle = new Circle({
      left: x,
      top: y,
      radius: 25,
      fill: "transparent",
      stroke: "hsl(142, 76%, 45%)",
      strokeWidth: 3,
    }) as ExtendedFabricObject;
    circle.data = { type: "inductor", value: "100", unit: "µH" };
    return circle;
  };

  const createMOSFET = (x: number, y: number) => {
    const rect = new Rect({
      left: x,
      top: y,
      width: 50,
      height: 60,
      fill: "transparent",
      stroke: "hsl(38, 92%, 50%)",
      strokeWidth: 3,
    }) as ExtendedFabricObject;
    rect.data = { type: "mosfet", value: "N-Channel", model: "IRF540" };
    return rect;
  };

  const createDiode = (x: number, y: number) => {
    const rect = new Rect({
      left: x,
      top: y,
      width: 40,
      height: 40,
      fill: "transparent",
      stroke: "hsl(0, 84%, 60%)",
      strokeWidth: 3,
      angle: 45,
    }) as ExtendedFabricObject;
    rect.data = { type: "diode", value: "1N4007" };
    return rect;
  };

  const handleClear = () => {
    if (!fabricCanvas) return;
    fabricCanvas.getObjects().forEach((obj) => {
      const extObj = obj as ExtendedFabricObject;
      if (!extObj.data?.isGrid) {
        fabricCanvas.remove(obj);
      }
    });
    toast.success("Canvas cleared");
  };

  return (
    <div className="relative flex-1 border border-border rounded-lg overflow-hidden">
      <canvas ref={canvasRef} />
    </div>
  );
};
