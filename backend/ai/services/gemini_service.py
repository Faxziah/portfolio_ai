"""
Gemini API service for AI chat functionality.
Uses google-genai SDK with gemini-2.5-flash model.
"""
from google import genai
from google.genai import types
from django.conf import settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

MODEL_NAME = 'gemini-2.5-flash'


class GeminiService:
    """Handle Gemini API interactions for resume chatbot."""

    def __init__(self):
        api_key = self._get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")

        self.client = genai.Client(api_key=api_key)

    def _get_api_key(self) -> str:
        try:
            from resume.models import Setting
            setting = Setting.objects.filter(name='gemini_api_key').first()
            if setting and setting.value:
                return setting.value
        except Exception:
            pass
        return settings.GEMINI_API_KEY if hasattr(settings, 'GEMINI_API_KEY') else ''

    def chat(
        self,
        message: str,
        chat_history: Optional[List[Dict]] = None,
        resume_context: Optional[str] = None,
        language: str = 'en'
    ) -> str:
        """
        Send message to Gemini API.

        Args:
            message: User's question
            chat_history: Previous conversation in format:
                [{"role": "user", "parts": ["..."]}, {"role": "model", "parts": ["..."]}]
            resume_context: Resume data from database (include only on first message)
            language: Language code for response

        Returns:
            AI response text
        """
        system_instruction = (
            "You are a helpful assistant for a PUBLIC portfolio website. "
            "Answer questions about the owner's experience, skills, projects, languages, and contact information based on the resume data below. "
            "IMPORTANT: All contact information (email, GitHub, LinkedIn, phone) is PUBLIC and meant to be shared with visitors. "
            "The 'Languages' section refers to SPOKEN/WRITTEN languages (like English, Spanish), NOT programming languages. "
            "IMPORTANT: Always respond in the SAME LANGUAGE as the user's question. If they ask in Russian, answer in Russian. If they ask in Chinese, answer in Chinese. "
            "Be concise, professional, and friendly. "
            "Keep your responses to a maximum of 100 words. Be brief and to the point."
        )

        if resume_context:
            system_instruction += f"\n\nRESUME:\n{resume_context}"

        # Конвертируем историю чата в формат SDK
        history = []
        if chat_history:
            for msg in chat_history:
                role = msg.get('role', 'user')
                parts = msg.get('parts', [])
                text = parts[0] if isinstance(parts, list) and parts else str(parts)
                history.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=text)]
                    )
                )

        try:
            chat = self.client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                ),
                history=history,
            )
            response = chat.send_message(message)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {type(e).__name__}: {e}")
            return self._get_fallback_message(language)

    def _get_fallback_message(self, language: str = 'en') -> str:
        try:
            from resume.models import Translation
            translation = Translation.objects.filter(key='aiUnavailable', language=language).first()
            if translation:
                return translation.value
            translation_en = Translation.objects.filter(key='aiUnavailable', language='en').first()
            if translation_en:
                return translation_en.value
        except Exception:
            pass
        return "AI assistant is currently unavailable. Please try again later."
