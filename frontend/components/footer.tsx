import { Mail } from "lucide-react"
import { Button } from "@/components/ui/button"
import { iconMap } from "@/lib/constants"
import { type ResumeData } from "@/lib/api"

interface FooterProps {
  translations: Record<string, string>
  resumeData?: ResumeData
  language?: string
}

export function Footer({ translations, resumeData, language = "en" }: FooterProps) {
  const currentYear = new Date().getFullYear()
  const t = (key: string) => translations[key] || key
  const name = resumeData?.name?.[language] || ""
  const contactInfo = resumeData?.contact_info || []

  return (
    <footer className="bg-muted/30 border-t border-border py-12">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center justify-center gap-6">
          <div className="flex items-center gap-4">
            {contactInfo.map((contact, index) => {
              const Icon = iconMap[contact.type] || Mail
              return (
                <Button key={index} variant="ghost" size="icon" asChild>
                  <a href={contact.href} target={contact.type === "phone" || contact.type === "email" ? undefined : "_blank"} rel={contact.type === "phone" || contact.type === "email" ? undefined : "noopener noreferrer"} aria-label={contact.label}>
                    <Icon className="h-5 w-5" />
                  </a>
                </Button>
              )
            })}
          </div>

          <div className="text-center text-sm text-muted-foreground">
            <p>© {currentYear} {name}. {t("allRightsReserved")}</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
