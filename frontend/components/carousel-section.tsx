"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { SectionWrapper } from "@/components/section-wrapper"
import { ChevronLeft, ChevronRight, Play } from "lucide-react"
import { useClient } from "@/components/client-providers"
import { LazyYouTube } from "@/components/lazy-youtube"

function getYouTubeVideoId(url: string): string | null {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/
  const match = url.match(regExp)
  if (match && match[2].length === 11) {
    return match[2]
  }
  return null
}

function getYouTubeEmbedUrl(url: string): string | null {
  const videoId = getYouTubeVideoId(url)
  if (videoId) {
    return `https://www.youtube.com/embed/${videoId}`
  }
  return null
}

function getYouTubeThumbnail(url: string): string | null {
  const videoId = getYouTubeVideoId(url)
  if (videoId) {
    return `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`
  }
  return null
}

function CarouselSkeleton() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="relative">
        <div className="overflow-hidden rounded-xl">
          <div className="w-full h-[400px] bg-muted animate-pulse flex items-center justify-center">
            <div className="w-16 h-16 border-4 border-muted-foreground/20 border-t-primary rounded-full animate-spin" />
          </div>
        </div>
      </div>
      {/* Skeleton thumbnails */}
      <div className="flex gap-2 mt-4 overflow-x-auto pb-2">
        {[1, 2, 3].map((i) => (
          <div key={i} className="flex-shrink-0 w-16 h-12 bg-muted rounded-lg animate-pulse" />
        ))}
      </div>
    </div>
  )
}

export function CarouselSection() {
  const { carouselData, carouselLoading, settings, t } = useClient()
  const [currentIndex, setCurrentIndex] = useState(0)

  // Check if carousel should be shown
  if (settings.show_carousel === "0") {
    return null
  }

  // Show skeleton while loading
  if (carouselLoading) {
    return (
      <SectionWrapper id="carousel" title={t("carouselTitle")} className="bg-white dark:bg-background">
        <CarouselSkeleton />
      </SectionWrapper>
    )
  }

  if (!carouselData || carouselData.length === 0) {
    return null
  }

  const items = carouselData

  const nextSlide = () => {
    setCurrentIndex((prev) => (prev + 1) % items.length)
  }

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev - 1 + items.length) % items.length)
  }

  const goToSlide = (index: number) => {
    setCurrentIndex(index)
  }

  return (
    <SectionWrapper id="carousel" title={t("carouselTitle")} className="bg-white dark:bg-background">
      <div className="max-w-4xl mx-auto">
        <div className="relative">
          {/* Main carousel */}
          <div className="overflow-hidden rounded-xl">
            <div
              className="flex transition-transform duration-300 ease-in-out"
              style={{ transform: `translateX(-${currentIndex * 100}%)` }}
            >
              {items.map((item, index) => (
                <div key={item.id} className="w-full flex-shrink-0 relative">
                  {item.type === "photo" && item.photo_base64 ? (
                    <img
                      src={`data:${item.photo_mime_type};base64,${item.photo_base64}`}
                      alt={item.description || `Slide ${index + 1}`}
                      className="w-full h-[400px] object-contain"
                    />
                  ) : item.type === "video" && item.video_url ? (
                    <div className="w-full h-[400px] bg-black flex items-center justify-center relative">
                      {getYouTubeVideoId(item.video_url) ? (
                        <LazyYouTube
                          videoId={getYouTubeVideoId(item.video_url)!}
                          title={item.description || `Video ${index + 1}`}
                        />
                      ) : (
                        <iframe
                          src={item.video_url}
                          title={item.description || `Video ${index + 1}`}
                          className="w-full h-full"
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                          allowFullScreen
                        />
                      )}
                    </div>
                  ) : (
                    <div className="w-full h-[400px] bg-muted flex items-center justify-center">
                      <span className="text-muted-foreground">{t("noContent")}</span>
                    </div>
                  )}
                  {item.description && (
                    <div className="absolute top-0 left-0 right-0 bg-gradient-to-b from-black/70 to-transparent p-4 pointer-events-none">
                      <h3 className="text-white text-lg font-semibold">{item.description}</h3>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Navigation arrows */}
          {items.length > 1 && (
            <>
              <Button
                variant="outline"
                size="icon"
                className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full bg-background/80 backdrop-blur-sm cursor-pointer"
                onClick={prevSlide}
              >
                <ChevronLeft className="w-5 h-5" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-background/80 backdrop-blur-sm cursor-pointer"
                onClick={nextSlide}
              >
                <ChevronRight className="w-5 h-5" />
              </Button>
            </>
          )}
        </div>

        {/* Dots navigation */}
        {items.length > 1 && (
          <div className="flex justify-center gap-2 mt-4">
            {items.map((_, index) => (
              <button
                key={index}
                className={`w-2 h-2 rounded-full transition-colors ${
                  index === currentIndex ? "bg-primary" : "bg-muted-foreground/30"
                }`}
                onClick={() => goToSlide(index)}
              />
            ))}
          </div>
        )}

        {/* Thumbnails */}
        {items.length > 1 && (
          <div className="flex gap-2 mt-4 overflow-x-auto pb-2">
            {items.map((item, index) => (
              <button
                key={item.id}
                className={`flex-shrink-0 rounded-lg overflow-hidden border-2 transition-colors cursor-pointer ${
                  index === currentIndex ? "border-primary" : "border-transparent"
                }`}
                onClick={() => goToSlide(index)}
              >
                {item.type === "photo" && item.photo_base64 ? (
                  <img
                    src={`data:${item.photo_mime_type};base64,${item.photo_base64}`}
                    alt={item.description || `Thumbnail ${index + 1}`}
                    className="w-16 h-12 object-cover"
                  />
                ) : item.type === "video" && item.video_url ? (
                  <div className="w-16 h-12 relative">
                    {getYouTubeThumbnail(item.video_url) ? (
                      <img
                        src={getYouTubeThumbnail(item.video_url)!}
                        alt={item.description || `Video ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full bg-black" />
                    )}
                    {/* YouTube-style red play button */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="bg-[#FF0000] rounded-sm px-1 py-0.5 flex items-center justify-center">
                        <Play className="w-3 h-3 text-white fill-white" />
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="w-16 h-12 bg-muted flex items-center justify-center">
                    <Play className="w-4 h-4" />
                  </div>
                )}
              </button>
            ))}
          </div>
        )}
      </div>
    </SectionWrapper>
  )
}
