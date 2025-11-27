"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Mail, Phone, Github, Send, Globe, type LucideIcon } from "lucide-react"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"

const iconMap: Record<string, LucideIcon> = {
  phone: Phone,
  email: Mail,
  github: Github,
  telegram: Send,
  hh: Globe,
}

export function ContactSection() {
  const { t, resumeData, language } = useApp()

  const contactInfo = resumeData?.contact_info || []

  if (!contactInfo || contactInfo.length === 0) {
    return null
  }

  return (
    <SectionWrapper id="contact" title={t("contactTitle")} background="muted">
      <div className="max-w-4xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {contactInfo.map((contact, index) => {
            const Icon = iconMap[contact.type] || Mail
            let displayText = contact.value
            if (contact.type === "phone") {
              displayText = t("call")
            } else if (contact.type === "email") {
              displayText = t("write")
            } else {
              displayText = t("goTo")
            }
            return (
              <Card key={index} className="p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-primary/10 rounded-lg">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <div className="flex-grow">
                    <div className="text-sm text-muted-foreground mb-1">{contact.label}</div>
                    <Button
                      variant="link"
                      className="h-auto p-0 text-primary hover:text-primary/80 hover:underline hover:font-semibold cursor-pointer font-medium transition-all"
                      asChild
                    >
                      <a href={contact.href} target={contact.type === "phone" || contact.type === "email" ? undefined : "_blank"} rel={contact.type === "phone" || contact.type === "email" ? undefined : "noopener noreferrer"}>
                        {displayText}
                      </a>
                    </Button>
                  </div>
                </div>
              </Card>
            )
          })}
        </div>
      </div>
    </SectionWrapper>
  )
}
