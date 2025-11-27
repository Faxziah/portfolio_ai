from django.core.management.base import BaseCommand
from resume.models import Language, Skill, Experience, Education, Certificate, Project


class Command(BaseCommand):
    help = "Update order values for all resume models with interval of 10"

    def handle(self, *args, **options):
        self.stdout.write("Updating order intervals...")

        languages_en = Language.objects.filter(language="en").order_by('order', 'id')
        languages_ru = Language.objects.filter(language="ru").order_by('order', 'id')
        updated = 0
        for i, language in enumerate(languages_en, start=1):
            language.order = i * 10
            language.save()
            updated += 1
        for i, language in enumerate(languages_ru, start=1):
            language.order = i * 10
            language.save()
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} languages"))

        processed_categories = set()
        skills = Skill.objects.all().order_by('category_name_key', 'language', 'order', 'id')
        updated = 0
        for skill in skills:
            category_key = (skill.category_name_key, skill.language)
            if category_key not in processed_categories:
                category_skills = Skill.objects.filter(
                    category_name_key=skill.category_name_key,
                    language=skill.language
                ).order_by('order', 'id')
                
                for i, s in enumerate(category_skills, start=1):
                    s.order = i * 10
                    s.save()
                    updated += 1
                
                processed_categories.add(category_key)
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} skills"))

        experiences = Experience.objects.all().order_by('order', 'id')
        updated = 0
        for i, experience in enumerate(experiences, start=1):
            experience.order = i * 10
            experience.save()
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} experiences"))

        educations = Education.objects.all().order_by('-order', '-year', 'id')
        updated = 0
        for i, education in enumerate(educations, start=1):
            education.order = i * 10
            education.save()
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} educations"))

        certificates = Certificate.objects.all().order_by('order', 'id')
        updated = 0
        for i, certificate in enumerate(certificates, start=1):
            certificate.order = i * 10
            certificate.save()
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} certificates"))

        projects = Project.objects.all().order_by('order', 'id')
        updated = 0
        for i, project in enumerate(projects, start=1):
            project.order = i * 10
            project.save()
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} projects"))

        self.stdout.write(self.style.SUCCESS("Successfully updated all order intervals!"))

