export type Language = string

export interface Translations {
  [key: string]: string
}

export interface TranslationsData {
  [language: string]: Translations
}

