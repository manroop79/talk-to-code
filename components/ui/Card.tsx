"use client"

import { useRouter } from "next/navigation";
import React from "react";

export interface CardProps {
    title: string;
    description: string;
    price: string;
    features: string[];
    highlightColor?: string; // optional color (e.g., 'bg-blue-600')
    buttonText?: string;
}

const Card: React.FC<CardProps> = ({
    title,
    description,
    price,
    features,
    highlightColor = "bg-blue-600", // fallback
    buttonText = "Get Started",
}) => {

    const router = useRouter();

    return (
        <div
            className={`
                group w-full max-w-sm rounded-xl h-full flex flex-col justify-between border border-gray-300 dark:border-gray-600
                bg-transparent dark:bg-white/5 p-6 shadow-md backdrop-blur-md transition-all
                hover:scale-[1.03] hover:${highlightColor} hover:text-white
            `}
        >
            <h3 className="text-sm font-medium text-green-400 group-hover:text-white">{title}</h3>
            <p className="mt-1 text-lg font-semibold">{price}</p>
            <p className="mt-1 text-sm text-gray-300 group-hover:text-white">{description}</p>

            <ul className="mt-4 space-y-2">
            {features.map((item, idx) => (
            <li key={idx} className="text-sm text-gray-300 group-hover:text-white">✅ {item}</li>
            ))}
            </ul>

            <button onClick={() => router.push("/workspace")} className="mt-6 w-full rounded-md bg-white text-black font-medium py-2 transition hover:bg-green-500 hover:text-white cursor-pointer">
                {buttonText}
            </button>
        </div>
);
};

export default Card;