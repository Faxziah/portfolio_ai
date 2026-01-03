from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
import base64
from .models import Resume, Language, Skill, Experience, Education, Certificate, Project, ContactInfo, Visit, Setting, Translation, Carousel, Review, Price, Document


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["language", "lastname", "firstname", "patronymic", "updated_at"]
    list_filter = ["language"]

    fieldsets = (
        ("Language", {
            "fields": ("language",)
        }),
        ("Personal Information", {
            "fields": ("lastname", "firstname", "patronymic"),
            "description": "For Russian: ФИО (Фамилия Имя Отчество). For English: First Last."
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


class ThemeSettingForm(forms.ModelForm):
    """Custom form for theme setting with color picker."""

    THEME_CHOICES = [
        ('blue', 'Blue Ocean'),
        ('green', 'Forest Green'),
        ('purple', 'Royal Purple'),
        ('orange', 'Sunset Orange'),
        ('red', 'Ruby Red'),
        ('cyan', 'Cyan Blue'),
    ]

    theme_preset = forms.ChoiceField(
        choices=THEME_CHOICES,
        required=False,
        label='Theme Preset'
    )
    theme_custom = forms.CharField(
        required=False,
        label='Custom Color',
        widget=forms.TextInput(attrs={
            'type': 'color',
            'style': 'width: 60px; height: 40px; padding: 0; border: none; cursor: pointer;',
            'id': 'id_theme_custom'
        })
    )

    class Meta:
        model = Setting
        fields = ['name', 'value', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.name == 'theme':
            value = self.instance.value
            if value.startswith('#'):
                self.fields['theme_custom'].initial = value
                self.fields['theme_preset'].initial = 'blue'
            else:
                self.fields['theme_preset'].initial = value
                self.fields['theme_custom'].initial = '#3b82f6'


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Admin for application settings."""

    list_display = ['name', 'value_preview', 'description']
    search_fields = ['name', 'value', 'description']

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.name == 'theme':
            return ThemeSettingForm
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj and obj.name == 'theme':
            return [
                ('Theme Settings', {
                    'fields': ['name', 'theme_preset', 'theme_custom', 'value'],
                    'description': 'Select a preset theme or pick a custom color. The color picker updates the Value field automatically.'
                }),
                ('Help', {
                    'fields': ['description'],
                    'classes': ['collapse'],
                }),
            ]
        return [
            ('Setting', {
                'fields': ['name', 'value'],
            }),
            ('Help', {
                'fields': ['description'],
                'classes': ['collapse'],
            }),
        ]

    class Media:
        js = ('admin/js/theme_color_picker.js',)

    def save_model(self, request, obj, form, change):
        # For theme setting, the value field is updated via JS from color picker
        # Just save whatever is in the value field
        super().save_model(request, obj, form, change)

    def value_preview(self, obj):
        """Show truncated value with color preview for theme."""
        if obj.name == 'theme' and obj.value.startswith('#'):
            return format_html(
                '<span style="display:inline-block;width:20px;height:20px;background:{};border:1px solid #ccc;vertical-align:middle;margin-right:5px;"></span> {}',
                obj.value, obj.value
            )
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


class CarouselAdminForm(forms.ModelForm):
    """Custom form for Carousel with file upload."""

    photo_upload = forms.FileField(required=False, label='Upload Photo', help_text='Upload an image file (JPEG, PNG, etc.)')

    class Meta:
        model = Carousel
        fields = ['type', 'description', 'video_url', 'language', 'order']

    def save(self, commit=True):
        instance = super().save(commit=False)
        photo_file = self.cleaned_data.get('photo_upload')
        if photo_file:
            instance.photo_data = photo_file.read()
            instance.photo_mime_type = photo_file.content_type
        if commit:
            instance.save()
        return instance


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    """Admin for carousel items."""

    form = CarouselAdminForm
    list_display = ['description', 'type', 'language', 'order', 'created_at', 'photo_preview', 'video_url']
    list_display_links = ['description']
    list_editable = ['order']
    list_filter = ['type', 'language']
    search_fields = ['description']
    ordering = ['order']

    fieldsets = [
        ('Item Info', {
            'fields': ['type', 'description', 'language', 'order', 'created_at'],
        }),
        ('Photo', {
            'fields': ['photo_upload'],
            'classes': ['collapse'],
            'description': 'Upload a photo for this carousel item (only for type "photo")'
        }),
        ('Video', {
            'fields': ['video_url'],
            'classes': ['collapse'],
            'description': 'Enter a video URL (e.g., YouTube) for this carousel item (only for type "video")'
        }),
    ]

    def photo_preview(self, obj):
        """Show photo preview."""
        if obj.photo_data and obj.photo_mime_type:
            data = base64.b64encode(obj.photo_data).decode('utf-8')
            return format_html(
                '<img src="data:{};base64,{}" style="max-width:100px;max-height:60px;"/>',
                obj.photo_mime_type, data
            )
        return '-'
    photo_preview.short_description = 'Photo'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin for reviews."""

    list_display = ['stars_display', 'text_preview', 'author', 'created_at', 'language', 'order']
    list_display_links = ['stars_display', 'text_preview']
    list_editable = ['order']
    list_filter = ['stars', 'language']
    search_fields = ['text', 'author']
    ordering = ['order', '-created_at']

    fieldsets = [
        ('Review', {
            'fields': ['stars', 'text', 'author', 'created_at', 'language', 'order'],
        }),
    ]

    def stars_display(self, obj):
        """Show stars as visual rating."""
        return '★' * obj.stars + '☆' * (5 - obj.stars)
    stars_display.short_description = 'Rating'

    def text_preview(self, obj):
        """Show truncated text."""
        return (obj.text[:80] + '...') if len(obj.text) > 80 else obj.text
    text_preview.short_description = 'Review'


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """Admin for prices/services."""

    list_display = ['name', 'price', 'currency', 'language', 'order']
    list_editable = ['order', 'price']
    list_filter = ['currency', 'language']
    search_fields = ['name']
    ordering = ['order', 'name']

    fieldsets = [
        ('Service', {
            'fields': ['name', 'price', 'currency', 'language', 'order'],
        }),
    ]


class DocumentAdminForm(forms.ModelForm):
    """Custom form for Document with file upload."""

    photo_upload = forms.FileField(required=False, label='Upload Photo', help_text='Upload a document image (JPEG, PNG, etc.)')

    class Meta:
        model = Document
        fields = ['description', 'language', 'order']

    def save(self, commit=True):
        instance = super().save(commit=False)
        photo_file = self.cleaned_data.get('photo_upload')
        if photo_file:
            instance.photo_data = photo_file.read()
            instance.photo_mime_type = photo_file.content_type
        if commit:
            instance.save()
        return instance


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin for documents."""

    form = DocumentAdminForm
    list_display = ['description_short', 'language', 'order', 'photo_preview']
    list_editable = ['order']
    list_filter = ['language']
    search_fields = ['description']
    ordering = ['order']

    fieldsets = [
        ('Document', {
            'fields': ['description', 'photo_upload', 'language', 'order'],
        }),
    ]

    def description_short(self, obj):
        """Show short description."""
        return obj.description[:50] if obj.description else '-'
    description_short.short_description = 'Description'

    def photo_preview(self, obj):
        """Show photo preview."""
        if obj.photo_data and obj.photo_mime_type:
            data = base64.b64encode(obj.photo_data).decode('utf-8')
            return format_html(
                '<img src="data:{};base64,{}" style="max-width:100px;max-height:60px;"/>',
                obj.photo_mime_type, data
            )
        return '-'
    photo_preview.short_description = 'Preview'


admin.site.site_header = _("Portfolio Administration")
admin.site.site_title = _("Portfolio")
admin.site.index_title = _("My Resume")
