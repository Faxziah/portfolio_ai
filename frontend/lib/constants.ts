import { Github, Send, Mail, Phone, Globe, Instagram, Users, type LucideIcon } from "lucide-react"

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export const API_ENDPOINTS = {
  RESUME: "/api/resume/",
  AI_CHAT: "/api/ai/chat/",
  CSRF: "/api/csrf/",
} as const

// Number of items to show before "Show more" button appears
export const ITEMS_DISPLAY_LIMIT = 4

export const iconMap: Record<string, LucideIcon> = {
  phone: Phone,
  email: Mail,
  github: Github,
  telegram: Send,
  hh: Globe,
  web: Globe,
  social: Users,
  instagram: Instagram,
}

