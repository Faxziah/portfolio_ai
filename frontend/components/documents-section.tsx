"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useApp } from "@/context/app-context"
import { SectionWrapper } from "@/components/section-wrapper"
import { ChevronDown, ChevronUp, X, ZoomIn } from "lucide-react"

export function DocumentsSection() {
  const { t, resumeData, settings } = useApp()
  const [showAll, setShowAll] = useState(false)
  const [lightboxImage, setLightboxImage] = useState<{ src: string; description: string } | null>(null)

  // Check if documents should be shown
  if (settings.show_documents === "0") {
    return null
  }

  if (!resumeData?.documents || resumeData.documents.length === 0) {
    return null
  }

  const documents = resumeData.documents
  const displayedDocuments = showAll ? documents : documents.slice(0, 5)
  const hasMore = documents.length > 5

  return (
    <>
      <SectionWrapper id="documents" title={t("documentsTitle")} background="muted">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {displayedDocuments.map((doc) => (
              <Card
                key={doc.id}
                className="overflow-hidden group cursor-pointer hover:shadow-lg transition-shadow"
                onClick={() => {
                  if (doc.photo_base64) {
                    setLightboxImage({
                      src: `data:${doc.photo_mime_type};base64,${doc.photo_base64}`,
                      description: doc.description,
                    })
                  }
                }}
              >
                {doc.photo_base64 ? (
                  <div className="relative aspect-[3/4]">
                    <img
                      src={`data:${doc.photo_mime_type};base64,${doc.photo_base64}`}
                      alt={doc.description}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors flex items-center justify-center">
                      <ZoomIn className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </div>
                ) : (
                  <div className="aspect-[3/4] bg-muted flex items-center justify-center">
                    <span className="text-muted-foreground text-sm">{t("noImage")}</span>
                  </div>
                )}
                {doc.description && (
                  <div className="p-3">
                    <h3 className="text-sm font-medium line-clamp-2">{doc.description}</h3>
                  </div>
                )}
              </Card>
            ))}
          </div>

          {hasMore && (
            <div className="text-center mt-6">
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

      {/* Lightbox */}
      {lightboxImage && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          onClick={() => setLightboxImage(null)}
        >
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-4 right-4 text-white hover:bg-white/20"
            onClick={() => setLightboxImage(null)}
          >
            <X className="w-6 h-6" />
          </Button>
          <div className="max-w-4xl max-h-[90vh] overflow-auto" onClick={(e) => e.stopPropagation()}>
            <img
              src={lightboxImage.src}
              alt={lightboxImage.description}
              className="max-w-full h-auto"
            />
            {lightboxImage.description && (
              <p className="text-white text-center mt-4 text-lg">{lightboxImage.description}</p>
            )}
          </div>
        </div>
      )}
    </>
  )
}
