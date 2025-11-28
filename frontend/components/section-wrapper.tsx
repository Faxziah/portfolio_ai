"use client"

import { type ReactNode } from "react"
import { cn } from "@/lib/utils"

interface SectionWrapperProps {
  id: string
  title: string
  children: ReactNode
  className?: string
  background?: "default" | "muted"
}

export function SectionWrapper({ id, title, children, className, background = "default" }: SectionWrapperProps) {
  return (
    <section
      id={id}
      className={cn(
        "py-20 scroll-mt-20",
        background === "muted" ? "bg-muted/30" : "",
        className
      )}
    >
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">{title}</h2>
        {children}
      </div>
    </section>
  )
}

