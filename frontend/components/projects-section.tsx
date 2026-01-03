"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ExternalLink, ChevronDown, ChevronUp } from "lucide-react"
import { ITEMS_DISPLAY_LIMIT } from "@/lib/constants"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"

export function ProjectsSection() {
  const { t, resumeData } = useApp()
  const [showAll, setShowAll] = useState(false)

  if (!resumeData?.projects || resumeData.projects.length === 0) {
    return null
  }

  const projects = resumeData.projects
  const displayedProjects = showAll ? projects : projects.slice(0, ITEMS_DISPLAY_LIMIT)
  const hasMore = projects.length > ITEMS_DISPLAY_LIMIT

  return (
    <SectionWrapper id="projects" title={t("projectsTitle")}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
        {displayedProjects.map((project) => {
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
    </SectionWrapper>
  )
}
