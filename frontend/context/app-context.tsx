"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { type Language, type Translations } from "@/lib/types"
import { fetchResume, type ResumeData, type SiteLanguage, type Settings } from "@/lib/api"
import { API_BASE_URL } from "@/lib/constants"

interface AppContextType {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: string) => string
  theme: "light" | "dark"
  toggleTheme: () => void
  colorScheme: string
  resumeData: ResumeData
  resumeError: Error | null
  siteLanguages: SiteLanguage[]
}

const AppContext = createContext<AppContextType | undefined>(undefined)

// Convert hex color to oklch for CSS variables
function hexToOklch(hex: string): { l: number; c: number; h: number } {
  // Remove # if present
  hex = hex.replace(/^#/, '')

  // Parse hex to RGB
  const r = parseInt(hex.slice(0, 2), 16) / 255
  const g = parseInt(hex.slice(2, 4), 16) / 255
  const b = parseInt(hex.slice(4, 6), 16) / 255

  // Convert RGB to linear RGB
  const toLinear = (c: number) => c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
  const lr = toLinear(r)
  const lg = toLinear(g)
  const lb = toLinear(b)

  // Convert linear RGB to XYZ (D65)
  const x = 0.4124564 * lr + 0.3575761 * lg + 0.1804375 * lb
  const y = 0.2126729 * lr + 0.7151522 * lg + 0.0721750 * lb
  const z = 0.0193339 * lr + 0.1191920 * lg + 0.9503041 * lb

  // Convert XYZ to Lab
  const xn = 0.95047, yn = 1.0, zn = 1.08883
  const f = (t: number) => t > 0.008856 ? Math.pow(t, 1/3) : (903.3 * t + 16) / 116
  const fx = f(x / xn)
  const fy = f(y / yn)
  const fz = f(z / zn)

  const labL = 116 * fy - 16
  const labA = 500 * (fx - fy)
  const labB = 200 * (fy - fz)

  // Convert Lab to OKLab (approximation)
  const l = labL / 100
  const c = Math.sqrt(labA * labA + labB * labB) / 100
  let h = Math.atan2(labB, labA) * (180 / Math.PI)
  if (h < 0) h += 360

  return { l: Math.max(0, Math.min(1, l * 0.8)), c: Math.max(0, Math.min(0.4, c * 0.3)), h }
}

// Apply theme colors to CSS variables
function applyTheme(themeValue: string) {
  const root = document.documentElement

  if (themeValue.startsWith('#')) {
    // Custom hex color
    root.setAttribute("data-color-scheme", "custom")
    const { l, c, h } = hexToOklch(themeValue)

    // Set primary color with variations for secondary and accent
    const primaryL = Math.max(0.4, Math.min(0.7, l + 0.1))
    const secondaryH = (h + 20) % 360
    const accentH = (h - 10 + 360) % 360

    root.style.setProperty('--primary', `oklch(${primaryL.toFixed(2)} ${(c + 0.1).toFixed(2)} ${h.toFixed(0)})`)
    root.style.setProperty('--secondary', `oklch(${(primaryL - 0.04).toFixed(2)} ${(c + 0.12).toFixed(2)} ${secondaryH.toFixed(0)})`)
    root.style.setProperty('--accent', `oklch(${(primaryL - 0.07).toFixed(2)} ${(c + 0.13).toFixed(2)} ${accentH.toFixed(0)})`)
    root.style.setProperty('--ring', `oklch(${primaryL.toFixed(2)} ${(c + 0.1).toFixed(2)} ${h.toFixed(0)})`)
    root.style.setProperty('--sidebar-primary', `oklch(${primaryL.toFixed(2)} ${(c + 0.1).toFixed(2)} ${h.toFixed(0)})`)
    root.style.setProperty('--sidebar-ring', `oklch(${primaryL.toFixed(2)} ${(c + 0.1).toFixed(2)} ${h.toFixed(0)})`)
  } else {
    // Preset theme - remove custom styles and use CSS classes
    root.setAttribute("data-color-scheme", themeValue)
    root.style.removeProperty('--primary')
    root.style.removeProperty('--secondary')
    root.style.removeProperty('--accent')
    root.style.removeProperty('--ring')
    root.style.removeProperty('--sidebar-primary')
    root.style.removeProperty('--sidebar-ring')
  }
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>("")
  const [theme, setTheme] = useState<"light" | "dark">("light")
  const [colorScheme, setColorScheme] = useState<string>("blue")
  const [mounted, setMounted] = useState(false)
  const [resumeData, setResumeData] = useState<ResumeData | null>(null)
  const [resumeError, setResumeError] = useState<Error | null>(null)
  const [translations, setTranslations] = useState<Translations>({})
  const [siteLanguages, setSiteLanguages] = useState<SiteLanguage[]>([])
  const [defaultLanguage, setDefaultLanguage] = useState<string>("en")

  useEffect(() => {
    setMounted(true)
    const savedLanguage = localStorage.getItem("language")
    const savedTheme = localStorage.getItem("theme") as "light" | "dark"

    const initialTheme = savedTheme || "light"
    setTheme(initialTheme)
    document.documentElement.classList.toggle("dark", initialTheme === "dark")
    document.documentElement.setAttribute("data-color-scheme", "blue")

    // Load settings first to get default language and site languages
    fetch(`${API_BASE_URL}/api/settings/`)
      .then((res) => res.json())
      .then((data: Settings) => {
        if (data.theme) {
          setColorScheme(data.theme)
          applyTheme(data.theme)
        }

        // Set site languages from settings
        if (data.site_languages && data.site_languages.length > 0) {
          setSiteLanguages(data.site_languages)
        }

        // Determine initial language: saved > default from settings > first available > "en"
        const settingsDefaultLang = data.default_language || (data.site_languages?.[0]?.code) || "en"
        setDefaultLanguage(settingsDefaultLang)

        const initialLang = savedLanguage || settingsDefaultLang
        setLanguage(initialLang)

        // Load translations
        fetch(`${API_BASE_URL}/api/translations/?lang=${initialLang}`)
          .then((res) => res.json())
          .then((translationsData) => {
            setTranslations(translationsData)
          })
          .catch((error) => {
            console.error("Failed to fetch translations:", error)
          })

        // Load resume
        fetchResume(initialLang)
          .then((resumeDataResponse) => {
            setResumeData(resumeDataResponse)
            setResumeError(null)
          })
          .catch((error) => {
            console.error("Failed to fetch resume data:", error)
            setResumeError(error instanceof Error ? error : new Error("Failed to load resume"))
          })
      })
      .catch((error) => {
        console.error("Failed to fetch settings:", error)
        // Fallback if settings fail
        const initialLang = savedLanguage || "en"
        setLanguage(initialLang)
        setDefaultLanguage("en")

        fetch(`${API_BASE_URL}/api/translations/?lang=${initialLang}`)
          .then((res) => res.json())
          .then((data) => setTranslations(data))
          .catch((err) => console.error("Failed to fetch translations:", err))

        fetchResume(initialLang)
          .then((data) => {
            setResumeData(data)
            setResumeError(null)
          })
          .catch((err) => {
            console.error("Failed to fetch resume data:", err)
            setResumeError(err instanceof Error ? err : new Error("Failed to load resume"))
          })
      })
  }, [])

  useEffect(() => {
    if (mounted) {
      // Load resume data
      fetchResume(language)
        .then((data) => {
          setResumeData(data)
          setResumeError(null)
        })
        .catch((error) => {
          console.error("Failed to fetch resume data:", error)
        })
      
      // Load translations
      fetch(`${API_BASE_URL}/api/translations/?lang=${language}`)
        .then((res) => res.json())
        .then((data) => {
          setTranslations(data)
        })
        .catch((error) => {
          console.error("Failed to fetch translations:", error)
        })
    }
  }, [language, mounted])

  const handleSetLanguage = (lang: Language) => {
    setLanguage(lang)
    localStorage.setItem("language", lang)
  }

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light"
    setTheme(newTheme)
    localStorage.setItem("theme", newTheme)
    document.documentElement.classList.toggle("dark", newTheme === "dark")
  }

  const t = (key: string): string => {
    // Special keys from resume data
    if (key === "heroTitle" && resumeData) {
      return resumeData.resume_title[language] || resumeData.resume_title[defaultLanguage] || ""
    }
    if (key === "heroDescription" && resumeData) {
      return resumeData.resume_description[language] || resumeData.resume_description[defaultLanguage] || ""
    }
    if (key === "aboutDescription" && resumeData) {
      return resumeData.about_me[language] || resumeData.about_me[defaultLanguage] || ""
    }

    // Get from database translations
    return translations[key] || key
  }

  if (!mounted || !resumeData || !language) {
    return null
  }

  return (
    <AppContext.Provider value={{ language, setLanguage: handleSetLanguage, t, theme, toggleTheme, colorScheme, resumeData, resumeError, siteLanguages }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error("useApp must be used within AppProvider")
  }
  return context
}
