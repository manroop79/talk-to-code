// import BackgroundBoxes from "@/components/BackgroundBoxes";

import { ExpandableCard } from "@/components/ui/Features";
import { Hero } from "@/components/ui/Hero";
import { NavbarDemo } from "@/components/ui/Navbar";
import Pricing from "@/components/ui/Pricing";
import { cn } from "@/lib/utils";

export default function HomePage() {
  return (
    <div>
      <NavbarDemo />
      <div className="relative flex flex-col min-h-[30vh] w-full items-center justify-center sm:px-4 md:px-6 bg-white dark:bg-black">
        <div
          className={cn(
            "absolute inset-0",
            "[background-size:40px_40px]",
            "[background-image:linear-gradient(to_right,#e4e4e7_1px,transparent_1px),linear-gradient(to_bottom,#e4e4e7_1px,transparent_1px)]",
            "dark:[background-image:linear-gradient(to_right,#262626_1px,transparent_1px),linear-gradient(to_bottom,#262626_1px,transparent_1px)]"
          )}
        />
        {/* Radial gradient for the container to give a faded look */}
        <div className="pointer-events-none absolute inset-0 z-0 flex items-center justify-center bg-white [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)] dark:bg-black"></div>
        <div className="relative z-10 px-2 py-10 w-full max-w-4xl text-center">
          <Hero />
          <div className="pt-10 space-y-10">

            <section id="features" className="scroll-mt-28">
              <ExpandableCard />
            </section>
            <section id="pricing" className="scroll-mt-28">
              <Pricing />
            </section>
            
          </div>
        </div>
      </div>
    </div>
  );
}