"use client"

import { useState, useRef, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Send, Bot, User } from "lucide-react"
import { cn } from "@/lib/utils"
import { useApp } from "@/context/app-context"
import { sendChatMessage } from "@/lib/api"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

interface Message {
  role: "user" | "assistant"
  content: string
}

interface AIChatPanelProps {
  isOpen: boolean
  onClose: () => void
}

export function AIChatPanel({ isOpen, onClose }: AIChatPanelProps) {
  const { t, resumeData, language } = useApp()
  
  const getWelcomeMessage = () => {
    const baseMessage = t("aiChatWelcome")
    if (resumeData?.firstname && resumeData?.lastname) {
      const firstName = resumeData.firstname[language] || resumeData.firstname.en || ""
      const lastName = resumeData.lastname[language] || resumeData.lastname.en || ""
      const fullName = `${firstName} ${lastName}`.trim()
      if (fullName) {
        return baseMessage.replace(/\{name\}/g, fullName)
      }
    }
    return baseMessage.replace(/\{name\}/g, "")
  }

  const [messages, setMessages] = useState<Message[]>([])
  const [sessionId, setSessionId] = useState<string>()
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setSessionId(crypto.randomUUID?.() || Math.random().toString(36).substring(2) + Date.now().toString(36))
    setMessages([
      {
        role: "assistant",
        content: getWelcomeMessage(),
      },
    ])
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (sessionId) {
      const welcomeMsg = getWelcomeMessage()
      setMessages([
        {
          role: "assistant",
          content: welcomeMsg,
        },
      ])
    }
  }, [language, resumeData, t, sessionId])

  const handleSend = async () => {
    if (!input.trim() || isLoading || !sessionId) return

    const userMessage = input.trim()
    setInput("")
    setMessages((prev) => [...prev, { role: "user", content: userMessage }])
    setIsLoading(true)

    try {
      const welcomeMsg = getWelcomeMessage()
      const chatHistory = messages
        .filter((msg) => msg.role !== "assistant" || msg.content !== welcomeMsg)
        .map((msg) => ({
          role: msg.role === "user" ? "user" : "model",
          parts: [msg.content],
        }))

      const response = await sendChatMessage(userMessage, chatHistory, sessionId, language)
      
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.response,
        },
      ])
    } catch (error: any) {
      console.error("Error sending message:", error)
      const errorMessage = error?.errorType === 'NO_API_KEY' 
        ? t("aiChatNoApiKey") 
        : t("aiChatError")
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: errorMessage,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div
      className={cn(
        "fixed bottom-24 left-4 right-4 sm:left-auto sm:right-6 z-40 w-auto sm:w-full sm:max-w-md h-[70vh] sm:h-[500px] transition-all duration-300",
        isOpen ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0 pointer-events-none",
      )}
    >
      <Card className="h-full flex flex-col shadow-2xl glass-strong border-2 border-primary/20">
        <div className="p-4 border-b border-border bg-gradient-to-r from-primary/20 via-secondary/20 to-accent/20">
          <h3 className="font-bold text-lg">{t("aiChatTitle")}</h3>
          <p className="text-sm text-muted-foreground">{t("aiChatSubtitle")}</p>
        </div>

        <div className="flex-grow overflow-y-auto p-4 space-y-4 bg-background">
          {messages.map((message, index) => (
            <div key={index} className={cn("flex gap-3", message.role === "user" ? "justify-end" : "justify-start")}>
              {message.role === "assistant" && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center">
                  <Bot className="h-5 w-5 text-white" />
                </div>
              )}

              <div
                className={cn(
                  "rounded-lg px-4 py-2 max-w-[80%]",
                  message.role === "user"
                    ? "bg-gradient-to-r from-primary to-secondary text-white"
                    : "bg-muted text-foreground",
                )}
              >
                {message.role === "assistant" ? (
                  <div className="text-sm leading-relaxed [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                        strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                        em: ({ children }) => <em className="italic">{children}</em>,
                        ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1 ml-2">{children}</ul>,
                        ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1 ml-2">{children}</ol>,
                        li: ({ children }) => <li className="ml-1">{children}</li>,
                        code: ({ children, className }) => {
                          const isInline = !className
                          return isInline ? (
                            <code className="bg-muted-foreground/20 px-1 py-0.5 rounded text-xs font-mono">{children}</code>
                          ) : (
                            <code className="block bg-muted-foreground/20 p-2 rounded text-xs font-mono overflow-x-auto mb-2 whitespace-pre-wrap">{children}</code>
                          )
                        },
                        pre: ({ children }) => <pre className="bg-muted-foreground/20 p-2 rounded text-xs font-mono overflow-x-auto mb-2 whitespace-pre-wrap">{children}</pre>,
                        h1: ({ children }) => <h1 className="text-lg font-bold mb-2 mt-3 first:mt-0">{children}</h1>,
                        h2: ({ children }) => <h2 className="text-base font-bold mb-2 mt-3 first:mt-0">{children}</h2>,
                        h3: ({ children }) => <h3 className="text-sm font-bold mb-1 mt-2 first:mt-0">{children}</h3>,
                        blockquote: ({ children }) => <blockquote className="border-l-4 border-primary/50 pl-3 italic my-2 opacity-80">{children}</blockquote>,
                        a: ({ children, href }) => <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary underline hover:text-primary/80">{children}</a>,
                        hr: () => <hr className="my-3 border-border" />,
                        table: ({ children }) => <div className="overflow-x-auto my-2"><table className="min-w-full border-collapse border border-border">{children}</table></div>,
                        thead: ({ children }) => <thead className="bg-muted">{children}</thead>,
                        tbody: ({ children }) => <tbody>{children}</tbody>,
                        tr: ({ children }) => <tr className="border-b border-border">{children}</tr>,
                        th: ({ children }) => <th className="border border-border px-2 py-1 text-left font-semibold">{children}</th>,
                        td: ({ children }) => <td className="border border-border px-2 py-1">{children}</td>,
                      }}
                    >
                      {message.content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <p className="text-sm leading-relaxed">{message.content}</p>
                )}
              </div>

              {message.role === "user" && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                  <User className="h-5 w-5" />
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center">
                <Bot className="h-5 w-5 text-white" />
              </div>
              <div className="bg-muted rounded-lg px-4 py-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-secondary rounded-full animate-bounce [animation-delay:0.2s]" />
                  <div className="w-2 h-2 bg-accent rounded-full animate-bounce [animation-delay:0.4s]" />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 border-t border-border bg-background">
          <form
            onSubmit={(e) => {
              e.preventDefault()
              handleSend()
            }}
            className="flex gap-2"
          >
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={t("aiChatPlaceholder")}
              disabled={isLoading}
              className="flex-grow"
            />
            <Button
              type="submit"
              size="icon"
              disabled={isLoading || !input.trim()}
              className="bg-gradient-to-r from-primary to-secondary hover:opacity-90 cursor-pointer"
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  )
}
