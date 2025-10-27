import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { PFCCalculator } from "@/components/PFCCalculator";
import { BuckCalculator } from "@/components/BuckCalculator";
import { ComponentLibrary } from "@/components/ComponentLibrary";
import { Zap, Library } from "lucide-react";

const Index = () => {
  const [libraryOpen, setLibraryOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <Zap className="h-10 w-10 text-primary" />
              <h1 className="text-4xl font-bold bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
                Circuit Designer Pro
              </h1>
            </div>
            <Sheet open={libraryOpen} onOpenChange={setLibraryOpen}>
              <SheetTrigger asChild>
                <Button variant="outline" className="gap-2">
                  <Library className="h-4 w-4" />
                  Component Library
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-full sm:max-w-4xl overflow-y-auto">
                <SheetHeader>
                  <SheetTitle>Component Library</SheetTitle>
                  <SheetDescription>
                    Browse available MOSFETs, capacitors, and inductors for your circuit designs
                  </SheetDescription>
                </SheetHeader>
                <div className="mt-6">
                  <ComponentLibrary />
                </div>
              </SheetContent>
            </Sheet>
          </div>
          <p className="text-muted-foreground">
            Design circuits with AI-powered component calculations and grounded theory
          </p>
        </header>

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
