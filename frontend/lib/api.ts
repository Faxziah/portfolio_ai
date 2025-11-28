import { API_BASE_URL, API_ENDPOINTS } from "./constants"

// Get CSRF token from cookie
function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null
  return null
}

// Fetch CSRF token from server
export async function fetchCsrfToken(): Promise<void> {
  try {
    await fetch(`${API_BASE_URL}${API_ENDPOINTS.CSRF}`, {
      method: "GET",
      credentials: "include",
    })
  } catch (error) {
    console.error("Failed to fetch CSRF token:", error)
  }
}

export interface Language {
  id: number
  name: string
  level: string
  proficiency: number
  order: number
}

export interface Skill {
  id: number
  name: string
  order: number
}

export interface SkillCategory {
  id: number
  name: string
  name_key: string
  color: string
  order: number
  skills: Skill[]
}

export interface Experience {
  id: number
  company: string
  position: string
  start_date: string
  end_date: string
  description: string
  order: number
}

export interface Education {
  id: number
  institution: string
  degree: string
  faculty: string
  year: string
  order: number
}

export interface Certificate {
  id: number
  name: string
  year: string
  order: number
}

export interface Project {
  id: number
  code: string
  title: string
  description: string
  technologies: string[]
  link: string
  order: number
}

export interface ContactInfo {
  type: string
  label: string
  value: string
  href: string
  icon?: string
}

export interface ResumeData {
  name: Record<string, string>
  firstname: Record<string, string>
  lastname: Record<string, string>
  languages: Language[]
  skills: Record<string, string[]>
  skill_categories: SkillCategory[]
  experiences: Experience[]
  education: Education[]
  certificates: Certificate[]
  projects: Project[]
  about_me: Record<string, string>
  resume_description: Record<string, string>
  resume_title: Record<string, string>
  stats: {
    years_experience: string
    projects_completed: string
    languages_count: string
  }
  contact_info: ContactInfo[]
  meta: {
    title: Record<string, string>
    description: Record<string, string>
  }
}

export interface SiteLanguage {
  code: string
  name: string
  flag: string
}

export interface Settings {
  theme?: string
  site_languages?: SiteLanguage[]
  default_language?: string
  [key: string]: unknown
}

export async function fetchResume(lang: string = "en"): Promise<ResumeData> {
  const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.RESUME}?lang=${lang}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch resume data: ${response.statusText}`)
  }

  return response.json()
}

export async function sendChatMessage(
  message: string,
  chatHistory: Array<{ role: string; parts: string[] }> = [],
  sessionId?: string,
  language: string = "en"
): Promise<{ response: string; session_id: string }> {
  const csrftoken = getCookie('csrftoken')
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  }
  if (csrftoken) {
    headers["X-CSRFToken"] = csrftoken
  }

  const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.AI_CHAT}`, {
    method: "POST",
    headers,
    credentials: "include",
    body: JSON.stringify({
      message,
      chat_history: chatHistory,
      session_id: sessionId,
      language,
    }),
  })

  if (!response.ok) {
    let errorData: { error?: string } = {};
    try {
      errorData = await response.json()
    } catch {
      errorData = { error: `Failed to send chat message: ${response.statusText}` }
    }
    const error = new Error(errorData.error || `Failed to send chat message: ${response.statusText}`)
    ;(error as any).errorType = errorData.error === 'No API key' ? 'NO_API_KEY' : 'GENERAL'
    throw error
  }

  return response.json()
}

