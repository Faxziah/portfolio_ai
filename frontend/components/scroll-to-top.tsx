"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { ArrowUp } from "lucide-react"
import { cn } from "@/lib/utils"

interface ScrollToTopProps {
  aiChatOpen?: boolean
}

export function ScrollToTop({ aiChatOpen = false }: ScrollToTopProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.scrollY > 500 && !aiChatOpen) {
        setIsVisible(true)
      } else {
        setIsVisible(false)
      }
    }

    toggleVisibility()
    window.addEventListener("scroll", toggleVisibility)
    return () => window.removeEventListener("scroll", toggleVisibility)
  }, [aiChatOpen])

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    })
  }

  return (
    <Button
      size="icon"
      className={cn(
        "fixed bottom-24 right-6 z-40 h-12 w-12 rounded-full shadow-lg bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-300 cursor-pointer",
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-16 pointer-events-none",
      )}
      onClick={scrollToTop}
      aria-label="Scroll to top"
    >
      <ArrowUp className="h-5 w-5" />
    </Button>
  )
}
