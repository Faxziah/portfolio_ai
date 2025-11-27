"""
Gemini API service for AI chat functionality.
Uses gemini-2.0-flash-exp model (latest as of 2025).
"""
import google.generativeai as genai
from django.conf import settings
from typing import List, Dict, Optional


class GeminiService:
    """Handle Gemini API interactions for resume chatbot."""
    
    def __init__(self):
        """Initialize Gemini with API key from settings."""
        api_key = self._get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def _get_api_key(self) -> str:
        """Get API key from settings table or environment."""
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
                [{"role": "user", "parts": "..."}, {"role": "model", "parts": "..."}]
            resume_context: Resume data from database (include only on first message)
            language: Language code for response

        Returns:
            AI response text
        """
        # Build conversation history
        history = []

        # Add system prompt and resume on first message
        if resume_context:
            system_message = (
                "You are a helpful assistant for a PUBLIC portfolio website. "
                "Below is the owner's resume information that they have CHOSEN TO PUBLISH PUBLICLY. "
                "Answer questions about their experience, skills, projects, languages, and contact information based on this data. "
                "IMPORTANT: All contact information (email, GitHub, LinkedIn, phone) is PUBLIC and meant to be shared with visitors. "
                "The 'Languages' section refers to SPOKEN/WRITTEN languages (like English, Spanish), NOT programming languages. "
                "IMPORTANT: Always respond in the SAME LANGUAGE as the user's question. If they ask in Russian, answer in Russian. If they ask in Chinese, answer in Chinese. "
                "Be concise, professional, and friendly. "
                "Keep your responses to a maximum of 100 words. Be brief and to the point.\n\n"
                f"RESUME:\n{resume_context}"
            )
            history.append({
                "role": "user",
                "parts": [system_message]
            })
            history.append({
                "role": "model",
                "parts": ["I understand. I'm ready to answer questions about this person's resume and experience."]
            })
        
        # Add previous chat history
        if chat_history:
            history.extend(chat_history)
        
        # Start chat with history
        chat = self.model.start_chat(history=history)
        
        # Send message with length constraint
        try:
            message_with_constraint = f"{message}\n\nIMPORTANT: Keep your response to a maximum of 100 words. Be brief and concise."
            response = chat.send_message(message_with_constraint)
            return response.text
        except Exception as e:
            # Return fallback message
            return self._get_fallback_message(language)
    
    def _get_fallback_message(self, language: str = 'en') -> str:
        """Get fallback message when API fails."""
        try:
            from resume.models import Translation
            translation = Translation.objects.filter(key='aiUnavailable', language=language).first()
            if translation:
                return translation.value
            # Fallback to English if translation not found
            translation_en = Translation.objects.filter(key='aiUnavailable', language='en').first()
            if translation_en:
                return translation_en.value
        except Exception:
            pass
        return "AI assistant is currently unavailable. Please try again later."

