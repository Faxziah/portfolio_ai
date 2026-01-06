"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { useRouter } from "next/navigation"
import { type Settings, type ResumeData } from "@/lib/api"
import { AIChatButton } from "@/components/ai-chat-button"
import { ScrollToTop } from "@/components/scroll-to-top"

interface ClientContextType {
  theme: "light" | "dark"
  toggleTheme: () => void
  language: string
  setLanguage: (lang: string) => void
  settings: Settings
  translations: Record<string, string>
  t: (key: string) => string
  resumeData: ResumeData | null
}

const ClientContext = createContext<ClientContextType | undefined>(undefined)

// Adjust color brightness
function adjustBrightness(hex: string, percent: number): string {
  hex = hex.replace(/^#/, '')
  const r = Math.min(255, Math.max(0, parseInt(hex.slice(0, 2), 16) + percent))
  const g = Math.min(255, Math.max(0, parseInt(hex.slice(2, 4), 16) + percent))
  const b = Math.min(255, Math.max(0, parseInt(hex.slice(4, 6), 16) + percent))
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`
}

// Apply theme colors to CSS variables
function applyTheme(themeValue: string) {
  const root = document.documentElement

  if (themeValue.startsWith('#')) {
    root.setAttribute("data-color-scheme", "custom")
    const primaryColor = themeValue
    const secondaryColor = adjustBrightness(themeValue, -20)
    const accentColor = adjustBrightness(themeValue, -40)

    root.style.setProperty('--primary', primaryColor)
    root.style.setProperty('--secondary', secondaryColor)
    root.style.setProperty('--accent', accentColor)
    root.style.setProperty('--ring', primaryColor)
    root.style.setProperty('--sidebar-primary', primaryColor)
    root.style.setProperty('--sidebar-ring', primaryColor)
  } else {
    root.setAttribute("data-color-scheme", themeValue)
    root.style.removeProperty('--primary')
    root.style.removeProperty('--secondary')
    root.style.removeProperty('--accent')
    root.style.removeProperty('--ring')
    root.style.removeProperty('--sidebar-primary')
    root.style.removeProperty('--sidebar-ring')
  }
}

interface ClientProvidersProps {
  children: ReactNode
  settings: Settings
  language: string
  translations: Record<string, string>
  resumeData: ResumeData | null
}

export function ClientProviders({ children, settings, language: initialLanguage, translations, resumeData }: ClientProvidersProps) {
  const router = useRouter()
  const [theme, setTheme] = useState<"light" | "dark">("light")
  const [language, setLanguageState] = useState(initialLanguage)
  const [mounted, setMounted] = useState(false)
  const [aiChatOpen, setAiChatOpen] = useState(false)

  useEffect(() => {
    setMounted(true)

    // Initialize theme
    const savedTheme = localStorage.getItem("theme") as "light" | "dark"
    const initialTheme = savedTheme || "light"
    setTheme(initialTheme)
    document.documentElement.classList.toggle("dark", initialTheme === "dark")

    // Apply color scheme from settings
    if (settings.theme) {
      applyTheme(settings.theme)
    } else {
      document.documentElement.setAttribute("data-color-scheme", "blue")
    }
  }, [settings.theme])

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light"
    setTheme(newTheme)
    localStorage.setItem("theme", newTheme)
    document.documentElement.classList.toggle("dark", newTheme === "dark")
  }

  const setLanguage = (lang: string) => {
    setLanguageState(lang)
    // Set cookie and refresh to get new server-rendered content
    document.cookie = `language=${lang};path=/;max-age=31536000`
    router.refresh()
  }

  const t = (key: string): string => translations[key] || key

  return (
    <ClientContext.Provider value={{ theme, toggleTheme, language, setLanguage, settings, translations, t, resumeData }}>
      {children}
      {mounted && (
        <>
          <AIChatButton onOpenChange={setAiChatOpen} />
          <ScrollToTop aiChatOpen={aiChatOpen} />
        </>
      )}
    </ClientContext.Provider>
  )
}

export function useClient() {
  const context = useContext(ClientContext)
  if (!context) {
    throw new Error("useClient must be used within ClientProviders")
  }
  return context
}
