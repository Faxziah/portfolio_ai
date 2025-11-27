"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ExternalLink } from "lucide-react"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"

export function ProjectsSection() {
  const { t, resumeData } = useApp()

  if (!resumeData?.projects || resumeData.projects.length === 0) {
    return null
  }

  return (
    <SectionWrapper id="projects" title={t("projectsTitle")}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
        {resumeData.projects.map((project) => {
          const hasLink = project.link && project.link !== "#"
          
          return (
            <Card key={project.id} className="p-6 hover:shadow-lg transition-shadow flex flex-col">
              <h3 className="text-xl font-bold mb-3 text-foreground">{project.title}</h3>
              <p className="text-muted-foreground mb-4 flex-grow leading-relaxed">{project.description}</p>
              <div className="flex flex-wrap gap-2 mb-4">
                {project.technologies.map((tech, techIndex) => (
                  <Badge key={techIndex} variant="outline">
                    {tech}
                  </Badge>
                ))}
              </div>
              {hasLink ? (
                <Button
                  variant="outline"
                  size="sm"
                  className="w-fit bg-transparent hover:bg-primary/10 cursor-pointer"
                  asChild
                >
                  <a href={project.link} target="_blank" rel="noopener noreferrer">
                    {t("viewProject")} <ExternalLink className="ml-2 h-4 w-4" />
                  </a>
                </Button>
              ) : (
                <div className="h-9"></div>
              )}
            </Card>
          )
        })}
      </div>
    </SectionWrapper>
  )
}
