"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { GraduationCap, Award, ChevronDown, ChevronUp } from "lucide-react"
import { ITEMS_DISPLAY_LIMIT } from "@/lib/constants"
import { SectionWrapper } from "@/components/section-wrapper"
import { type ResumeData } from "@/lib/api"

interface EducationSectionProps {
  resumeData: ResumeData
  translations: Record<string, string>
}

export function EducationSection({ resumeData, translations }: EducationSectionProps) {
  const t = (key: string) => translations[key] || key
  const [showAllEducation, setShowAllEducation] = useState(false)
  const [showAllCertificates, setShowAllCertificates] = useState(false)

  const hasEducation = resumeData?.education && resumeData.education.length > 0
  const hasCertificates = resumeData?.certificates && resumeData.certificates.length > 0

  if (!hasEducation && !hasCertificates) {
    return null
  }

  const education = resumeData?.education || []
  const certificates = resumeData?.certificates || []

  const displayedEducation = showAllEducation ? education : education.slice(0, ITEMS_DISPLAY_LIMIT)
  const displayedCertificates = showAllCertificates ? certificates : certificates.slice(0, ITEMS_DISPLAY_LIMIT)

  const hasMoreEducation = education.length > ITEMS_DISPLAY_LIMIT
  const hasMoreCertificates = certificates.length > ITEMS_DISPLAY_LIMIT

  const title = `${t("educationTitle")} ${t("and")} ${t("certificationsTitle")}`

  return (
    <SectionWrapper id="education" title={title} background="muted">
      <div className="max-w-4xl mx-auto space-y-8">
        {hasEducation && (
          <div>
            <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <GraduationCap className="h-6 w-6 text-primary" />
              {t("educationTitle")}
            </h3>
            <div className="grid gap-4">
              {displayedEducation.map((edu) => (
                <Card key={edu.id} className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="text-lg font-bold text-foreground">{edu.institution}</h4>
                      {edu.location && (
                        <p className="text-sm text-muted-foreground">{edu.location}</p>
                      )}
                      <p className="text-primary font-semibold mt-1 whitespace-pre-line">
                        {edu.faculty ? `${edu.degree}, ${edu.faculty}` : edu.degree}
                      </p>
                    </div>
                    <span className="text-sm text-muted-foreground">{edu.year}</span>
                  </div>
                </Card>
              ))}
            </div>
            {hasMoreEducation && (
              <div className="text-center mt-4">
                <Button
                  variant="outline"
                  onClick={() => setShowAllEducation(!showAllEducation)}
                  className="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive bg-background dark:bg-input/30 dark:border-input dark:hover:bg-input/50 h-10 rounded-md px-6 has-[>svg]:px-4 border-2 border-primary/50 hover:border-primary hover:bg-primary/10 hover:text-primary hover:scale-105 transition-all duration-300 shadow-sm hover:shadow-md cursor-pointer"
                >
                  {showAllEducation ? (
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
        )}

        {hasCertificates && (
          <div>
            <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Award className="h-6 w-6 text-primary" />
              {t("certificationsTitle")}
            </h3>
            <div className="grid gap-4">
              {displayedCertificates.map((cert) => (
                <Card key={cert.id} className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between">
                    <p className="text-lg font-semibold text-foreground">{cert.name}</p>
                    {cert.year && (
                      <span className="text-sm text-muted-foreground font-medium ml-4 whitespace-nowrap">{cert.year}</span>
                    )}
                  </div>
                </Card>
              ))}
            </div>
            {hasMoreCertificates && (
              <div className="text-center mt-4">
                <Button
                  variant="outline"
                  onClick={() => setShowAllCertificates(!showAllCertificates)}
                  className="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive bg-background dark:bg-input/30 dark:border-input dark:hover:bg-input/50 h-10 rounded-md px-6 has-[>svg]:px-4 border-2 border-primary/50 hover:border-primary hover:bg-primary/10 hover:text-primary hover:scale-105 transition-all duration-300 shadow-sm hover:shadow-md cursor-pointer"
                >
                  {showAllCertificates ? (
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
        )}
      </div>
    </SectionWrapper>
  )
}
