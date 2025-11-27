"use client"

import { Card } from "@/components/ui/card"
import { GraduationCap, Award } from "lucide-react"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"

export function EducationSection() {
  const { t, resumeData } = useApp()

  const hasEducation = resumeData?.education && resumeData.education.length > 0
  const hasCertificates = resumeData?.certificates && resumeData.certificates.length > 0

  if (!hasEducation && !hasCertificates) {
    return null
  }

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
              {resumeData.education.map((edu) => (
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
          </div>
        )}

        {hasCertificates && (
          <div>
            <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Award className="h-6 w-6 text-primary" />
              {t("certificationsTitle")}
            </h3>
            <div className="grid gap-4">
              {resumeData.certificates.map((cert) => (
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
          </div>
        )}
      </div>
    </SectionWrapper>
  )
}
