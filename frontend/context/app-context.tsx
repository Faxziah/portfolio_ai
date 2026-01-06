"use client"

import { createContext, useContext, useState, useEffect, useRef, type ReactNode } from "react"
import { type Language, type Translations } from "@/lib/types"
import { fetchResume, fetchCsrfToken, type ResumeData, type SiteLanguage, type Settings, type CarouselItem, type DocumentItem } from "@/lib/api"
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
  // Separate loading states for media sections
  carouselData: CarouselItem[]
  carouselLoading: boolean
  documentsData: DocumentItem[]
  documentsLoading: boolean
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

  // Separate state for media-heavy sections
  const [carouselData, setCarouselData] = useState<CarouselItem[]>([])
  const [carouselLoading, setCarouselLoading] = useState(true)
  const [documentsData, setDocumentsData] = useState<DocumentItem[]>([])
  const [documentsLoading, setDocumentsLoading] = useState(true)

  // Track if initial load is complete to prevent duplicate requests
  const initialLoadRef = useRef(false)
  const prevLanguageRef = useRef<string>("")

  // Load core resume data (without media) - fast
  const loadCoreData = async (lang: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/resume/?lang=${lang}`, {
        credentials: "include",
      })
      if (!response.ok) throw new Error("Failed to fetch resume")
      const data = await response.json()
      setResumeData(data)
      setResumeError(null)
    } catch (error) {
      console.error("Failed to fetch resume data:", error)
      setResumeError(error instanceof Error ? error : new Error("Failed to load resume"))
    }
  }

  // Load carousel data separately - may be slow/large
  const loadCarouselData = async (lang: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/resume/carousel/?lang=${lang}`, {
        credentials: "include",
      })
      if (!response.ok) throw new Error("Failed to fetch carousel")
      const data = await response.json()
      setCarouselData(data || [])
    } catch (error) {
      console.error("Failed to fetch carousel data:", error)
      setCarouselData([])
    } finally {
      setCarouselLoading(false)
    }
  }

  // Load documents data separately - may be slow/large
  const loadDocumentsData = async (lang: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/resume/documents/?lang=${lang}`, {
        credentials: "include",
      })
      if (!response.ok) throw new Error("Failed to fetch documents")
      const data = await response.json()
      setDocumentsData(data || [])
    } catch (error) {
      console.error("Failed to fetch documents data:", error)
      setDocumentsData([])
    } finally {
      setDocumentsLoading(false)
    }
  }

  // Load all data for a language
  const loadAllData = (lang: string) => {
    loadTranslations(lang)
    loadCoreData(lang)
    // Load media sections in parallel (they show skeletons while loading)
    loadCarouselData(lang)
    loadDocumentsData(lang)
  }

  // Load translations
  const loadTranslations = async (lang: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/translations/?lang=${lang}`, {
        credentials: "include",
      })
      if (!response.ok) throw new Error("Failed to fetch translations")
      const data = await response.json()
      setTranslations(data)
    } catch (error) {
      console.error("Failed to fetch translations:", error)
    }
  }

  // Initial mount effect - loads settings and determines language
  useEffect(() => {
    setMounted(true)
    const savedLanguage = localStorage.getItem("language")
    const savedTheme = localStorage.getItem("theme") as "light" | "dark"

    const initialTheme = savedTheme || "light"
    setTheme(initialTheme)
    document.documentElement.classList.toggle("dark", initialTheme === "dark")

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
        prevLanguageRef.current = initialLang
        setLanguage(initialLang)

        // Load data for initial language
        initialLoadRef.current = true
        loadAllData(initialLang)
      })
      .catch((error) => {
        console.error("Failed to fetch settings:", error)
        // Fallback if settings fail
        const initialLang = savedLanguage || "en"
        prevLanguageRef.current = initialLang
        setLanguage(initialLang)
        setDefaultLanguage("en")

        initialLoadRef.current = true
        loadAllData(initialLang)
      })
  }, [])

  // Effect for language changes (after initial load)
  useEffect(() => {
    // Skip if not mounted, language is empty, or this is the initial load
    if (!mounted || !language || !initialLoadRef.current) {
      return
    }

    // Skip if language hasn't actually changed
    if (prevLanguageRef.current === language) {
      return
    }

    prevLanguageRef.current = language

    // Reset loading states for media sections
    setCarouselLoading(true)
    setDocumentsLoading(true)

    // Load data for new language
    loadAllData(language)
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
    <AppContext.Provider value={{
      language,
      setLanguage: handleSetLanguage,
      t,
      theme,
      toggleTheme,
      colorScheme,
      resumeData,
      resumeError,
      siteLanguages,
      settings,
      carouselData,
      carouselLoading,
      documentsData,
      documentsLoading,
    }}>
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
