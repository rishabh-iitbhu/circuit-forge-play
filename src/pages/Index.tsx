import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PFCCalculator } from "@/components/PFCCalculator";
import { BuckCalculator } from "@/components/BuckCalculator";
import { ComponentLibrary } from "@/components/ComponentLibrary";
import { Zap } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Zap className="h-10 w-10 text-primary" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
              Circuit Designer Pro
            </h1>
          </div>
          <p className="text-muted-foreground">
            Design circuits with AI-powered component calculations and grounded theory
          </p>
        </header>

        <div className="mb-8">
          <ComponentLibrary />
        </div>

        <Tabs defaultValue="pfc" className="w-full">
          <TabsList className="grid w-full md:w-auto md:inline-grid grid-cols-2 mb-6">
            <TabsTrigger value="pfc">PFC Circuit</TabsTrigger>
            <TabsTrigger value="buck">Buck Converter</TabsTrigger>
          </TabsList>

          <TabsContent value="pfc">
            <PFCCalculator />
          </TabsContent>

          <TabsContent value="buck">
            <BuckCalculator />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Index;
