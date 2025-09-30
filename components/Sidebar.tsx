import React, { ReactNode } from "react";

type SidebarProps = {
  children: ReactNode;
};

export default function Sidebar({ children }: SidebarProps) {
  return (
    <div className="w-80 bg-neutral-900 p-4">
      {children}
    </div>
  );
}