"use client"

import { useState } from "react"
import Image from "next/image"
import { Moon, Sun, Globe, Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { useApp } from "@/context/app-context"

const navItems = [
  { key: "navAbout", href: "#about" },
  { key: "navExperience", href: "#experience" },
  { key: "navSkills", href: "#skills" },
  { key: "navProjects", href: "#projects" },
  { key: "navEducation", href: "#education" },
  { key: "navLanguages", href: "#languages" },
  { key: "navContact", href: "#contact" },
]

export function Header() {
  const { language, setLanguage, theme, toggleTheme, resumeData, siteLanguages, t } = useApp()
  const name = resumeData?.name?.[language] || ""
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleNavClick = (href: string) => {
    setMobileMenuOpen(false)
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
    }
  }

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    })
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-[12px] cursor-pointer" onClick={scrollToTop}>
            <Image src="/logo.png" alt={name || "Logo"} width={48} height={48} priority className="object-contain rounded-[12px]" />
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1 mr-2">
            {navItems.map((item) => (
              <button
                key={item.key}
                onClick={() => handleNavClick(item.href)}
                className="px-3 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
              >
                {t(item.key)}
              </button>
            ))}
          </nav>

          {/* Mobile menu button */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
            className="lg:hidden w-10 cursor-pointer"
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
          {siteLanguages.length > 1 && (
            <DropdownMenu modal={false}>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" aria-label="Select language" className="w-10 cursor-pointer">
                  <Globe className="h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="glass-strong min-w-[150px]" sideOffset={5}>
                {siteLanguages.map((lang) => (
                  <DropdownMenuItem
                    key={lang.code}
                    onClick={() => setLanguage(lang.code)}
                    className={`cursor-pointer ${language === lang.code ? "bg-primary/10" : ""}`}
                  >
                    <span className="mr-2">{lang.flag}</span>
                    {lang.name}
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          )}

          <Button variant="ghost" size="icon" onClick={toggleTheme} aria-label="Toggle theme" className="w-10 cursor-pointer">
            {theme === "light" ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
          </Button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <nav className="lg:hidden glass border-t border-border">
          <div className="container mx-auto px-4 py-2">
            {navItems.map((item) => (
              <button
                key={item.key}
                onClick={() => handleNavClick(item.href)}
                className="block w-full text-left px-3 py-3 text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors cursor-pointer rounded-lg"
              >
                {t(item.key)}
              </button>
            ))}
          </div>
        </nav>
      )}
    </header>
  )
}
