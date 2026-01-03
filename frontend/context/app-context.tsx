"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { type Language, type Translations } from "@/lib/types"
import { fetchResume, fetchCsrfToken, type ResumeData, type SiteLanguage, type Settings } from "@/lib/api"
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
  settings: Settings
}

const AppContext = createContext<AppContextType | undefined>(undefined)

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

    // Use hex color directly for CSS variables
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
  const [settings, setSettings] = useState<Settings>({})

  useEffect(() => {
    setMounted(true)
    const savedLanguage = localStorage.getItem("language")
    const savedTheme = localStorage.getItem("theme") as "light" | "dark"

    const initialTheme = savedTheme || "light"
    setTheme(initialTheme)
    document.documentElement.classList.toggle("dark", initialTheme === "dark")
    document.documentElement.setAttribute("data-color-scheme", "blue")

    // Fetch CSRF token for POST requests
    fetchCsrfToken()

    // Load settings first to get default language and site languages
    fetch(`${API_BASE_URL}/api/settings/`, { credentials: "include" })
      .then((res) => res.json())
      .then((data: Settings) => {
        setSettings(data)

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
        fetch(`${API_BASE_URL}/api/translations/?lang=${initialLang}`, { credentials: "include" })
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
    <AppContext.Provider value={{ language, setLanguage: handleSetLanguage, t, theme, toggleTheme, colorScheme, resumeData, resumeError, siteLanguages, settings }}>
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
