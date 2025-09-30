"use client";

import React, { useEffect, useId, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { useOutsideClick } from "@/hooks/useOutside";
import { useRouter } from "next/navigation";
import { FaUpload, FaQuestionCircle, FaBolt, FaFolderOpen, FaLink } from "react-icons/fa"; // Example icons

export function ExpandableCard() {
  const [active, setActive] = useState<(typeof cards)[number] | boolean | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  const id = useId();
  const router = useRouter();

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setActive(false);
      }
    }

    if (active && typeof active === "object") {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [active]);

  useOutsideClick(ref, () => setActive(null));

  return (
    <>
      <AnimatePresence>
        {active && typeof active === "object" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/20 h-full w-full z-10"
          />
        )}
      </AnimatePresence>
      <AnimatePresence>
        {active && typeof active === "object" ? (
          <div className="fixed inset-0  grid place-items-center z-[100]">
            <motion.button
              key={`button-${active.title}-${id}`}
              layout
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{
                opacity: 0,
                transition: { duration: 0.05 },
              }}
              className="flex absolute top-2 right-2 lg:hidden items-center justify-center bg-white rounded-full h-6 w-6"
              onClick={() => setActive(null)}
            >
              <CloseIcon />
            </motion.button>
            <motion.div
              layoutId={`card-${active.title}-${id}`}
              ref={ref}
              className="w-full max-w-[500px]  h-full md:h-fit md:max-h-[90%]  flex flex-col bg-white dark:bg-neutral-900 sm:rounded-3xl overflow-hidden"
            >
              <motion.div layoutId={`icon-${active.title}-${id}`} className="flex justify-center items-center py-8">
                {active.icon}
              </motion.div>
              <div>
                <div className="flex justify-between items-start p-4">
                  <div className="">
                    <motion.h3
                      layoutId={`title-${active.title}-${id}`}
                      className="font-bold text-neutral-700 dark:text-neutral-200"
                    >
                      {active.title}
                    </motion.h3>
                    <motion.p
                      layoutId={`description-${active.description}-${id}`}
                      className="text-neutral-600 dark:text-neutral-400"
                    >
                      {active.description}
                    </motion.p>
                  </div>
                  <motion.button
                    layoutId={`button-${active.title}-${id}`}
                    className="px-4 py-3 text-sm rounded-full font-bold bg-green-500 text-white cursor-pointer transition"
                    onClick={() => router.push("/workspace")}
                  >
                    {active.ctaText}
                  </motion.button>
                </div>
                <div className="pt-4 relative px-4">
                  <motion.div
                    layout
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="text-neutral-600 text-xs md:text-sm lg:text-base h-40 md:h-fit pb-10 flex flex-col items-start gap-4 overflow-auto dark:text-neutral-400 [mask:linear-gradient(to_bottom,white,white,transparent)] [scrollbar-width:none] [-ms-overflow-style:none] [-webkit-overflow-scrolling:touch]"
                  >
                    {typeof active.content === "function"
                      ? active.content()
                      : active.content}
                  </motion.div>
                </div>
              </div>
            </motion.div>
          </div>
        ) : null}
      </AnimatePresence>
      <ul className="max-w-2xl mx-auto w-full gap-4">
        {cards.map((card, index) => (
          <motion.div
            layoutId={`card-${card.title}-${id}`}
            key={`card-${card.title}-${id}`}
            onClick={() => setActive(card)}
            className="p-4 mb-4 md:mb-2 flex flex-col md:flex-row md:justify-between md:items-center hover:bg-neutral-50 dark:hover:bg-neutral-800 rounded-xl cursor-pointer"
          >
            <div className="flex gap-4 flex-col items-center md:flex-row md:items-start">
              <motion.div layoutId={`icon-${card.title}-${id}`} className="flex items-center justify-center h-14 w-14 rounded-lg bg-gray-100">
                {card.icon}
              </motion.div>
              <div className="">
                <motion.h3
                  layoutId={`title-${card.title}-${id}`}
                  className="font-medium text-neutral-800 dark:text-neutral-200 text-center md:text-left"
                >
                  {card.title}
                </motion.h3>
                <motion.p
                  layoutId={`description-${card.description}-${id}`}
                  className="text-neutral-600 dark:text-neutral-400 text-center md:text-left"
                >
                  {card.description}
                </motion.p>
              </div>
            </div>
            <motion.button
              layoutId={`button-${card.title}-${id}`}
              className="px-4 py-2 text-sm rounded-full font-bold bg-gray-100 hover:bg-green-500 hover:text-white text-black mt-4 md:mt-0 self-center md:self-auto cursor-pointer transition"
            >
              {card.ctaText}
            </motion.button>
          </motion.div>
        ))}
      </ul>
    </>
  );
}

export const CloseIcon = () => {
  return (
    <motion.svg
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{
        opacity: 0,
        transition: { duration: 0.05 },
      }}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-4 w-4 text-black"
    >
      <path stroke="none" d="M0 0h24v24H0z" fill="none" />
      <path d="M18 6l-12 12" />
      <path d="M6 6l12 12" />
    </motion.svg>
  );
};

// Replace images with icons
const cards = [
  {
    description: "Upload a ZIP and leave the rest to us",
    title: "Add your project",
    icon: <FaUpload size={40} className="text-green-500" />,
    ctaText: "Learn more",
    ctaLink: "https://ui.aceternity.com/templates",
    content: () => (
      <p>
        Drop a ZIP of your code, we then scan the files, organize what&apos;s inside 
        and then you can ask questions about your project right away.
      </p>
    ),
  },
  {
    description: "Type a question like you would to a teammate",
    title: "Ask your code anything",
    icon: <FaQuestionCircle size={40} className="text-blue-500" />,
    ctaText: "Learn more",
    ctaLink: "https://ui.aceternity.com/templates",
    content: () => (
      <p>
        Just ask in plain English-&quot;What does this file do?&quot; or &quot;Where do we check login?&quot;
        and EchoCode will read through your project to give a clear, helpful answer.
      </p>
    ),
  },
  {
    description: "Text appears as it's written-easy to read",
    title: "Fast, readable replies",
    icon: <FaBolt size={40} className="text-yellow-500" />,
    ctaText: "Learn more",
    ctaLink: "https://ui.aceternity.com/templates",
    content: () => (
      <p>
        Replies appear live as they&apos;re generated, with clean formatting making it feel
        quick and keeping you in the flow while you work.
      </p>
    ),
  },
  {
    description: "Swich between uploads any time",
    title: "Keep multiple projects",
    icon: <FaFolderOpen size={40} className="text-purple-500" />,
    ctaText: "Learn more",
    ctaLink: "https://ui.aceternity.com/templates",
    content: () => (
      <p>
        You can keep more than one project and switch between them whenever you like.
        Your recent uploads are listed neatly making it easy to return to something you were working
        on earlier.
      </p>
    ),
  },
  {
    description: "See exactly where the answer came from",
    title: "Answer with sources",
    icon: <FaLink size={40} className="text-gray-500" />,
    ctaText: "Learn more",
    ctaLink: "https://ui.aceternity.com/templates",
    content: () => (
      <p>
        Every answer includes links back to the exact files and lines used. Click a source to jump straight
        to it, so you always know why a result is correct and where it lives in your project
      </p>
    ),
  },
];