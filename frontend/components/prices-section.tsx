"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { SectionWrapper } from "@/components/section-wrapper"
import { ChevronDown, ChevronUp } from "lucide-react"
import { ITEMS_DISPLAY_LIMIT } from "@/lib/constants"
import { type ResumeData, type Settings } from "@/lib/api"

function formatPrice(price: string, currency: string): string {
  const num = parseFloat(price)
  const currencySymbols: Record<string, string> = {
    RUB: '\u20BD',
    USD: '$',
    EUR: '\u20AC',
    GBP: '\u00A3',
  }
  const symbol = currencySymbols[currency] || currency
  return `${num.toLocaleString()} ${symbol}`
}

interface PricesSectionProps {
  resumeData: ResumeData
  settings: Settings
  translations: Record<string, string>
}

export function PricesSection({ resumeData, settings, translations }: PricesSectionProps) {
  const t = (key: string) => translations[key] || key
  const [showAll, setShowAll] = useState(false)

  // Check if prices should be shown
  if (settings.show_prices === "0") {
    return null
  }

  if (!resumeData?.prices || resumeData.prices.length === 0) {
    return null
  }

  const prices = resumeData.prices
  const displayedPrices = showAll ? prices : prices.slice(0, ITEMS_DISPLAY_LIMIT)
  const hasMore = prices.length > ITEMS_DISPLAY_LIMIT

  return (
    <SectionWrapper id="prices" title={t("pricesTitle")}>
      <div className="max-w-4xl mx-auto">
        <div className="grid gap-3">
          {displayedPrices.map((item) => (
            <Card key={item.id} className="p-4 flex justify-between items-center hover:shadow-md transition-shadow">
              <span className="font-medium">{item.name}</span>
              <span className="text-lg font-bold text-primary">
                {formatPrice(item.price, item.currency)}
              </span>
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
  )
}
