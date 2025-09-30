"use client";

import { useRouter } from "next/navigation";
import { TypewriterEffectSmooth } from "./TypeWriter";

export function Hero() {

  const router = useRouter();

  const words = [
    {
      text: "Understand",
    },
    {
      text: "code",
    },
    {
      text: "instantly",
    },
    {
      text: "with",
    },
    {
      text: "EchoCode.",
      className: "text-green-500 dark:text-green-500",
    },
  ];
  return (
    <div className="flex flex-col items-center justify-center min-h-[16rem]">
      <p className="text-neutral-600 dark:text-neutral-200 text-xs sm:text-base  ">
        Talk to your code like never before.
      </p>
      <TypewriterEffectSmooth words={words} />
      <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 space-x-0 md:space-x-4">
        <button onClick={() => router.push("/workspace")} className="w-40 h-10 rounded-xl bg-white text-black text-sm transition-transform duration-200 hover:font-bold hover:scale-105 hover:bg-green-500 hover:text-white border border-gray-600 dark:border-gray-950 cursor-pointer">
          Get Started
        </button>
      </div>
    </div>
  );
}