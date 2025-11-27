"use client"

import { Card } from "@/components/ui/card"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"

export function LanguagesSection() {
  const { t, resumeData } = useApp()

  if (!resumeData?.languages || resumeData.languages.length === 0) {
    return null
  }

  return (
    <SectionWrapper id="languages" title={t("languagesTitle")}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        {resumeData.languages.map((lang) => (
            <Card key={lang.id} className="p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-xl font-bold text-foreground">{lang.name}</h3>
                <span className="text-sm text-muted-foreground">{lang.level}</span>
              </div>
              <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary to-chart-2 transition-all duration-1000"
                  style={{ width: `${lang.proficiency}%` }}
                />
              </div>
            </Card>
          ))}
        </div>
    </SectionWrapper>
  )
}
