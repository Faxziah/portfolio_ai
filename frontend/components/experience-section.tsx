"use client"

import { Card } from "@/components/ui/card"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"

export function ExperienceSection() {
  const { t, resumeData } = useApp()

  if (!resumeData?.experiences || resumeData.experiences.length === 0) {
    return null
  }

  return (
    <SectionWrapper id="experience" title={t("experienceTitle")}>
        <div className="max-w-4xl mx-auto relative">
          <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary via-chart-2 to-chart-3 hidden md:block" />

          <div className="space-y-8">
          {resumeData.experiences.map((exp) => (
              <div key={exp.id} className="relative pl-0 md:pl-20">
                <div className="absolute left-6 top-6 w-4 h-4 rounded-full bg-primary ring-4 ring-background hidden md:block" />

                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-3">
                    <h3 className="text-xl font-bold text-foreground">{exp.position}</h3>
                    <span className="text-sm text-muted-foreground">
                      {exp.start_date} - {exp.end_date === "Present" ? t("present") : exp.end_date}
                    </span>
                  </div>
                  <div className="text-primary font-semibold mb-2">{t("company")}: {exp.company}</div>
                  <p className="text-muted-foreground leading-relaxed whitespace-pre-line">{exp.description}</p>
                </Card>
              </div>
            ))}
          </div>
        </div>
    </SectionWrapper>
  )
}
