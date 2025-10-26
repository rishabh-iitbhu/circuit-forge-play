import { Button } from "@/components/ui/button";
import { Download, Trash2, Save, Settings } from "lucide-react";
import { toast } from "sonner";

export const Toolbar = () => {
  const handleSave = () => {
    toast.success("Circuit design saved");
  };

  const handleExport = () => {
    toast.success("Exporting design...");
  };

  return (
    <div className="h-16 border-b border-border bg-card px-6 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
          Circuit Designer Pro
        </h1>
        <div className="text-xs text-muted-foreground">v1.0</div>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="outline" size="sm" onClick={handleSave}>
          <Save className="h-4 w-4 mr-2" />
          Save
        </Button>
        <Button variant="outline" size="sm" onClick={handleExport}>
          <Download className="h-4 w-4 mr-2" />
          Export
        </Button>
        <Button variant="outline" size="sm">
          <Settings className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
};
