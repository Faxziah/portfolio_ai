import { type ResumeData } from "@/lib/api"
import { HeroButtons } from "./hero-buttons"
import { HeroBackground } from "./hero-background"

interface HeroSectionProps {
  resumeData: ResumeData
  language: string
  translations: Record<string, string>
}

export function HeroSection({ resumeData, language, translations }: HeroSectionProps) {
  const t = (key: string) => translations[key] || key

  const name = resumeData?.name?.[language] || ""
  const heroTitle = resumeData?.resume_title?.[language] || ""
  const heroDescription = resumeData?.resume_description?.[language] || ""

  return (
    <section className="min-h-screen flex items-center justify-center relative pt-20 overflow-hidden">
      <HeroBackground />

      <div className="container mx-auto px-4 text-center">
        <div className="animate-fade-in">
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-primary via-secondary to-accent text-gradient">{name}</span>
          </h1>
          <h2 className="text-2xl md:text-4xl font-semibold mb-6 text-foreground whitespace-pre-line">{heroTitle}</h2>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8 leading-relaxed">
            {heroDescription}
          </p>

          <HeroButtons
            viewProjectsText={t("viewProjects")}
            contactMeText={t("contactMe")}
          />
        </div>
      </div>
    </section>
  )
}
