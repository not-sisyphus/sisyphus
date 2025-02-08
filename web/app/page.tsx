import * as React from "react";

// import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
// import { Input } from "@/components/ui/input";
// import { Label } from "@/components/ui/label";
// import {
//   Select,
//   SelectContent,
//   SelectItem,
//   SelectTrigger,
//   SelectValue,
// } from "@/components/ui/select";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center pt-10">
      <div className="z-10 w-full overflow-x-auto whitespace-nowrap flex flex-nowrap justify-start gap-4 font-mono text-sm">
        <Card className="w-[350px] h-[400px] flex items-center justify-center text-center shrink-0">
          <h1 className="text-9xl">1</h1>
        </Card>
        <Card className="w-[350px] h-[400px] flex items-center justify-center text-center shrink-0">
          <h1 className="text-9xl">3</h1>
        </Card>
        <Card className="w-[350px] h-[400px] flex items-center justify-center text-center shrink-0">
          <h1 className="text-9xl">5</h1>
        </Card>
        <Card className="w-[350px] h-[400px] flex items-center justify-center text-center shrink-0">
          <h1 className="text-9xl">8</h1>
        </Card>
        <Card className="w-[350px] h-[400px] flex items-center justify-center text-center shrink-0">
          <h1 className="text-9xl">100</h1>
        </Card>
        <Card className="w-[350px] h-[400px] flex items-center justify-center text-center shrink-0">
          <h1 className="text-9xl">☕️</h1>
        </Card>
        <Card className="w-[350px] h-[400px] flex items-center justify-center text-center shrink-0">
          <h1 className="text-9xl">?</h1>
        </Card>
      </div>
    </main>
  );
}
