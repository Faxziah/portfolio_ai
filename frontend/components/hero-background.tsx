"use client"

import { useEffect, useState } from "react"

export function HeroBackground() {
  const [mounted, setMounted] = useState(false)
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  // First effect: just set mounted after hydration
  useEffect(() => {
    setMounted(true)
  }, [])

  // Second effect: set up mouse tracking only after mounted
  useEffect(() => {
    if (!mounted) return

    let rafId: number | null = null
    const handleMouseMove = (e: MouseEvent) => {
      if (rafId) return // throttle to animation frame
      rafId = requestAnimationFrame(() => {
        setMousePosition({ x: e.clientX, y: e.clientY })
        rafId = null
      })
    }
    window.addEventListener("mousemove", handleMouseMove, { passive: true })
    return () => {
      window.removeEventListener("mousemove", handleMouseMove)
      if (rafId) cancelAnimationFrame(rafId)
    }
  }, [mounted])

  return (
    <div className="absolute inset-0 -z-10 pointer-events-none">
      {/* Mouse-following orb - only render after mount to avoid hydration mismatch */}
      {mounted && (
        <div
          className="absolute h-96 w-96 rounded-full bg-primary/20 blur-3xl will-change-transform transition-transform duration-500 ease-out"
          style={{
            transform: `translate3d(${mousePosition.x - 192}px, ${mousePosition.y - 192}px, 0)`,
          }}
        />
      )}
      {/* Static animated orbs */}
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-float [animation-delay:1s]" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-accent/10 rounded-full blur-3xl animate-float [animation-delay:2s]" />
    </div>
  )
}
