from rest_framework import serializers
import base64
from .models import Resume, Language, Skill, Experience, Education, Certificate, Project, ContactInfo, Carousel, Review, Price, Document


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name", "level", "proficiency", "order"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category_name", "category_name_key", "category_color", "order"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ["id", "company", "position", "start_date", "end_date", "description", "order"]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "institution", "location", "degree", "faculty", "year", "order"]


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "name", "year", "order"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "code", "title", "description", "technologies", "link", "order"]


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ["id", "type", "label", "value", "href", "order"]


class CarouselSerializer(serializers.ModelSerializer):
    photo_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Carousel
        fields = ["id", "type", "description", "photo_base64", "photo_mime_type", "video_url", "order"]

    def get_photo_base64(self, obj):
        if obj.photo_data:
            return base64.b64encode(obj.photo_data).decode('utf-8')
        return None


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "stars", "text", "author", "order", "created_at"]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["id", "name", "price", "currency", "order"]


class DocumentSerializer(serializers.ModelSerializer):
    photo_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ["id", "description", "photo_base64", "photo_mime_type", "order"]

    def get_photo_base64(self, obj):
        if obj.photo_data:
            return base64.b64encode(obj.photo_data).decode('utf-8')
        return None

