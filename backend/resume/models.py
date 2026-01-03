from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Resume(models.Model):
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    firstname = models.CharField(max_length=100, help_text="First name")
    lastname = models.CharField(max_length=100, help_text="Last name")
    patronymic = models.CharField(max_length=100, blank=True, default="", help_text="Patronymic/Middle name (for Russian)")
    resume_title = models.CharField(max_length=200, help_text="Title for hero section")
    resume_description = models.TextField(help_text="Short description for hero section")
    about_me = models.TextField(help_text="Full description for About section")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume"
        verbose_name = _("Resume")
        verbose_name_plural = _("Resumes")
        unique_together = [["language"]]

    def __str__(self):
        return f"Resume ({self.language})"

    @classmethod
    def load(cls, language="en"):
        defaults_map = {
            "en": {
                "firstname": "John",
                "lastname": "Doe",
                "resume_title": "Team Lead, Senior Backend (Fullstack) Developer",
                "resume_description": "Building scalable applications with 8+ years of experience in full-stack development, team leadership, and modern technologies",
                "about_me": "full-stack developer and team lead with expertise in building scalable web applications. I specialize in backend development while maintaining strong full-stack capabilities. Currently leading technical teams and architecting complex systems.",
            },
            "ru": {
                "firstname": "Иван",
                "lastname": "Иванов",
                "resume_title": "Тим лид, Senior Бекенд (Фуллстек) разработчик",
                "resume_description": "Создание масштабируемых приложений с опытом 8+ лет в фуллстек разработке, руководстве командами и современных технологиях",
                "about_me": "фуллстек разработчик и тимлид с экспертизой в создании масштабируемых веб-приложений. Специализируюсь на backend-разработке, сохраняя сильные фуллстек навыки. В настоящее время руковожу техническими командами и проектирую сложные системы.",
            },
            "zh": {
                "firstname": "张",
                "lastname": "伟",
                "resume_title": "团队负责人，高级后端（全栈）开发工程师",
                "resume_description": "拥有8年以上全栈开发、团队领导和现代技术经验，构建可扩展应用程序",
                "about_me": "全栈开发工程师和团队负责人，专注于构建可扩展的Web应用程序。我专注于后端开发，同时保持强大的全栈能力。目前领导技术团队并设计复杂系统。",
            }
        }
        
        obj, created = cls.objects.get_or_create(
            language=language,
            defaults=defaults_map.get(language, defaults_map["en"])
        )
        return obj


class Language(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=0, help_text="Proficiency percentage (0-100)")
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_language"
        ordering = ["order", "name"]
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return f"{self.name} - {self.level}"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category_name = models.CharField(max_length=100)
    category_name_key = models.CharField(max_length=100, help_text="Key for category translation")
    category_color = models.CharField(max_length=100, default="from-blue-500 to-cyan-500", help_text="CSS classes for gradient")
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_skill"
        ordering = ["category_name_key", "order", "name"]
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    def __str__(self):
        return f"{self.category_name}: {self.name}"


class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    start_date = models.CharField(max_length=50, help_text="E.g.: Aug 2024")
    end_date = models.CharField(max_length=50, help_text="E.g.: Present or Aug 2024")
    description = models.TextField()
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_experience"
        ordering = ["order", "-start_date"]
        verbose_name = _("Experience")
        verbose_name_plural = _("Experience")

    def __str__(self):
        return f"{self.position} at {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, help_text="Location (e.g., CA, USA)")
    degree = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200, blank=True, help_text="Faculty or major")
    year = models.CharField(max_length=50)
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_education"
        ordering = ["order", "-year"]
        verbose_name = _("Education")
        verbose_name_plural = _("Education")

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Certificate(models.Model):
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=50, blank=True, help_text="Certificate year")
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_certificate"
        ordering = ["order", "name"]
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")

    def __str__(self):
        return self.name


class Project(models.Model):
    code = models.CharField(max_length=100, help_text="Unique project code (e.g.: ai-text-tools, simple-alarm)")
    title = models.CharField(max_length=200, help_text="Project title")
    description = models.TextField(help_text="Project description")
    technologies = models.JSONField(default=list, help_text="List of technologies")
    link = models.URLField(blank=True, default="#")
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_project"
        ordering = ["order"]
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        unique_together = [["code", "language"]]

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    type = models.CharField(max_length=50, help_text="Contact type: phone, email, github, telegram, hh, etc.")
    label = models.CharField(max_length=100, help_text="Contact label (Phone, Email, GitHub, etc.)")
    value = models.CharField(max_length=200, help_text="Contact value")
    href = models.URLField(help_text="Contact link")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_contact_info"
        ordering = ["order"]
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return f"{self.label}: {self.value}"


