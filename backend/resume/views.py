from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Resume, Language, Skill, Experience, Education, Certificate, Project, ContactInfo, Setting, Translation, Visit
from .serializers import (
    LanguageSerializer, ExperienceSerializer,
    EducationSerializer, CertificateSerializer, ProjectSerializer, ContactInfoSerializer
)
import logging
import json

logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_resume(request):
    try:
        lang = request.GET.get("lang", "en")
        
        # Get valid languages from settings
        valid_langs = ["en"]
        try:
            site_languages_setting = Setting.objects.filter(name='site_languages').first()
            if site_languages_setting:
                valid_langs = [l['code'] for l in json.loads(site_languages_setting.value)]
                if lang not in valid_langs:
                    lang = valid_langs[0] if valid_langs else "en"
        except:
            pass

        # Load all resumes dynamically from DB
        resumes = {}
        for lang_code in valid_langs:
            resumes[lang_code] = Resume.load(lang_code)
        languages = Language.objects.filter(language=lang)
        skills = Skill.objects.filter(language=lang).order_by("category_name_key", "order", "name")
        experiences = Experience.objects.filter(language=lang)
        education = Education.objects.filter(language=lang)
        certificates = Certificate.objects.filter(language=lang)
        projects = Project.objects.filter(language=lang)
        contact_info = ContactInfo.objects.filter(language=lang).order_by("order")
        
        unique_projects_count = Project.objects.filter(language=lang).count()
        languages_count = Language.objects.filter(language=lang).count()
        
        # Подсчет опыта работы: суммируем месяцы из всех уникальных периодов
        years_experience = "8+"
        try:
            from datetime import datetime
            from dateutil.relativedelta import relativedelta
            import calendar
            
            # Load month translations from DB
            month_translations = {}
            for translation in Translation.objects.filter(key__startswith='month_'):
                lang_code = translation.language
                key = translation.key
                # Extract month number from key (month_1_full -> 1, month_12_short -> 12)
                if '_full' in key or '_short' in key:
                    month_num = int(key.replace('month_', '').replace('_full', '').replace('_short', ''))
                else:
                    continue
                
                if lang_code not in month_translations:
                    month_translations[lang_code] = {}
                month_translations[lang_code][translation.value.lower()] = month_num
            
            # Маппинг английских месяцев
            en_months = {month.lower(): i for i, month in enumerate(calendar.month_abbr[1:], 1)}
            en_months.update({month.lower(): i for i, month in enumerate(calendar.month_name[1:], 1)})
            
            def parse_date(date_str):
                """Парсит дату в формате 'Aug 2024' или 'Авг 2024'"""
                # Load present values dynamically from translations
                present_values = []
                for trans in Translation.objects.filter(key='present'):
                    present_values.append(trans.value.lower())
                
                if not date_str or date_str.lower() in present_values:
                    return datetime.now()
                
                parts = date_str.strip().split()
                if len(parts) >= 2:
                    month_str = parts[0].lower()
                    year_str = parts[-1]
                    
                    if year_str.isdigit():
                        year = int(year_str)
                        month = None
                        
                        # Пробуем найти месяц в переводах для всех языков
                        for lang_code, months_dict in month_translations.items():
                            for month_name, month_num in months_dict.items():
                                if month_str.startswith(month_name):
                                    month = month_num
                                    break
                            if month:
                                break
                        
                        # Если не нашли, пробуем английские
                        if month is None:
                            month = en_months.get(month_str, 1)
                        
                        return datetime(year, month, 1)
                
                # Если не удалось распарсить, берем год из конца строки
                year_str = ''.join(filter(str.isdigit, date_str))
                if year_str:
                    return datetime(int(year_str), 1, 1)
                
                return datetime.now()
            
            # Получаем уникальные периоды работы (по компании и датам, без учета языка)
            # Используем только английские версии для подсчета
            experiences_for_calc = Experience.objects.filter(language="en")
            unique_periods = {}
            
            for exp in experiences_for_calc:
                # Нормализуем даты для сравнения (убираем языковые различия)
                start_normalized = exp.start_date
                end_normalized = exp.end_date
                
                key = (exp.company, start_normalized, end_normalized)
                if key not in unique_periods:
                    unique_periods[key] = exp
            
            # Суммируем месяцы
            total_months = 0
            for exp in unique_periods.values():
                start = parse_date(exp.start_date)
                end = parse_date(exp.end_date)
                
                delta = relativedelta(end, start)
                months = delta.years * 12 + delta.months
                if months > 0:
                    total_months += months
            
            # Конвертируем в годы
            years = total_months // 12
            if years > 0:
                years_experience = f"{years}+"
            else:
                months_only = total_months
                years_experience = f"{months_only}+" if months_only > 0 else "0+"
        except Exception as e:
            logger.exception(f"Error calculating years_experience: {e}")
            years_experience = "8+"

        skills_dict = {}
        for skill in skills:
            if skill.category_name_key not in skills_dict:
                skills_dict[skill.category_name_key] = []
            skills_dict[skill.category_name_key].append(skill.name)

        skills_data = {}
        category_orders = {}
        for skill in skills:
            category_key = skill.category_name_key
            if category_key not in skills_data:
                skills_data[category_key] = {
                    "id": category_key,
                    "name": skill.category_name,
                    "name_key": skill.category_name_key,
                    "color": skill.category_color,
                    "order": skill.order,
                    "skills": []
                }
                category_orders[category_key] = skill.order
            else:
                category_orders[category_key] = min(category_orders[category_key], skill.order)
            skills_data[category_key]["skills"].append({
                "id": skill.id,
                "name": skill.name,
                "order": skill.order
            })
        
        for category_key in skills_data:
            skills_data[category_key]["order"] = category_orders[category_key]

        # Build dynamic response with all languages from DB
        name_dict = {}
        firstname_dict = {}
        lastname_dict = {}
        about_me_dict = {}
        resume_description_dict = {}
        resume_title_dict = {}
        
        for lang_code, resume_obj in resumes.items():
            name_dict[lang_code] = f"{resume_obj.firstname} {resume_obj.lastname}"
            firstname_dict[lang_code] = resume_obj.firstname
            lastname_dict[lang_code] = resume_obj.lastname
            about_me_dict[lang_code] = resume_obj.about_me or ""
            resume_description_dict[lang_code] = resume_obj.resume_description or ""
            resume_title_dict[lang_code] = resume_obj.resume_title or ""
        
        return Response({
            "name": name_dict,
            "firstname": firstname_dict,
            "lastname": lastname_dict,
            "languages": LanguageSerializer(languages, many=True).data,
            "skills": skills_dict,
            "skill_categories": list(skills_data.values()),
            "experiences": ExperienceSerializer(experiences, many=True).data,
            "education": EducationSerializer(education, many=True).data,
            "certificates": CertificateSerializer(certificates, many=True).data,
            "projects": ProjectSerializer(projects, many=True).data,
            "about_me": about_me_dict,
            "resume_description": resume_description_dict,
            "resume_title": resume_title_dict,
            "contact_info": ContactInfoSerializer(contact_info, many=True).data,
            "stats": {
                "years_experience": years_experience,
                "projects_completed": str(unique_projects_count),
                "languages_count": str(languages_count),
            },
        })
    except Exception as e:
        logger.exception("Error in get_resume endpoint")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_client_ip(request):
    """Get real IP address, considering proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def track_visit(request):
    """Track visit from API request using session cookie."""
    try:
        session_id = request.COOKIES.get('sessionid') or request.META.get('HTTP_X_SESSION_ID')
        if not session_id:
            # Generate a session ID from IP + User-Agent hash
            import hashlib
            ip = get_client_ip(request)
            ua = request.META.get('HTTP_USER_AGENT', '')[:100]
            session_id = hashlib.md5(f"{ip}{ua}".encode()).hexdigest()

        visit = Visit.objects.filter(session_id=session_id).first()
        if visit:
            visit.save(update_fields=['last_visit'])
        else:
            Visit.objects.create(
                session_id=session_id,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                referer=request.META.get('HTTP_REFERER', '')[:500] if request.META.get('HTTP_REFERER') else None,
                page='/'
            )
    except Exception as e:
        logger.warning(f"Visit tracking error: {e}")


@api_view(['GET'])
@permission_classes([AllowAny])
def get_settings(request):
    """
    Get public settings.
    Returns: { "theme": "blue", "site_languages": [{code, name, flag}], ... }
    """
    # Track visit on settings load (first API call from frontend)
    track_visit(request)

    settings = {}
    for setting in Setting.objects.all():
        if setting.name in ['site_languages', 'available_languages']:
            try:
                settings[setting.name] = json.loads(setting.value)
            except:
                settings[setting.name] = [{'code': 'en', 'name': 'English', 'flag': '🇺🇸'}]
        else:
            settings[setting.name] = setting.value

    return Response(settings)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_translations(request):
    """
    Get all translations.
    Returns: { "en": {"certificates": "Certifications"}, "ru": {...} }
    """
    lang = request.GET.get('lang', 'en')
    
    translations = {}
    for t in Translation.objects.filter(language=lang):
        translations[t.key] = t.value
    
    return Response(translations)
