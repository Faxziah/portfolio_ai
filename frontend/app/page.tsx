"use client"

import { useState } from "react"
import { HeroSection } from "@/components/hero-section"
import { AboutSection } from "@/components/about-section"
import { ExperienceSection } from "@/components/experience-section"
import { SkillsSection } from "@/components/skills-section"
import { ProjectsSection } from "@/components/projects-section"
import { EducationSection } from "@/components/education-section"
import { LanguagesSection } from "@/components/languages-section"
import { ContactSection } from "@/components/contact-section"
import { Header } from "@/components/header"
import { AIChatButton } from "@/components/ai-chat-button"
import { ScrollToTop } from "@/components/scroll-to-top"
import { Footer } from "@/components/footer"

export default function Home() {
  const [aiChatOpen, setAiChatOpen] = useState(false)

  return (
    <div className="min-h-screen">
      <Header />
      <AIChatButton onOpenChange={setAiChatOpen} />
      <main>
        <HeroSection />
        <AboutSection />
        <ExperienceSection />
        <SkillsSection />
        <ProjectsSection />
        <EducationSection />
        <LanguagesSection />
        <ContactSection />
      </main>
      <Footer />
      <ScrollToTop aiChatOpen={aiChatOpen} />
    </div>
  )
}
