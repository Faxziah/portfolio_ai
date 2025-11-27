from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .services.gemini_service import GeminiService
from .models import AIChatLog
import uuid
import logging

logger = logging.getLogger(__name__)


def get_resume_context(language: str) -> str:
    """
    Build resume context from database for AI.
    Returns formatted string with all resume data.
    """
    from resume.models import (
        Resume, Experience, Education, Skill,
        Certificate, Project, Language as LangModel, ContactInfo
    )

    parts = []

    # Basic info
    resume = Resume.objects.filter(language=language).first()
    if resume:
        parts.append(f"# {resume.firstname} {resume.lastname}")
        parts.append(f"**{resume.resume_title}**")
        parts.append(f"\n{resume.resume_description}")
        parts.append(f"\n## About\n{resume.about_me}")

    # Experience
    experiences = Experience.objects.filter(language=language).order_by('order')
    if experiences:
        parts.append("\n## Experience")
        for exp in experiences:
            parts.append(f"\n### {exp.position} at {exp.company}")
            parts.append(f"{exp.start_date} - {exp.end_date}")
            parts.append(exp.description)

    # Skills
    skills = Skill.objects.filter(language=language).order_by('category_name_key', 'order')
    if skills:
        parts.append("\n## Skills")
        current_category = None
        for skill in skills:
            if skill.category_name != current_category:
                current_category = skill.category_name
                parts.append(f"\n**{current_category}:**")
            parts.append(f"- {skill.name}")

    # Education
    education = Education.objects.filter(language=language).order_by('order')
    if education:
        parts.append("\n## Education")
        for edu in education:
            location = f", {edu.location}" if edu.location else ""
            faculty = f" - {edu.faculty}" if edu.faculty else ""
            parts.append(f"- {edu.degree}{faculty} at {edu.institution}{location} ({edu.year})")

    # Certificates
    certificates = Certificate.objects.filter(language=language).order_by('order')
    if certificates:
        parts.append("\n## Certificates")
        for cert in certificates:
            year = f" ({cert.year})" if cert.year else ""
            parts.append(f"- {cert.name}{year}")

    # Projects
    projects = Project.objects.filter(language=language).order_by('order')
    if projects:
        parts.append("\n## Projects")
        for proj in projects:
            techs = ", ".join(proj.technologies) if proj.technologies else ""
            parts.append(f"\n### {proj.title}")
            parts.append(proj.description)
            if techs:
                parts.append(f"Technologies: {techs}")

    # Languages
    languages = LangModel.objects.filter(language=language).order_by('order')
    if languages:
        parts.append("\n## Languages")
        for lang in languages:
            parts.append(f"- {lang.name}: {lang.level}")

    # Contact
    contacts = ContactInfo.objects.filter(language=language).order_by('order')
    if contacts:
        parts.append("\n## Contact")
        for contact in contacts:
            parts.append(f"- {contact.label}: {contact.value}")

    return "\n".join(parts)


@api_view(['POST'])
@permission_classes([AllowAny])
def ai_chat(request):
    """
    AI Chat endpoint using Gemini API.

    Request body:
    {
        "message": "What is your experience?",
        "chat_history": [  # Optional, empty on first message
            {"role": "user", "parts": ["Previous question"]},
            {"role": "model", "parts": ["Previous answer"]}
        ],
        "session_id": "uuid",  # Optional, for tracking conversation
        "language": "en"  # Optional, defaults to "en"
    }
    """
    message = request.data.get('message')
    chat_history = request.data.get('chat_history', [])
    session_id = request.data.get('session_id')
    language = request.data.get('language', 'en')

    if not message:
        return Response(
            {'error': 'Message is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not session_id:
        session_id = str(uuid.uuid4())

    # Check if API key is configured
    try:
        from resume.models import Setting
        api_key_setting = Setting.objects.filter(name='gemini_api_key').first()
        if not api_key_setting or not api_key_setting.value:
            return Response(
                {'error': 'No API key'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    except Exception as e:
        logger.warning(f"Error checking API key: {e}")
        return Response(
            {'error': 'No API key'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    # Get resume context from DB (always include for context)
    resume_context = None
    try:
        resume_context = get_resume_context(language)
    except Exception as e:
        logger.warning(f"Error fetching resume data: {e}")

    try:
        gemini = GeminiService()
        ai_response = gemini.chat(message, chat_history, resume_context, language)
    except ValueError as e:
        error_msg = str(e)
        if "GEMINI_API_KEY not configured" in error_msg or "not configured" in error_msg.lower():
            return Response(
                {'error': 'No API key'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        return Response(
            {'error': str(e)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"AI service error: {e}")
        return Response(
            {'error': 'AI service error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Log chat interaction
    try:
        AIChatLog.objects.create(
            session_id=session_id,
            user_message=message,
            ai_response=ai_response,
            language=language
        )
    except Exception as e:
        logger.warning(f"Error saving chat log: {e}")

    return Response({
        'response': ai_response,
        'session_id': session_id
    })