class Setting(models.Model):
    """Application settings configurable through admin."""

    THEME_CHOICES = [
        ('blue', 'Blue Ocean'),
        ('green', 'Forest Green'),
        ('purple', 'Royal Purple'),
        ('orange', 'Sunset Orange'),
        ('red', 'Ruby Red'),
        ('cyan', 'Cyan Blue'),
        ('custom', 'Custom (hex color)'),
    ]

    name = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.TextField()
    description = models.TextField(blank=True, help_text="What this setting does")
    
    class Meta:
        db_table = "setting"
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Translation(models.Model):
    """Multi-language translations for UI elements."""
    
    key = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Translation key (e.g., 'certificates', 'education')"
    )
    language = models.CharField(
        max_length=10,
        db_index=True,
        help_text="Language code (e.g., 'en', 'ru', 'zh')"
    )
    value = models.CharField(
        max_length=255,
        help_text="Translated text"
    )
    
    class Meta:
        unique_together = ['key', 'language']
        verbose_name = _("Translation")
        verbose_name_plural = _("Translations")
        ordering = ['key', 'language']
        indexes = [
            models.Index(fields=['key', 'language']),
        ]

    def __str__(self):
        return f"{self.key} ({self.language})"


class Visit(models.Model):
    """Track website visitors with session-based tracking."""

    session_id = models.CharField(max_length=100, db_index=True, help_text="Unique session identifier")
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referer = models.URLField(blank=True, null=True, max_length=500)
    page = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    first_visit = models.DateTimeField(auto_now_add=True, db_index=True, help_text="First visit timestamp")
    last_visit = models.DateTimeField(auto_now=True, help_text="Last visit timestamp (updated on each request)")

    class Meta:
        db_table = "visit"
        ordering = ['-last_visit']
        verbose_name = _("Visit")
        verbose_name_plural = _("Visits")
        indexes = [
            models.Index(fields=['-last_visit']),
            models.Index(fields=['session_id']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['page']),
        ]

    def __str__(self):
        duration = (self.last_visit - self.first_visit).total_seconds() if self.last_visit and self.first_visit else 0
        return f"{self.ip_address} - {self.page} - {self.first_visit.strftime('%Y-%m-%d %H:%M')} ({int(duration)}s)"


class Carousel(models.Model):
    """Carousel items for photo/video gallery."""

    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='photo', help_text="Type: photo or video")
    description = models.TextField(blank=True, help_text="Description of the item")
    photo_data = models.BinaryField(blank=True, null=True, help_text="Photo stored as binary data")
    photo_mime_type = models.CharField(max_length=50, blank=True, null=True, help_text="MIME type of the photo (e.g., image/jpeg)")
    video_url = models.URLField(blank=True, help_text="URL for video (e.g., YouTube link)")
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(default=timezone.now, help_text="Date created (editable)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_carousel"
        ordering = ["order"]
        verbose_name = _("Carousel Item")
        verbose_name_plural = _("Carousel Items")

    def __str__(self):
        return f"{self.type.capitalize()}: {self.description[:50] if self.description else 'No description'}"


class Review(models.Model):
    """Customer reviews/testimonials."""

    stars = models.IntegerField(default=5, help_text="Rating from 1 to 5 stars")
    text = models.TextField(help_text="Review text")
    author = models.CharField(max_length=100, blank=True, help_text="Author name (optional)")
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(default=timezone.now, help_text="Date created (editable)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_review"
        ordering = ["order", "-created_at"]
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return f"{'★' * self.stars}{'☆' * (5 - self.stars)} - {self.text[:50]}..."


class Price(models.Model):
    """Services and pricing."""

    name = models.CharField(max_length=200, help_text="Service name")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price amount")
    currency = models.CharField(max_length=10, default="RUB", help_text="Currency code (e.g., RUB, USD, EUR)")
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_price"
        ordering = ["order", "name"]
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"


class Document(models.Model):
    """Documents/certificates stored as binary images."""

    description = models.TextField(blank=True, help_text="Description of the document")
    photo_data = models.BinaryField(help_text="Document image stored as binary data")
    photo_mime_type = models.CharField(max_length=50, default="image/jpeg", help_text="MIME type of the image")
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume_document"
        ordering = ["order"]
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __str__(self):
        return self.description[:50] if self.description else f"Document {self.id}"
