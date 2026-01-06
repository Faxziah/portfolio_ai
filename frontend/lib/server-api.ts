import { type ResumeData, type Settings, type CarouselItem, type DocumentItem } from "./api"

// Server-side API URL - use internal Docker network (backend:8000) for SSR
// NEXT_PUBLIC_API_URL is for client-side, API_URL is for server-side
const API_URL = process.env.API_URL || "http://backend:8000"

export type Translations = Record<string, string>

export async function getSettings(): Promise<Settings> {
  const response = await fetch(`${API_URL}/api/settings/`, {
    next: { revalidate: 60 }, // Cache for 60 seconds
  })
  if (!response.ok) {
    console.error("Failed to fetch settings:", response.statusText)
    return {}
  }
  return response.json()
}

export async function getTranslations(lang: string): Promise<Translations> {
  const response = await fetch(`${API_URL}/api/translations/?lang=${lang}`, {
    next: { revalidate: 60 },
  })
  if (!response.ok) {
    console.error("Failed to fetch translations:", response.statusText)
    return {}
  }
  return response.json()
}

export async function getResumeData(lang: string): Promise<ResumeData | null> {
  const response = await fetch(`${API_URL}/api/resume/?lang=${lang}`, {
    next: { revalidate: 60 },
  })
  if (!response.ok) {
    console.error("Failed to fetch resume:", response.statusText)
    return null
  }
  return response.json()
}

export async function getCarouselData(lang: string): Promise<CarouselItem[]> {
  const response = await fetch(`${API_URL}/api/resume/carousel/?lang=${lang}`, {
    next: { revalidate: 300 }, // Cache for 5 minutes (media changes rarely)
  })
  if (!response.ok) {
    console.error("Failed to fetch carousel:", response.statusText)
    return []
  }
  return response.json()
}

export async function getDocumentsData(lang: string): Promise<DocumentItem[]> {
  const response = await fetch(`${API_URL}/api/resume/documents/?lang=${lang}`, {
    next: { revalidate: 300 },
  })
  if (!response.ok) {
    console.error("Failed to fetch documents:", response.statusText)
    return []
  }
  return response.json()
}

// Helper to get language from cookies
export function getLanguageFromCookies(cookieHeader: string | null, defaultLang: string): string {
  if (!cookieHeader) return defaultLang
  const match = cookieHeader.match(/language=([^;]+)/)
  return match ? match[1] : defaultLang
}
