import { cookies } from "next/headers"
import { type Metadata } from "next"
import { getSettings, getTranslations, getResumeData } from "@/lib/server-api"

// Don't prerender - requires backend connection
export const dynamic = 'force-dynamic'

export async function generateMetadata(): Promise<Metadata> {
  const cookieStore = await cookies()
  const settings = await getSettings()
  const defaultLang = settings.default_language || settings.site_languages?.[0]?.code || "en"
  const language = cookieStore.get("language")?.value || defaultLang

  const [translations, resumeData] = await Promise.all([
    getTranslations(language),
    getResumeData(language),
  ])

  const name = resumeData?.name?.[language] || "Portfolio"
  const title = resumeData?.resume_title?.[language] || name
  const description = resumeData?.resume_description?.[language] || translations["heroDescription"] || ""

  return {
    title: `${name} - ${title}`,
    description,
    openGraph: {
      title: `${name} - ${title}`,
      description,
      type: "website",
    },
  }
}
import { HeroSection } from "@/components/hero-section"
import { CarouselSection } from "@/components/carousel-section"
import { AboutSection } from "@/components/about-section"
import { ExperienceSection } from "@/components/experience-section"
import { SkillsSection } from "@/components/skills-section"
import { ProjectsSection } from "@/components/projects-section"
import { EducationSection } from "@/components/education-section"
import { LanguagesSection } from "@/components/languages-section"
import { ReviewsSection } from "@/components/reviews-section"
import { PricesSection } from "@/components/prices-section"
import { ContactSection } from "@/components/contact-section"
import { DocumentsSection } from "@/components/documents-section"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { ClientProviders } from "@/components/client-providers"

export default async function Home() {
  // Get language from cookies
  const cookieStore = await cookies()
  const settings = await getSettings()

  const defaultLang = settings.default_language || settings.site_languages?.[0]?.code || "en"
  const language = cookieStore.get("language")?.value || defaultLang

  // Fetch core data on server (media loaded on client to reduce initial page size)
  const [translations, resumeData] = await Promise.all([
    getTranslations(language),
    getResumeData(language),
  ])

  if (!resumeData) {
    return <div>Failed to load data</div>
  }

  // Helper function for translations
  const t = (key: string): string => translations[key] || key

  return (
    <ClientProviders
      settings={settings}
      language={language}
      translations={translations}
      resumeData={resumeData}
    >
      <div className="min-h-screen">
        <Header
          settings={settings}
          language={language}
          translations={translations}
        />
        <main>
          <HeroSection
            resumeData={resumeData}
            language={language}
            translations={translations}
          />
          <CarouselSection />
          <AboutSection
            resumeData={resumeData}
            language={language}
            translations={translations}
          />
          <ExperienceSection
            resumeData={resumeData}
            translations={translations}
          />
          <SkillsSection
            resumeData={resumeData}
            translations={translations}
          />
          <ProjectsSection
            resumeData={resumeData}
            translations={translations}
          />
          <EducationSection
            resumeData={resumeData}
            translations={translations}
          />
          <LanguagesSection
            resumeData={resumeData}
            translations={translations}
          />
          <ReviewsSection
            resumeData={resumeData}
            settings={settings}
            translations={translations}
            language={language}
          />
          <PricesSection
            resumeData={resumeData}
            settings={settings}
            translations={translations}
          />
          <ContactSection
            resumeData={resumeData}
            translations={translations}
          />
          <DocumentsSection />
        </main>
        <Footer translations={translations} resumeData={resumeData} language={language} />
      </div>
    </ClientProviders>
  )
}
