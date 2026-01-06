import type React from "react"
import type { Metadata } from "next"

import "@/app/globals.css"

// Don't prerender - layout fetches from backend
export const dynamic = 'force-dynamic'

import { Geist, Geist_Mono, Geist as V0_Font_Geist, Geist_Mono as V0_Font_Geist_Mono, Source_Serif_4 as V0_Font_Source_Serif_4 } from 'next/font/google'
import { getSettings } from "@/lib/server-api"

// Initialize fonts
const _geist = V0_Font_Geist({ subsets: ['latin'], weight: ["100","200","300","400","500","600","700","800","900"] })
const _geistMono = V0_Font_Geist_Mono({ subsets: ['latin'], weight: ["100","200","300","400","500","600","700","800","900"] })
const _sourceSerif_4 = V0_Font_Source_Serif_4({ subsets: ['latin'], weight: ["200","300","400","500","600","700","800","900"] })

const geistSans = Geist({
  subsets: ["latin"],
  variable: "--font-geist-sans",
})

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
})

export const metadata: Metadata = {
  // Default metadata, overridden by generateMetadata in page.tsx
}

// Helper to generate CSS variables for custom hex colors
function getThemeStyles(theme: string | undefined): string {
  if (!theme) return ''
  if (!theme.startsWith('#')) return ''

  const hex = theme.replace(/^#/, '')
  const r = parseInt(hex.slice(0, 2), 16)
  const g = parseInt(hex.slice(2, 4), 16)
  const b = parseInt(hex.slice(4, 6), 16)

  const adjustBrightness = (r: number, g: number, b: number, percent: number) => {
    const nr = Math.min(255, Math.max(0, r + percent))
    const ng = Math.min(255, Math.max(0, g + percent))
    const nb = Math.min(255, Math.max(0, b + percent))
    return `#${nr.toString(16).padStart(2, '0')}${ng.toString(16).padStart(2, '0')}${nb.toString(16).padStart(2, '0')}`
  }

  const primary = theme
  const secondary = adjustBrightness(r, g, b, -20)
  const accent = adjustBrightness(r, g, b, -40)

  return `--primary: ${primary}; --secondary: ${secondary}; --accent: ${accent}; --ring: ${primary}; --sidebar-primary: ${primary}; --sidebar-ring: ${primary};`
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const settings = await getSettings()
  const theme = settings.theme || 'blue'
  const isCustomColor = theme.startsWith('#')
  const colorScheme = isCustomColor ? 'custom' : theme
  const inlineStyles = isCustomColor ? getThemeStyles(theme) : undefined

  return (
    <html lang="en" suppressHydrationWarning data-color-scheme={colorScheme}>
      <head>
        {inlineStyles && (
          <style dangerouslySetInnerHTML={{ __html: `:root[data-color-scheme="custom"] { ${inlineStyles} }` }} />
        )}
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  )
}
