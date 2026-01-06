"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { SectionWrapper } from "@/components/section-wrapper"
import { Star, ChevronDown, ChevronUp } from "lucide-react"
import { ITEMS_DISPLAY_LIMIT } from "@/lib/constants"
import { type ResumeData, type Settings } from "@/lib/api"

const MAX_TEXT_LENGTH = 400

interface ReviewCardProps {
  review: { id: number; stars: number; text: string; author?: string; created_at: string }
  language: string
  translations: Record<string, string>
}

function ReviewCard({ review, language, translations }: ReviewCardProps) {
  const t = (key: string) => translations[key] || key
  const [expanded, setExpanded] = useState(false)

  const isLongText = review.text.length > MAX_TEXT_LENGTH

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    // Use UTC to avoid hydration mismatch between server and client
    const locale = language === 'ru' ? 'ru-RU' : language === 'zh' ? 'zh-CN' : 'en-US'
    return date.toLocaleDateString(locale, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      timeZone: 'UTC'
    })
  }

  return (
    <Card className="p-6 flex flex-col">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-1">
          {[...Array(5)].map((_, i) => (
            <Star
              key={i}
              className={`w-5 h-5 ${
                i < review.stars
                  ? "fill-yellow-400 text-yellow-400"
                  : "text-muted-foreground"
              }`}
            />
          ))}
        </div>
        <span className="text-xs text-muted-foreground">
          {formatDate(review.created_at)}
        </span>
      </div>

      <div className="relative">
        <p className={`text-foreground whitespace-pre-line ${!expanded && isLongText ? "line-clamp-[12]" : ""}`}>
          {review.text}
        </p>
        {!expanded && isLongText && (
          <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-card to-transparent pointer-events-none" />
        )}
      </div>

      <div className="pt-4">
        {isLongText && (
          <Button
            variant="outline"
            onClick={() => setExpanded(!expanded)}
            className="self-start py-2 inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive bg-background dark:bg-input/30 dark:border-input dark:hover:bg-input/50 h-10 rounded-md px-6 has-[>svg]:px-4 border-2 border-primary/50 hover:border-primary hover:bg-primary/10 hover:text-primary hover:scale-105 transition-all duration-300 shadow-sm hover:shadow-md cursor-pointer"
          >
            {expanded ? t("showLess") : t("showFull")}
          </Button>
        )}

        {review.author && (
          <p className="text-sm text-muted-foreground mt-2">— {review.author}</p>
        )}
      </div>
    </Card>
  )
}

interface ReviewsSectionProps {
  resumeData: ResumeData
  settings: Settings
  translations: Record<string, string>
  language?: string
}

export function ReviewsSection({ resumeData, settings, translations, language = "en" }: ReviewsSectionProps) {
  const t = (key: string) => translations[key] || key
  const [showAll, setShowAll] = useState(false)

  // Check if reviews should be shown
  if (settings.show_reviews === "0") {
    return null
  }

  if (!resumeData?.reviews || resumeData.reviews.length === 0) {
    return null
  }

  const reviews = resumeData.reviews
  const displayedReviews = showAll ? reviews : reviews.slice(0, ITEMS_DISPLAY_LIMIT)
  const hasMore = reviews.length > ITEMS_DISPLAY_LIMIT

  return (
    <SectionWrapper id="reviews" title={t("reviewsTitle")} background="muted">
      <div className="max-w-4xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {displayedReviews.map((review) => (
            <ReviewCard key={review.id} review={review} language={language} translations={translations} />
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
  )
}
