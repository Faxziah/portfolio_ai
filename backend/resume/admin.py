from django.contrib import admin
from .models import Resume, Language, Skill, Experience, Education, Certificate, Project, ContactInfo, Visit, Setting, Translation


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["language", "firstname", "lastname", "updated_at"]
    list_filter = ["language"]
    
    fieldsets = (
        ("Language", {
            "fields": ("language",)
        }),
        ("Personal Information", {
            "fields": ("firstname", "lastname")
        }),
        ("Hero Section", {
            "fields": (
                "resume_title",
                "resume_description",
            )
        }),
        ("About Section", {
            "fields": ("about_me",)
        }),
    )




@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "level", "proficiency", "language", "order"]
    list_editable = ["order"]
    list_filter = ["level", "language"]
    search_fields = ["name", "level"]
    fields = ("name", "level", "proficiency", "language", "order")
    ordering = ["order", "name"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category_name", "category_name_key", "language", "order"]
    list_editable = ["order"]
    list_filter = ["category_name_key", "language"]
    search_fields = ["name", "category_name", "category_name_key"]
    fields = ("name", "category_name", "category_name_key", "category_color", "language", "order")
    ordering = ["category_name_key", "order", "name"]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["position", "company", "language", "start_date", "end_date", "order"]
    list_editable = ["order"]
    list_filter = ["company", "start_date", "language"]
    search_fields = ["company", "position", "description"]
    fields = ("company", "position", "start_date", "end_date", "description", "language", "order")
    ordering = ["order", "-start_date"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "location", "faculty", "language", "year", "order"]
    list_editable = ["order"]
    list_filter = ["year", "language"]
    search_fields = ["institution", "degree", "faculty", "location"]
    fields = ("institution", "location", "degree", "faculty", "year", "language", "order")
    ordering = ["-order", "-year"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["name", "year", "language", "order"]
    list_editable = ["order"]
    list_filter = ["language", "year"]
    search_fields = ["name", "year"]
    fields = ("name", "year", "language", "order")
    ordering = ["order", "name"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "language", "link", "technologies_display", "order"]
    list_editable = ["order"]
    list_filter = ["language"]
    search_fields = ["code", "title", "description"]
    fields = ("code", "title", "description", "technologies", "link", "language", "order")
    ordering = ["order"]
    
    def technologies_display(self, obj):
        if obj.technologies:
            return ", ".join(obj.technologies)
        return "-"
    technologies_display.short_description = "Technologies"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ["label", "type", "value", "language", "order"]
    list_editable = ["order"]
    list_filter = ["language", "type"]
    search_fields = ["label", "value"]
    fields = ("language", "type", "label", "value", "href", "order")
    ordering = ["order"]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Admin for application settings."""

    list_display = ['name', 'value_preview', 'description']
    search_fields = ['name', 'value', 'description']

    fieldsets = [
        ('Setting', {
            'fields': ['name', 'value'],
        }),
        ('Help', {
            'fields': ['description'],
            'classes': ['collapse'],
        }),
    ]

    def value_preview(self, obj):
        """Show truncated value."""
        return (obj.value[:50] + '...') if len(obj.value) > 50 else obj.value
    value_preview.short_description = 'Value'


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    """Admin for managing translations."""
    
    list_display = ['key', 'language', 'value']
    list_filter = ['language']
    search_fields = ['key', 'value']
    
    fieldsets = [
        ('Translation', {
            'fields': ['key', 'language', 'value'],
        }),
    ]


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    """Admin for viewing visitor statistics."""
    
    list_display = ['first_visit', 'last_visit', 'duration_display', 'ip_address', 'page', 'session_id_short']
    list_filter = ['first_visit', 'page']
    search_fields = ['ip_address', 'page', 'user_agent', 'session_id']
    date_hierarchy = 'first_visit'
    readonly_fields = ['session_id', 'first_visit', 'last_visit', 'duration_display', 'ip_address', 'user_agent', 'referer', 'page', 'country', 'city']
    
    fieldsets = [
        ('Session Info', {
            'fields': ['session_id', 'first_visit', 'last_visit', 'duration_display']
        }),
        ('User Info', {
            'fields': ['ip_address', 'user_agent', 'referer']
        }),
        ('Page Info', {
            'fields': ['page', 'country', 'city']
        }),
    ]
    
    def session_id_short(self, obj):
        """Show shortened session ID."""
        return obj.session_id[:8] + '...' if len(obj.session_id) > 8 else obj.session_id
    session_id_short.short_description = 'Session'
    
    def duration_display(self, obj):
        """Show visit duration in human-readable format."""
        if obj.first_visit and obj.last_visit:
            duration = (obj.last_visit - obj.first_visit).total_seconds()
            if duration < 60:
                return f"{int(duration)}s"
            elif duration < 3600:
                return f"{int(duration / 60)}m {int(duration % 60)}s"
            else:
                hours = int(duration / 3600)
                minutes = int((duration % 3600) / 60)
                return f"{hours}h {minutes}m"
        return "0s"
    duration_display.short_description = 'Duration'
    
    def has_add_permission(self, request):
        """Visits are created automatically."""
        return False


admin.site.site_header = "Portfolio Administration"
admin.site.site_title = "Portfolio"
admin.site.index_title = "My Resume"
