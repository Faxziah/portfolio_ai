"use client"

import { useState, useEffect } from "react"
import { MessageCircle, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { AIChatPanel } from "@/components/ai-chat-panel"

interface AIChatButtonProps {
  onOpenChange?: (isOpen: boolean) => void
}

export function AIChatButton({ onOpenChange }: AIChatButtonProps) {
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    onOpenChange?.(isOpen)
  }, [isOpen, onOpenChange])

  return (
    <>
      <Button
        size="icon"
        className="fixed bottom-6 right-6 z-50 h-16 w-16 rounded-full shadow-2xl bg-gradient-to-r from-primary via-secondary to-accent hover:scale-110 transition-transform animate-glow cursor-pointer"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle AI Chat"
      >
        {isOpen ? <X className="h-7 w-7" /> : <MessageCircle className="h-7 w-7" />}
      </Button>

      <AIChatPanel isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  )
}
