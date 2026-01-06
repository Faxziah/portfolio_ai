"use client"

import { Button } from "@/components/ui/button"
import { ChevronDown } from "lucide-react"

interface HeroButtonsProps {
  viewProjectsText: string
  contactMeText: string
}

export function HeroButtons({ viewProjectsText, contactMeText }: HeroButtonsProps) {
  const scrollToSection = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" })
  }

  return (
    <>
      <div className="flex flex-wrap items-center justify-center gap-4">
        <Button
          size="lg"
          onClick={() => scrollToSection("projects")}
          className="bg-gradient-to-r from-primary via-secondary to-accent hover:scale-105 transition-transform shadow-lg cursor-pointer"
        >
          {viewProjectsText}
        </Button>
        <Button
          size="lg"
          variant="outline"
          onClick={() => scrollToSection("contact")}
          className="border-2 border-primary/50 hover:border-primary hover:bg-primary/10 hover:text-primary hover:scale-105 transition-all duration-300 shadow-sm hover:shadow-md cursor-pointer"
        >
          {contactMeText}
        </Button>
      </div>

      <div
        className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce cursor-pointer hover:scale-110 transition-transform"
        onClick={() => scrollToSection("about")}
      >
        <ChevronDown className="h-8 w-8 text-primary" />
      </div>
    </>
  )
}
