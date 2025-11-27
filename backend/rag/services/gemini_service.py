"""
Gemini API service for AI chat functionality.
Uses gemini-2.0-flash-exp model (latest as of 2025).
"""
import google.generativeai as genai
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
        """Get API key from settings table."""
        try:
            from resume.models import Setting
            setting = Setting.objects.filter(name='gemini_api_key').first()
            if setting and setting.value:
                return setting.value
        except Exception:
            pass
        return ''
    
    def chat(
        self, 
        message: str, 
        chat_history: Optional[List[Dict]] = None,
        resume_md: Optional[str] = None
    ) -> str:
        """
        Send message to Gemini API.
        
        Args:
            message: User's question
            chat_history: Previous conversation in format:
                [{"role": "user", "parts": "..."}, {"role": "model", "parts": "..."}]
            resume_md: Markdown resume (include only on first message)
        
        Returns:
            AI response text
        """
        # Build conversation history
        history = []
        
        # Add system prompt and resume on first message
        if resume_md:
            system_message = (
                "You are a helpful assistant for a portfolio website. "
                "Below is the owner's resume in Markdown format. "
                "Answer questions about their experience, skills, and projects based on this information. "
                "Be concise, professional, and friendly.\n\n"
                f"RESUME:\n{resume_md}"
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
        
        # Send message
        try:
            response = chat.send_message(message)
            return response.text
        except Exception as e:
            # Return fallback message
            return self._get_fallback_message()
    
    def _get_fallback_message(self) -> str:
        """Get fallback message when API fails."""
        try:
            from resume.models import Setting
            # Try to get language-specific message
            # For now, return English default
            setting = Setting.objects.filter(name='ai_unavailable_message_en').first()
            if setting:
                return setting.value
        except Exception:
            pass
        return "AI assistant is currently unavailable. Please try again later."

