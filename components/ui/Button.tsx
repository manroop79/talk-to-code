"use client";
import * as React from "react";

function cn(...parts: (string | false | null | undefined)[]) {
    return parts.filter(Boolean).join(" ");
}

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: "primary" | "secondary" | "ghost" | "danger" | "success";
    size?: "sm" | "md";
};

export default function Button({
    className,
    variant = "primary",
    size = "md",
    ...props
    }: Props) {
        const base =
        "inline-flex items-center justify-center rounded-md cursor-pointer select-none " +
        "transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40 " +
        "disabled:opacity-50 disabled:cursor-not-allowed";

    const sizes = {
        sm: "px-3 py-1.5 text-[13px]",
        md: "px-4 py-2 text-sm",
    };

    const variants = {
        primary:
        "bg-white text-black hover:brightness-105 active:brightness-95 shadow",
        secondary:
        "bg-white/10 text-white hover:bg-white/15 active:bg-white/20 border border-white/10",
        ghost:
        "bg-transparent text-white hover:bg-white/10 active:bg-white/15",
        danger:
        "bg-red-500 text-white hover:brightness-110 active:brightness-95",
        success:
        "bg-green-500 text-white hover:bg-green-600 active:bg-green-700",
    };

    return (
        <button
            className={cn(base, sizes[size], variants[variant], className)}
            {...props}
        />
    );
}