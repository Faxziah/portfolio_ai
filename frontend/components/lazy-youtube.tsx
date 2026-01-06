"use client"

import { useState } from "react"
import { Play } from "lucide-react"

interface LazyYouTubeProps {
  videoId: string
  title?: string
  className?: string
}

export function LazyYouTube({ videoId, title = "YouTube video", className = "" }: LazyYouTubeProps) {
  const [isLoaded, setIsLoaded] = useState(false)

  // Use higher quality thumbnail
  const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`

  if (isLoaded) {
    return (
      <iframe
        src={`https://www.youtube.com/embed/${videoId}?autoplay=1`}
        title={title}
        className={`w-full h-full ${className}`}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerPolicy="strict-origin-when-cross-origin"
        allowFullScreen
      />
    )
  }

  return (
    <button
      onClick={() => setIsLoaded(true)}
      className={`relative w-full h-full bg-black cursor-pointer group ${className}`}
      aria-label={`Play ${title}`}
    >
      {/* Thumbnail */}
      <img
        src={thumbnailUrl}
        alt={title}
        className="w-full h-full object-cover"
        loading="lazy"
      />

      {/* Dark overlay on hover */}
      <div className="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-colors" />

      {/* YouTube-style play button */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="bg-[#FF0000] group-hover:bg-[#FF0000]/90 rounded-xl px-4 py-3 flex items-center justify-center transition-transform group-hover:scale-110">
          <Play className="w-8 h-8 text-white fill-white ml-1" />
        </div>
      </div>
    </button>
  )
}
