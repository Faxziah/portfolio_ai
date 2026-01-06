"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { SectionWrapper } from "@/components/section-wrapper"
import { ChevronDown, ChevronUp } from "lucide-react"
import { ITEMS_DISPLAY_LIMIT } from "@/lib/constants"
import { type ResumeData } from "@/lib/api"

interface ExperienceSectionProps {
  resumeData: ResumeData
  translations: Record<string, string>
}

export function ExperienceSection({ resumeData, translations }: ExperienceSectionProps) {
  const t = (key: string) => translations[key] || key
  const [showAll, setShowAll] = useState(false)

  if (!resumeData?.experiences || resumeData.experiences.length === 0) {
    return null
  }

  const experiences = resumeData.experiences
  const displayedExperiences = showAll ? experiences : experiences.slice(0, ITEMS_DISPLAY_LIMIT)
  const hasMore = experiences.length > ITEMS_DISPLAY_LIMIT

  return (
    <SectionWrapper id="experience" title={t("experienceTitle")}>
        <div className="max-w-4xl mx-auto relative">
          <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary via-chart-2 to-chart-3 hidden md:block" />

          <div className="space-y-8">
          {displayedExperiences.map((exp) => (
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

          {hasMore && (
            <div className="text-center mt-8">
              <Button
                variant="outline"
                onClick={() => setShowAll(!showAll)}
                className="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive bg-background dark:bg-input/30 dark:border-input dark:hover:bg-input/50 h-10 rounded-md px-6 has-[>svg]:px-4 border-2 border-primary/50 hover:border-primary hover:bg-primary/10 hover:text-primary hover:scale-105 transition-all duration-300 shadow-sm hover:shadow-md cursor-pointer"
              >
                {showAll ? (
                  <>
                    {t("showLess")}
                    <ChevronUp className="w-4 h-4" />
                  </>
                ) : (
                  <>
                    {t("showMore")}
                    <ChevronDown className="w-4 h-4" />
                  </>
                )}
              </Button>
            </div>
          )}
        </div>
    </SectionWrapper>
  )
}
