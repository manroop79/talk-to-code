"use client"

import React from "react";
import Card from "./Card";

const CardGrid: React.FC = () => {
    const cards = [
        {
            title: "Starter",
            price: "$0/mo",
            description: "Best for trying EchoCode on a small project",
            features: [
            "1 project, up to 100 MB per upload",
            "50K tokens indexed per month",
            "GPT-3.5 answers with citations & streaming",
            "Basic email support",
            ],
            highlightColor: "bg-blue-600",
            },
            {
            title: "Pro",
            price: "$29/mo",
            description: "For solo devs and small teams using EchoCode weekly",
            features: [
            "10 projects, up to 2 GB per upload",
            "2M tokens indexed per month",
            "Faster answers, choose models (3.5 / 4o-mini)",
            "Priority support (24–48h)",
            ],
            highlightColor: "bg-black",
            },
            {
            title: "Enterprise",
            price: "Contact Us",
            description: "Tailored for security-focused teams & larger codebases",
            features: [
            "Unlimited projects & higher limits",
            "SSO/SAML, audit logs & SLAs",
            "Private networking options",
            "Dedicated support & onboarding",
            ],
            highlightColor: "bg-purple-600",
        },
    ];
        

return (
    <div className="flex flex-col items-center justify-center gap-6 px-4 py-12 sm:px-6 md:flex-row md:gap-8 md:py-20">
        {cards.map((card, idx) => (
            <Card key={idx} {...card} /> //takes all the properties inside the card object and spreads them individually inside the card component
        ))}
    </div>
    );
};

export default CardGrid;