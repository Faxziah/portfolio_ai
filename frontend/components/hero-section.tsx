"use client"

import { Button } from "@/components/ui/button"
import { ChevronDown } from "lucide-react"
import { useApp } from "@/context/app-context"

export function HeroSection() {
  const { t, resumeData, language } = useApp()

  const scrollToSection = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" })
  }

  const name = resumeData?.name?.[language] || ""
  const heroTitle = resumeData?.resume_title?.[language] || ""
  const heroDescription = resumeData?.resume_description?.[language] || ""

  return (
    <section className="min-h-screen flex items-center justify-center relative pt-20 overflow-hidden">
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-float [animation-delay:1s]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-accent/10 rounded-full blur-3xl animate-float [animation-delay:2s]" />
      </div>

      <div className="container mx-auto px-4 text-center">
        <div className="animate-fade-in">
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-primary via-secondary to-accent text-gradient">{name}</span>
          </h1>
          <h2 className="text-2xl md:text-4xl font-semibold mb-6 text-foreground whitespace-pre-line">{heroTitle}</h2>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8 leading-relaxed">
            {heroDescription}
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4">
            <Button
              size="lg"
              onClick={() => scrollToSection("projects")}
              className="bg-gradient-to-r from-primary via-secondary to-accent hover:scale-105 transition-transform shadow-lg cursor-pointer"
            >
              {t("viewProjects")}
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => scrollToSection("contact")}
              className="border-2 border-primary/50 hover:border-primary hover:bg-primary/10 hover:text-primary hover:scale-105 transition-all duration-300 shadow-sm hover:shadow-md cursor-pointer"
            >
              {t("contactMe")}
            </Button>
          </div>
        </div>

        <div 
          className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce cursor-pointer hover:scale-110 transition-transform"
          onClick={() => scrollToSection("about")}
        >
          <ChevronDown className="h-8 w-8 text-primary" />
        </div>
      </div>
    </section>
  )
}
