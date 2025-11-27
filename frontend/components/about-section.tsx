"use client"

import { Card } from "@/components/ui/card"
import { Briefcase, Code, Globe } from "lucide-react"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"

export function AboutSection() {
  const { t, resumeData, language } = useApp()

  const stats = [
    { icon: Briefcase, value: resumeData?.stats?.years_experience || "", label: t("yearsExperience") },
    { icon: Code, value: resumeData?.stats?.projects_completed || "", label: t("projectsCompleted") },
    { icon: Globe, value: resumeData?.stats?.languages_count || "", label: t("languages") },
  ]

  const aboutDescription = resumeData?.about_me?.[language] || ""

  return (
    <SectionWrapper id="about" title={t("aboutTitle")} background="muted">
        <div className="max-w-3xl mx-auto mb-12">
        <p className="text-lg text-muted-foreground leading-relaxed text-center">{aboutDescription}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {stats.map((stat, index) => (
            <Card key={index} className="p-6 text-center hover:shadow-lg transition-shadow">
              <stat.icon className="h-12 w-12 mx-auto mb-4 text-primary" />
              <div className="text-4xl font-bold mb-2 bg-gradient-to-r from-primary to-chart-2 bg-clip-text text-transparent">
                {stat.value}
              </div>
              <div className="text-muted-foreground">{stat.label}</div>
            </Card>
          ))}
        </div>
    </SectionWrapper>
  )
}
