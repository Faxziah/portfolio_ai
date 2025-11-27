from rest_framework import serializers
from .models import Resume, Language, Skill, Experience, Education, Certificate, Project, ContactInfo


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

