from django.db import models


class Resume(models.Model):
    language = models.CharField(max_length=10, default="en", help_text="Language code (e.g., en, ru, zh)")
    firstname = models.CharField(max_length=100, help_text="First name")
    lastname = models.CharField(max_length=100, help_text="Last name")
    resume_title = models.CharField(max_length=200, help_text="Title for hero section")
    resume_description = models.TextField(help_text="Short description for hero section")
    about_me = models.TextField(help_text="Full description for About section")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "resume"
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"
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
        verbose_name = "Language"
        verbose_name_plural = "Languages"

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
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

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
        verbose_name = "Experience"
        verbose_name_plural = "Experience"

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
        verbose_name = "Education"
        verbose_name_plural = "Education"

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
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"

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
        verbose_name = "Project"
        verbose_name_plural = "Projects"
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
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

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
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
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
        verbose_name = "Translation"
        verbose_name_plural = "Translations"
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
        verbose_name = "Visit"
        verbose_name_plural = "Visits"
        indexes = [
            models.Index(fields=['-last_visit']),
            models.Index(fields=['session_id']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['page']),
        ]
    
    def __str__(self):
        duration = (self.last_visit - self.first_visit).total_seconds() if self.last_visit and self.first_visit else 0
        return f"{self.ip_address} - {self.page} - {self.first_visit.strftime('%Y-%m-%d %H:%M')} ({int(duration)}s)"
