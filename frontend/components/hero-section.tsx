import { type ResumeData } from "@/lib/api"
import { HeroButtons } from "./hero-buttons"

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
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-float [animation-delay:1s]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-accent/10 rounded-full blur-3xl animate-float [animation-delay:2s]" />
      </div>

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
