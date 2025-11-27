"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"

export function SkillsSection() {
  const { t, resumeData } = useApp()

  if (!resumeData?.skill_categories || resumeData.skill_categories.length === 0) {
    return null
  }

  const skillCategories = resumeData.skill_categories.map((category) => ({
    category: category.name,
    skills: category.skills.map((s) => s.name),
    color: category.color,
  }))

  return (
    <SectionWrapper id="skills" title={t("skillsTitle")} background="muted">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
        {skillCategories.map((category, index) => (
          <Card key={index} className="p-6 hover:shadow-lg transition-shadow">
            <h3 className={`text-xl font-bold mb-4 bg-gradient-to-r ${category.color} bg-clip-text`}>
              {category.category}
            </h3>
            <div className="flex flex-wrap gap-2">
              {category.skills.map((skill, skillIndex) => (
                <Badge key={skillIndex} variant="secondary" className="text-sm">
                  {skill}
                </Badge>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </SectionWrapper>
  )
}
