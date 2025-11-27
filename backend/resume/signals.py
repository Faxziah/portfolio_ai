"""
Signals for handling language duplication when new languages are added.
"""
import json
import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender='resume.Setting')
def duplicate_content_for_new_language(sender, instance, **kwargs):
    """
    When site_languages setting is updated with a new language,
    duplicate all content from an existing language (prefer 'en').
    """
    if instance.name != 'site_languages':
        return

    try:
        new_languages = json.loads(instance.value)
        new_lang_codes = {lang['code'] for lang in new_languages}
    except (json.JSONDecodeError, KeyError, TypeError):
        return

    # Import models here to avoid circular imports
    from .models import (
        Resume, Language, Skill, Experience, Education,
        Certificate, Project, ContactInfo, Translation
    )

    # Models that have language field and should be duplicated
    models_to_duplicate = [
        Resume, Language, Skill, Experience, Education,
        Certificate, Project, ContactInfo, Translation
    ]

    # Find existing languages in the database
    existing_langs = set()
    for model in models_to_duplicate:
        existing_langs.update(
            model.objects.values_list('language', flat=True).distinct()
        )

    # Find new languages that don't have content yet
    new_langs_to_create = new_lang_codes - existing_langs
    if not new_langs_to_create:
        return

    # Choose source language (prefer 'en', then first available)
    source_lang = 'en' if 'en' in existing_langs else (list(existing_langs)[0] if existing_langs else None)
    if not source_lang:
        logger.warning("No source language found for duplication")
        return

    logger.info(f"Duplicating content from '{source_lang}' to new languages: {new_langs_to_create}")

    for new_lang in new_langs_to_create:
        for model in models_to_duplicate:
            _duplicate_model_entries(model, source_lang, new_lang)


def _duplicate_model_entries(model, source_lang, target_lang):
    """Duplicate all entries from source_lang to target_lang for a given model."""
    source_entries = model.objects.filter(language=source_lang)
    model_name = model.__name__

    for entry in source_entries:
        # Check if entry already exists for target language
        if model_name == 'Resume':
            # Resume is unique per language
            if model.objects.filter(language=target_lang).exists():
                continue
        elif hasattr(entry, 'code'):
            # Project has unique_together on (code, language)
            if model.objects.filter(code=entry.code, language=target_lang).exists():
                continue
        elif hasattr(entry, 'key'):
            # Translation has unique_together on (key, language)
            if model.objects.filter(key=entry.key, language=target_lang).exists():
                continue

        # Create a copy with the new language
        entry.pk = None
        entry.id = None
        entry.language = target_lang

        # Reset auto timestamps if present
        if hasattr(entry, 'created_at'):
            entry.created_at = None
        if hasattr(entry, 'updated_at'):
            entry.updated_at = None

        try:
            entry.save()
            logger.debug(f"Duplicated {model_name} to '{target_lang}'")
        except Exception as e:
            logger.warning(f"Failed to duplicate {model_name} to '{target_lang}': {e}")
