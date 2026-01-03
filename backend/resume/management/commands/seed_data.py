from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resume.models import (
    Setting, Translation, Resume, Experience, Education,
    Certificate, Project, Language, ContactInfo, Skill,
    Carousel, Review, Price, Document
)
import json
import os
import urllib.request
import urllib.error

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with John Doe test data'
    
    def handle(self, *args, **options):
        # Check if Resume table already has data - skip seeding if not empty
        if Resume.objects.exists():
            self.stdout.write(self.style.WARNING('⏭️  Database already has resume data. Skipping seed.'))
            return

        self.stdout.write('Seeding database...')

        # Create superuser
        self.create_superuser()
        
        # Create settings
        self.create_settings()
        
        # Create translations
        self.create_translations()
        
        # Create resume data
        self.create_resume_data()
        
        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))
    
    def create_superuser(self):
        """Create default admin user from environment variables."""
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(f'  ✓ Created superuser ({username})')
        else:
            self.stdout.write('  - Superuser already exists')
    
    def create_settings(self):
        """Create default settings."""
        settings_data = [
            {
                'name': 'theme',
                'value': 'blue',
                'description': 'Color theme: blue, green, purple, orange, red, cyan, or hex color (e.g., #A72A22)'
            },
            {
                'name': 'gemini_api_key',
                'value': '',
                'description': 'Google Gemini API key for AI chat'
            },
            {
                'name': 'site_languages',
                'value': json.dumps([
                    {'code': 'en', 'name': 'English', 'flag': '🇺🇸'},
                    {'code': 'ru', 'name': 'Русский', 'flag': '🇷🇺'},
                    {'code': 'zh', 'name': '中文', 'flag': '🇨🇳'}
                ], ensure_ascii=False),
                'description': 'Available site languages with codes, names, and flags (JSON array)'
            },
            {
                'name': 'default_language',
                'value': 'en',
                'description': 'Default language code'
            },
            {
                'name': 'show_carousel',
                'value': '1',
                'description': 'Show carousel section (1 = enabled, 0 = disabled)'
            },
            {
                'name': 'show_reviews',
                'value': '1',
                'description': 'Show reviews section (1 = enabled, 0 = disabled)'
            },
            {
                'name': 'show_prices',
                'value': '1',
                'description': 'Show prices section (1 = enabled, 0 = disabled)'
            },
            {
                'name': 'show_documents',
                'value': '1',
                'description': 'Show documents section (1 = enabled, 0 = disabled)'
            },
        ]
        
        created_count = 0
        for data in settings_data:
            obj, created = Setting.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                created_count += 1
        
        self.stdout.write(f'  ✓ Created/updated {len(settings_data)} settings ({created_count} new)')
    
    def create_translations(self):
        """Create UI translations."""
        translations = [
            # Navigation Menu
            {'key': 'navAbout', 'en': 'About', 'ru': 'Обо мне', 'zh': '关于'},
            {'key': 'navExperience', 'en': 'Experience', 'ru': 'Опыт', 'zh': '经验'},
            {'key': 'navSkills', 'en': 'Skills', 'ru': 'Навыки', 'zh': '技能'},
            {'key': 'navProjects', 'en': 'Projects', 'ru': 'Проекты', 'zh': '项目'},
            {'key': 'navEducation', 'en': 'Education', 'ru': 'Образование', 'zh': '教育'},
            {'key': 'navLanguages', 'en': 'Languages', 'ru': 'Языки', 'zh': '语言'},
            {'key': 'navContact', 'en': 'Contact', 'ru': 'Контакты', 'zh': '联系'},

            # Section Titles
            {'key': 'aboutTitle', 'en': 'About Me', 'ru': 'Обо мне', 'zh': '关于我'},
            {'key': 'experienceTitle', 'en': 'Work Experience', 'ru': 'Опыт работы', 'zh': '工作经验'},
            {'key': 'skillsTitle', 'en': 'Technical Skills', 'ru': 'Технические навыки', 'zh': '技术技能'},
            {'key': 'projectsTitle', 'en': 'Projects', 'ru': 'Проекты', 'zh': '项目'},
            {'key': 'educationTitle', 'en': 'Education', 'ru': 'Образование', 'zh': '教育'},
            {'key': 'certificationsTitle', 'en': 'Certifications', 'ru': 'Сертификаты', 'zh': '证书'},
            {'key': 'languagesTitle', 'en': 'Languages', 'ru': 'Языки', 'zh': '语言'},
            {'key': 'contactTitle', 'en': 'Get In Touch', 'ru': 'Контакты', 'zh': '联系方式'},
            
            # Connector words
            {'key': 'and', 'en': 'and', 'ru': 'и', 'zh': '和'},

            # Buttons
            {'key': 'viewProjects', 'en': 'View Projects', 'ru': 'Посмотреть проекты', 'zh': '查看项目'},
            {'key': 'contactMe', 'en': 'Contact Me', 'ru': 'Связаться', 'zh': '联系我'},
            {'key': 'viewProject', 'en': 'View Project', 'ru': 'Посмотреть проект', 'zh': '查看项目'},
            
            # Stats
            {'key': 'yearsExperience', 'en': 'Years Experience', 'ru': 'Лет опыта', 'zh': '年工作经验'},
            {'key': 'projectsCompleted', 'en': 'Projects Completed', 'ru': 'Проектов завершено', 'zh': '完成项目'},
            {'key': 'languages', 'en': 'Languages', 'ru': 'Языков', 'zh': '语言'},
            
            # Experience
            {'key': 'present', 'en': 'Present', 'ru': 'Настоящее время', 'zh': '至今'},
            {'key': 'company', 'en': 'Company', 'ru': 'Компания', 'zh': '公司'},
            
            # AI Chat
            {'key': 'aiChatTitle', 'en': 'AI Assistant', 'ru': 'AI Ассистент', 'zh': 'AI 助手'},
            {'key': 'aiChatSubtitle', 'en': 'Ask me about this portfolio', 'ru': 'Спросите меня о резюме', 'zh': '询问我有关简历的问题'},
            {'key': 'aiChatPlaceholder', 'en': 'Ask about experience, skills...', 'ru': 'Спросите об опыте, навыках...', 'zh': '询问经验、技能...'},
            {'key': 'aiChatSend', 'en': 'Send', 'ru': 'Отправить', 'zh': '发送'},
            {'key': 'aiChatWelcome', 'en': 'Hi! I\'m an AI assistant. Ask me about experience, skills, and projects of {name}!', 'ru': 'Привет! Я ИИ ассистент. Спросите меня об опыте, навыках и проектах {name}!', 'zh': '你好！我是AI助手。询问我关于{name}的经验、技能和项目！'},
            {'key': 'aiChatError', 'en': 'Sorry, I encountered an error. Please try again.', 'ru': 'Извините, произошла ошибка. Пожалуйста, попробуйте снова.', 'zh': '抱歉，发生错误。请重试。'},
            {'key': 'aiChatNoApiKey', 'en': 'Sorry, I encountered an error. No API key. Visit https://aistudio.google.com/app/apikey', 'ru': 'Извините, произошла ошибка. API ключ не настроен. Посетите https://aistudio.google.com/app/apikey', 'zh': '抱歉，发生错误。未配置API密钥。请访问 https://aistudio.google.com/app/apikey'},
            
            # Contact
            {'key': 'call', 'en': 'Call', 'ru': 'Позвонить', 'zh': '呼叫'},
            {'key': 'write', 'en': 'Write', 'ru': 'Написать', 'zh': '写信'},
            {'key': 'goTo', 'en': 'Go to', 'ru': 'Перейти', 'zh': '前往'},
            
            # Footer
            {'key': 'allRightsReserved', 'en': 'All rights reserved.', 'ru': 'Все права сохранены.', 'zh': '版权所有。'},

            # AI Unavailable
            {'key': 'aiUnavailable', 'en': 'AI assistant is currently unavailable. Please try again later.', 'ru': 'ИИ-ассистент временно недоступен. Попробуйте позже.', 'zh': 'AI助手暂时不可用。请稍后再试。'},

            # New sections
            {'key': 'carouselTitle', 'en': 'Gallery', 'ru': 'Галерея', 'zh': '图库'},
            {'key': 'reviewsTitle', 'en': 'Reviews', 'ru': 'Отзывы', 'zh': '评价'},
            {'key': 'pricesTitle', 'en': 'Services', 'ru': 'Услуги', 'zh': '服务'},
            {'key': 'documentsTitle', 'en': 'Documents', 'ru': 'Документы', 'zh': '文件'},

            # Show more/less buttons
            {'key': 'showMore', 'en': 'Show more', 'ru': 'Показать еще', 'zh': '显示更多'},
            {'key': 'showLess', 'en': 'Show less', 'ru': 'Скрыть', 'zh': '收起'},
            {'key': 'showFull', 'en': 'Show full', 'ru': 'Показать полностью', 'zh': '显示全部'},

            # Misc
            {'key': 'noContent', 'en': 'No content', 'ru': 'Нет содержимого', 'zh': '无内容'},
            {'key': 'noImage', 'en': 'No image', 'ru': 'Нет изображения', 'zh': '无图片'},

            # Months for date parsing (full names)
            {'key': 'month_1_full', 'en': 'january', 'ru': 'январь', 'zh': '一月'},
            {'key': 'month_2_full', 'en': 'february', 'ru': 'февраль', 'zh': '二月'},
            {'key': 'month_3_full', 'en': 'march', 'ru': 'март', 'zh': '三月'},
            {'key': 'month_4_full', 'en': 'april', 'ru': 'апрель', 'zh': '四月'},
            {'key': 'month_5_full', 'en': 'may', 'ru': 'май', 'zh': '五月'},
            {'key': 'month_6_full', 'en': 'june', 'ru': 'июнь', 'zh': '六月'},
            {'key': 'month_7_full', 'en': 'july', 'ru': 'июль', 'zh': '七月'},
            {'key': 'month_8_full', 'en': 'august', 'ru': 'август', 'zh': '八月'},
            {'key': 'month_9_full', 'en': 'september', 'ru': 'сентябрь', 'zh': '九月'},
            {'key': 'month_10_full', 'en': 'october', 'ru': 'октябрь', 'zh': '十月'},
            {'key': 'month_11_full', 'en': 'november', 'ru': 'ноябрь', 'zh': '十一月'},
            {'key': 'month_12_full', 'en': 'december', 'ru': 'декабрь', 'zh': '十二月'},
            # Months for date parsing (short names)
            {'key': 'month_1_short', 'en': 'jan', 'ru': 'янв', 'zh': '1月'},
            {'key': 'month_2_short', 'en': 'feb', 'ru': 'фев', 'zh': '2月'},
            {'key': 'month_3_short', 'en': 'mar', 'ru': 'мар', 'zh': '3月'},
            {'key': 'month_4_short', 'en': 'apr', 'ru': 'апр', 'zh': '4月'},
            {'key': 'month_5_short', 'en': 'may', 'ru': 'май', 'zh': '5月'},
            {'key': 'month_6_short', 'en': 'jun', 'ru': 'июн', 'zh': '6月'},
            {'key': 'month_7_short', 'en': 'jul', 'ru': 'июль', 'zh': '7月'},
            {'key': 'month_8_short', 'en': 'aug', 'ru': 'авг', 'zh': '8月'},
            {'key': 'month_9_short', 'en': 'sep', 'ru': 'сен', 'zh': '9月'},
            {'key': 'month_10_short', 'en': 'oct', 'ru': 'окт', 'zh': '10月'},
            {'key': 'month_11_short', 'en': 'nov', 'ru': 'ноя', 'zh': '11月'},
            {'key': 'month_12_short', 'en': 'dec', 'ru': 'дек', 'zh': '12月'},
        ]
        
        created_count = 0
        for t in translations:
            key = t['key']
            _, created_en = Translation.objects.get_or_create(
                key=key, language='en',
                defaults={'value': t['en']}
            )
            _, created_ru = Translation.objects.get_or_create(
                key=key, language='ru',
                defaults={'value': t['ru']}
            )
            _, created_zh = Translation.objects.get_or_create(
                key=key, language='zh',
                defaults={'value': t['zh']}
            )
            if created_en or created_ru or created_zh:
                created_count += 1
        
        self.stdout.write(f'  ✓ Created/updated {len(translations) * 3} translations ({created_count} new)')
    
    def create_resume_data(self):
        """Create John Doe test resume."""
        
        # Resume EN
        resume_en, created_en = Resume.objects.get_or_create(
            language='en',
            defaults={
                'firstname': 'John',
                'lastname': 'Doe',
                'resume_title': 'Senior Full-Stack Developer & Team Lead',
                'resume_description': 'Building modern web applications with React, Node.js, and Python. Leading development teams and architecting scalable solutions. Passionate about mentoring developers and driving technical excellence.',
                'about_me': 'Experienced full-stack developer with 5+ years building scalable web applications. Passionate about clean code and modern technologies.',
            }
        )
        
        # Resume RU
        resume_ru, created_ru = Resume.objects.get_or_create(
            language='ru',
            defaults={
                'firstname': 'Джон',
                'lastname': 'Доу',
                'resume_title': 'Тим Лид, Сеньор Фуллстек Разработчик',
                'resume_description': 'Создание современных веб-приложений на React, Node.js и Python. Руководство командами разработки и проектирование масштабируемых решений. Увлечен менторством разработчиков и достижением технического совершенства.',
                'about_me': 'Опытный фулстек-разработчик с опытом 5+ лет создания масштабируемых веб-приложений. Увлечен чистым кодом и современными технологиями.',
            }
        )
        
        # Resume ZH
        resume_zh, created_zh = Resume.objects.get_or_create(
            language='zh',
            defaults={
                'firstname': '张',
                'lastname': '伟',
                'resume_title': '高级全栈开发工程师和团队负责人',
                'resume_description': '使用React、Node.js和Python构建现代Web应用程序。领导开发团队并设计可扩展解决方案。热衷于指导开发人员并推动技术卓越。',
                'about_me': '经验丰富的全栈开发工程师，拥有5年以上构建可扩展Web应用程序的经验。热衷于编写干净的代码和使用现代技术。',
            }
        )
        
        if created_en or created_ru or created_zh:
            self.stdout.write('  ✓ Created resume entries')
        
        # Experience
        experiences_en = [
            {
                'company': 'Tech Corp',
                'position': 'Senior Full-Stack Developer',
                'start_date': 'Jan 2022',
                'end_date': 'Present',
                'description': 'Leading development of enterprise web applications using React and Node.js. Mentoring junior developers and establishing best practices. Architected microservices infrastructure handling 1M+ daily requests. Implemented CI/CD pipelines reducing deployment time by 60%. Collaborated with product team to define technical requirements and roadmap.',
                'language': 'en',
                'order': 10
            },
            {
                'company': 'TechStartup',
                'position': 'Full-Stack Developer',
                'start_date': 'Jun 2019',
                'end_date': 'Dec 2021',
                'description': 'Developed multiple SaaS products from scratch. Built RESTful APIs, responsive frontends, and managed AWS infrastructure. Optimized database queries improving response time by 40%. Integrated third-party payment systems and analytics tools. Led technical interviews and onboarding of new team members.',
                'language': 'en',
                'order': 20
            },
            {
                'company': 'Digital Agency',
                'position': 'Junior Developer',
                'start_date': 'Jan 2018',
                'end_date': 'May 2019',
                'description': 'Developed custom WordPress themes and plugins for clients. Implemented responsive designs using HTML, CSS, and JavaScript. Collaborated with designers to translate mockups into functional websites. Maintained and updated existing client projects with bug fixes and new features.',
                'language': 'en',
                'order': 30
            },
        ]
        
        experiences_ru = [
            {
                'company': 'Tech Corp',
                'position': 'Senior Full-Stack Developer',
                'start_date': 'Янв 2022',
                'end_date': 'Настоящее время',
                'description': 'Руководство разработкой корпоративных веб-приложений на React и Node.js. Менторинг junior разработчиков и установление лучших практик. Разработка архитектуры микросервисов, обрабатывающих 1M+ запросов в день. Внедрение CI/CD пайплайнов, сокращающих время деплоя на 60%. Сотрудничество с продуктовой командой для определения технических требований и дорожной карты.',
                'language': 'ru',
                'order': 10
            },
            {
                'company': 'TechStartup',
                'position': 'Full-Stack Developer',
                'start_date': 'Июнь 2019',
                'end_date': 'Дек 2021',
                'description': 'Разработка нескольких SaaS продуктов с нуля. Создание RESTful API, адаптивных фронтендов и управление AWS инфраструктурой. Оптимизация запросов к базе данных, улучшение времени отклика на 40%. Интеграция сторонних платежных систем и инструментов аналитики. Проведение технических интервью и онбординг новых членов команды.',
                'language': 'ru',
                'order': 20
            },
            {
                'company': 'Digital Agency',
                'position': 'Junior Developer',
                'start_date': 'Янв 2018',
                'end_date': 'Май 2019',
                'description': 'Разработка кастомных WordPress тем и плагинов для клиентов. Реализация адаптивного дизайна с использованием HTML, CSS и JavaScript. Сотрудничество с дизайнерами для преобразования макетов в функциональные веб-сайты. Поддержка и обновление существующих клиентских проектов с исправлением ошибок и добавлением новых функций.',
                'language': 'ru',
                'order': 30
            },
        ]
        
        experiences_zh = [
            {
                'company': 'Tech Corp',
                'position': '高级全栈开发工程师',
                'start_date': '2022年1月',
                'end_date': '现在',
                'description': '使用React和Node.js领导企业Web应用程序的开发。指导初级开发人员并建立最佳实践。设计了处理每日100万+请求的微服务基础设施。实施了CI/CD管道，将部署时间减少60%。与产品团队合作定义技术要求和路线图。',
                'language': 'zh',
                'order': 10
            },
            {
                'company': 'TechStartup',
                'position': '全栈开发工程师',
                'start_date': '2019年6月',
                'end_date': '2021年12月',
                'description': '从零开始开发多个SaaS产品。构建RESTful API、响应式前端并管理AWS基础设施。优化数据库查询，将响应时间提高40%。集成第三方支付系统和分析工具。领导技术面试和新团队成员入职。',
                'language': 'zh',
                'order': 20
            },
            {
                'company': 'Digital Agency',
                'position': '初级开发工程师',
                'start_date': '2018年1月',
                'end_date': '2019年5月',
                'description': '为客户开发自定义WordPress主题和插件。使用HTML、CSS和JavaScript实现响应式设计。与设计师合作将模型转换为功能性网站。维护和更新现有客户项目，修复错误并添加新功能。',
                'language': 'zh',
                'order': 30
            },
        ]
        
        created_exp = 0
        for exp_data in experiences_en + experiences_ru + experiences_zh:
            _, created = Experience.objects.get_or_create(
                company=exp_data['company'],
                language=exp_data['language'],
                defaults=exp_data
            )
            if created:
                created_exp += 1
        
        if created_exp > 0:
            self.stdout.write(f'  ✓ Created {created_exp} experience entries')
        
        # Education
        educations_en = [
            {
                'institution': 'Stanford University',
                'location': 'CA, USA',
                'degree': "Bachelor's",
                'faculty': 'School of Engineering',
                'year': '2019',
                'language': 'en',
                'order': 10
            },
            {
                'institution': 'MIT',
                'location': 'MA, USA',
                'degree': "Master's",
                'faculty': 'Computer Science',
                'year': '2021',
                'language': 'en',
                'order': 5
            },
        ]
        
        educations_ru = [
            {
                'institution': 'Стэнфордский университет',
                'location': 'Калифорния, США',
                'degree': 'Бакалавриат',
                'faculty': 'Инженерная школа',
                'year': '2019',
                'language': 'ru',
                'order': 10
            },
            {
                'institution': 'Массачусетский технологический институт',
                'location': 'Массачусетс, США',
                'degree': 'Магистратура',
                'faculty': 'Информатика',
                'year': '2021',
                'language': 'ru',
                'order': 5
            },
        ]
        
        educations_zh = [
            {
                'institution': '斯坦福大学',
                'location': '加利福尼亚州, 美国',
                'degree': '学士',
                'faculty': '工程学院',
                'year': '2019',
                'language': 'zh',
                'order': 10
            },
            {
                'institution': '麻省理工学院',
                'location': '马萨诸塞州, 美国',
                'degree': '硕士',
                'faculty': '计算机科学',
                'year': '2021',
                'language': 'zh',
                'order': 5
            },
        ]
        
        created_edu = 0
        for edu_data in educations_en + educations_ru + educations_zh:
            _, created = Education.objects.get_or_create(
                institution=edu_data['institution'],
                language=edu_data['language'],
                defaults=edu_data
            )
            if created:
                created_edu += 1
        
        if created_edu > 0:
            self.stdout.write(f'  ✓ Created {created_edu} education entries')
        
        # Certificates
        certificates_en = [
            {'name': 'AWS Certified Developer', 'year': '2023', 'language': 'en', 'order': 10},
            {'name': 'Google Cloud Professional', 'year': '2022', 'language': 'en', 'order': 20},
        ]
        
        certificates_ru = [
            {'name': 'Сертификат AWS', 'year': '2023', 'language': 'ru', 'order': 10},
            {'name': 'Сертификат Google Cloud', 'year': '2022', 'language': 'ru', 'order': 20},
        ]
        
        certificates_zh = [
            {'name': 'AWS认证开发工程师', 'year': '2023', 'language': 'zh', 'order': 10},
            {'name': 'Google Cloud专业认证', 'year': '2022', 'language': 'zh', 'order': 20},
        ]
        
        created_cert = 0
        for cert_data in certificates_en + certificates_ru + certificates_zh:
            _, created = Certificate.objects.get_or_create(
                name=cert_data['name'],
                language=cert_data['language'],
                defaults=cert_data
            )
            if created:
                created_cert += 1
        
        if created_cert > 0:
            self.stdout.write(f'  ✓ Created {created_cert} certificate entries')
        
        # Projects
        projects_en = [
            {
                'code': 'ecommerce-platform',
                'title': 'E-commerce Platform',
                'description': 'Full-featured online store with payment processing and inventory management',
                'technologies': ['React', 'Node.js', 'PostgreSQL', 'Stripe'],
                'link': '#',
                'language': 'en',
                'order': 10
            },
            {
                'code': 'task-manager',
                'title': 'Team Task Manager',
                'description': 'Collaborative project management tool with real-time updates',
                'technologies': ['Vue.js', 'Python', 'Django', 'WebSockets'],
                'link': '#',
                'language': 'en',
                'order': 20
            },
            {
                'code': 'analytics-dashboard',
                'title': 'Analytics Dashboard',
                'description': 'Real-time analytics platform with customizable widgets and data visualization',
                'technologies': ['React', 'TypeScript', 'D3.js', 'Redis'],
                'link': '#',
                'language': 'en',
                'order': 30
            },
            {
                'code': 'api-gateway',
                'title': 'API Gateway Service',
                'description': 'Microservices API gateway with rate limiting, authentication, and load balancing',
                'technologies': ['Go', 'Docker', 'Kubernetes', 'Redis'],
                'link': '#',
                'language': 'en',
                'order': 40
            },
        ]
        
        projects_ru = [
            {
                'code': 'ecommerce-platform',
                'title': 'E-commerce Платформа',
                'description': 'Интернет-магазин с полным функционалом, обработкой платежей и управлением запасами',
                'technologies': ['React', 'Node.js', 'PostgreSQL', 'Stripe'],
                'link': '#',
                'language': 'ru',
                'order': 10
            },
            {
                'code': 'task-manager',
                'title': 'Менеджер Задач',
                'description': 'Инструмент для совместного управления проектами с обновлениями в реальном времени',
                'technologies': ['Vue.js', 'Python', 'Django', 'WebSockets'],
                'link': '#',
                'language': 'ru',
                'order': 20
            },
            {
                'code': 'analytics-dashboard',
                'title': 'Дашборд Аналитики',
                'description': 'Платформа аналитики в реальном времени с настраиваемыми виджетами и визуализацией данных',
                'technologies': ['React', 'TypeScript', 'D3.js', 'Redis'],
                'link': '#',
                'language': 'ru',
                'order': 30
            },
            {
                'code': 'api-gateway',
                'title': 'API Gateway Сервис',
                'description': 'API-шлюз для микросервисов с ограничением скорости, аутентификацией и балансировкой нагрузки',
                'technologies': ['Go', 'Docker', 'Kubernetes', 'Redis'],
                'link': '#',
                'language': 'ru',
                'order': 40
            },
        ]
        
        projects_zh = [
            {
                'code': 'ecommerce-platform',
                'title': '电商平台',
                'description': '功能齐全的在线商店，具有支付处理和库存管理功能',
                'technologies': ['React', 'Node.js', 'PostgreSQL', 'Stripe'],
                'link': '#',
                'language': 'zh',
                'order': 10
            },
            {
                'code': 'task-manager',
                'title': '团队任务管理器',
                'description': '具有实时更新的协作项目管理工具',
                'technologies': ['Vue.js', 'Python', 'Django', 'WebSockets'],
                'link': '#',
                'language': 'zh',
                'order': 20
            },
            {
                'code': 'analytics-dashboard',
                'title': '分析仪表板',
                'description': '具有可自定义小部件和数据可视化的实时分析平台',
                'technologies': ['React', 'TypeScript', 'D3.js', 'Redis'],
                'link': '#',
                'language': 'zh',
                'order': 30
            },
            {
                'code': 'api-gateway',
                'title': 'API网关服务',
                'description': '具有速率限制、身份验证和负载平衡的微服务API网关',
                'technologies': ['Go', 'Docker', 'Kubernetes', 'Redis'],
                'link': '#',
                'language': 'zh',
                'order': 40
            },
        ]
        
        created_proj = 0
        for proj_data in projects_en + projects_ru + projects_zh:
            _, created = Project.objects.get_or_create(
                code=proj_data['code'],
                language=proj_data['language'],
                defaults=proj_data
            )
            if created:
                created_proj += 1
        
        if created_proj > 0:
            self.stdout.write(f'  ✓ Created {created_proj} project entries')

        # Skills
        skills_en = [
            # Frontend
            {'name': 'React', 'category_name': 'Frontend', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'en', 'order': 10},
            {'name': 'Vue.js', 'category_name': 'Frontend', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'en', 'order': 20},
            {'name': 'TypeScript', 'category_name': 'Frontend', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'en', 'order': 30},
            {'name': 'Next.js', 'category_name': 'Frontend', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'en', 'order': 40},
            {'name': 'Tailwind CSS', 'category_name': 'Frontend', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'en', 'order': 50},
            # Backend
            {'name': 'Node.js', 'category_name': 'Backend', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'en', 'order': 10},
            {'name': 'Python', 'category_name': 'Backend', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'en', 'order': 20},
            {'name': 'Django', 'category_name': 'Backend', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'en', 'order': 30},
            {'name': 'Go', 'category_name': 'Backend', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'en', 'order': 40},
            {'name': 'REST API', 'category_name': 'Backend', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'en', 'order': 50},
            # Database
            {'name': 'PostgreSQL', 'category_name': 'Database', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'en', 'order': 10},
            {'name': 'MongoDB', 'category_name': 'Database', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'en', 'order': 20},
            {'name': 'Redis', 'category_name': 'Database', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'en', 'order': 30},
            # DevOps
            {'name': 'Docker', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'en', 'order': 10},
            {'name': 'Kubernetes', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'en', 'order': 20},
            {'name': 'AWS', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'en', 'order': 30},
            {'name': 'CI/CD', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'en', 'order': 40},
        ]

        skills_ru = [
            # Frontend
            {'name': 'React', 'category_name': 'Фронтенд', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'ru', 'order': 10},
            {'name': 'Vue.js', 'category_name': 'Фронтенд', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'ru', 'order': 20},
            {'name': 'TypeScript', 'category_name': 'Фронтенд', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'ru', 'order': 30},
            {'name': 'Next.js', 'category_name': 'Фронтенд', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'ru', 'order': 40},
            {'name': 'Tailwind CSS', 'category_name': 'Фронтенд', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'ru', 'order': 50},
            # Backend
            {'name': 'Node.js', 'category_name': 'Бэкенд', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'ru', 'order': 10},
            {'name': 'Python', 'category_name': 'Бэкенд', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'ru', 'order': 20},
            {'name': 'Django', 'category_name': 'Бэкенд', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'ru', 'order': 30},
            {'name': 'Go', 'category_name': 'Бэкенд', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'ru', 'order': 40},
            {'name': 'REST API', 'category_name': 'Бэкенд', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'ru', 'order': 50},
            # Database
            {'name': 'PostgreSQL', 'category_name': 'Базы данных', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'ru', 'order': 10},
            {'name': 'MongoDB', 'category_name': 'Базы данных', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'ru', 'order': 20},
            {'name': 'Redis', 'category_name': 'Базы данных', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'ru', 'order': 30},
            # DevOps
            {'name': 'Docker', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'ru', 'order': 10},
            {'name': 'Kubernetes', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'ru', 'order': 20},
            {'name': 'AWS', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'ru', 'order': 30},
            {'name': 'CI/CD', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'ru', 'order': 40},
        ]

        skills_zh = [
            # Frontend
            {'name': 'React', 'category_name': '前端', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'zh', 'order': 10},
            {'name': 'Vue.js', 'category_name': '前端', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'zh', 'order': 20},
            {'name': 'TypeScript', 'category_name': '前端', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'zh', 'order': 30},
            {'name': 'Next.js', 'category_name': '前端', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'zh', 'order': 40},
            {'name': 'Tailwind CSS', 'category_name': '前端', 'category_name_key': 'frontend', 'category_color': 'from-blue-500 to-cyan-500', 'language': 'zh', 'order': 50},
            # Backend
            {'name': 'Node.js', 'category_name': '后端', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'zh', 'order': 10},
            {'name': 'Python', 'category_name': '后端', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'zh', 'order': 20},
            {'name': 'Django', 'category_name': '后端', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'zh', 'order': 30},
            {'name': 'Go', 'category_name': '后端', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'zh', 'order': 40},
            {'name': 'REST API', 'category_name': '后端', 'category_name_key': 'backend', 'category_color': 'from-green-500 to-emerald-500', 'language': 'zh', 'order': 50},
            # Database
            {'name': 'PostgreSQL', 'category_name': '数据库', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'zh', 'order': 10},
            {'name': 'MongoDB', 'category_name': '数据库', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'zh', 'order': 20},
            {'name': 'Redis', 'category_name': '数据库', 'category_name_key': 'database', 'category_color': 'from-purple-500 to-pink-500', 'language': 'zh', 'order': 30},
            # DevOps
            {'name': 'Docker', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'zh', 'order': 10},
            {'name': 'Kubernetes', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'zh', 'order': 20},
            {'name': 'AWS', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'zh', 'order': 30},
            {'name': 'CI/CD', 'category_name': 'DevOps', 'category_name_key': 'devops', 'category_color': 'from-orange-500 to-red-500', 'language': 'zh', 'order': 40},
        ]

        created_skill = 0
        for skill_data in skills_en + skills_ru + skills_zh:
            _, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                language=skill_data['language'],
                category_name_key=skill_data['category_name_key'],
                defaults=skill_data
            )
            if created:
                created_skill += 1

        if created_skill > 0:
            self.stdout.write(f'  ✓ Created {created_skill} skill entries')

        # Languages
        languages_en = [
            {'name': 'English', 'level': 'Native', 'proficiency': 100, 'language': 'en', 'order': 10},
            {'name': 'Russian', 'level': 'C1 Advanced', 'proficiency': 90, 'language': 'en', 'order': 20},
            {'name': 'Spanish', 'level': 'B2 Upper Intermediate', 'proficiency': 75, 'language': 'en', 'order': 30},
            {'name': 'Chinese', 'level': 'A2 Elementary', 'proficiency': 40, 'language': 'en', 'order': 40},
        ]
        
        languages_ru = [
            {'name': 'Английский', 'level': 'Родной', 'proficiency': 100, 'language': 'ru', 'order': 10},
            {'name': 'Русский', 'level': 'C1 Продвинутый', 'proficiency': 90, 'language': 'ru', 'order': 20},
            {'name': 'Испанский', 'level': 'B2 Выше среднего', 'proficiency': 75, 'language': 'ru', 'order': 30},
            {'name': 'Китайский', 'level': 'A2 Элементарный', 'proficiency': 40, 'language': 'ru', 'order': 40},
        ]
        
        languages_zh = [
            {'name': '英语', 'level': '母语', 'proficiency': 100, 'language': 'zh', 'order': 10},
            {'name': '俄语', 'level': 'C1 高级', 'proficiency': 90, 'language': 'zh', 'order': 20},
            {'name': '西班牙语', 'level': 'B2 中高级', 'proficiency': 75, 'language': 'zh', 'order': 30},
            {'name': '中文', 'level': 'A2 初级', 'proficiency': 40, 'language': 'zh', 'order': 40},
        ]
        
        created_lang = 0
        for lang_data in languages_en + languages_ru + languages_zh:
            _, created = Language.objects.get_or_create(
                name=lang_data['name'],
                language=lang_data['language'],
                defaults=lang_data
            )
            if created:
                created_lang += 1
        
        if created_lang > 0:
            self.stdout.write(f'  ✓ Created {created_lang} language entries')
        
        # Contact Info
        contacts_en = [
            {'type': 'email', 'label': 'Email', 'value': 'john.doe@example.com', 'href': 'mailto:john.doe@example.com', 'language': 'en', 'order': 10},
            {'type': 'github', 'label': 'GitHub', 'value': 'github.com/Faxziah/portfolio', 'href': 'https://github.com/Faxziah/portfolio', 'language': 'en', 'order': 20},
            {'type': 'linkedin', 'label': 'LinkedIn', 'value': 'linkedin.com', 'href': 'https://www.linkedin.com/', 'language': 'en', 'order': 30},
        ]
        
        contacts_ru = [
            {'type': 'email', 'label': 'Email', 'value': 'john.doe@example.com', 'href': 'mailto:john.doe@example.com', 'language': 'ru', 'order': 10},
            {'type': 'github', 'label': 'GitHub', 'value': 'github.com/Faxziah/portfolio', 'href': 'https://github.com/Faxziah/portfolio', 'language': 'ru', 'order': 20},
            {'type': 'linkedin', 'label': 'LinkedIn', 'value': 'linkedin.com', 'href': 'https://www.linkedin.com/', 'language': 'ru', 'order': 30},
        ]
        
        contacts_zh = [
            {'type': 'email', 'label': 'Email', 'value': 'john.doe@example.com', 'href': 'mailto:john.doe@example.com', 'language': 'zh', 'order': 10},
            {'type': 'github', 'label': 'GitHub', 'value': 'github.com/Faxziah/portfolio', 'href': 'https://github.com/Faxziah/portfolio', 'language': 'zh', 'order': 20},
            {'type': 'linkedin', 'label': 'LinkedIn', 'value': 'linkedin.com', 'href': 'https://www.linkedin.com/', 'language': 'zh', 'order': 30},
        ]
        
        created_contact = 0
        for contact_data in contacts_en + contacts_ru + contacts_zh:
            _, created = ContactInfo.objects.get_or_create(
                type=contact_data['type'],
                language=contact_data['language'],
                defaults=contact_data
            )
            if created:
                created_contact += 1

        if created_contact > 0:
            self.stdout.write(f'  ✓ Created {created_contact} contact info entries')

        # Carousel items with placeholder images
        self.create_carousel_items()

        # Reviews
        self.create_reviews()

        # Prices
        self.create_prices()

    def download_placeholder_image(self, width, height, text=''):
        """Download a placeholder image from placehold.co."""
        url = f'https://placehold.co/{width}x{height}/3b82f6/ffffff/png?text={text or "Photo"}'
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                return response.read(), 'image/png'
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            self.stdout.write(f'    Warning: Could not download placeholder image: {e}')
            return None, None

    def create_carousel_items(self):
        """Create carousel test items."""
        if Carousel.objects.exists():
            self.stdout.write('  - Carousel items already exist')
            return

        carousel_items = [
            {'description': 'Office Work', 'type': 'photo', 'order': 10, 'placeholder': '800x600', 'text': 'Office'},
            {'description': 'Team Meeting', 'type': 'photo', 'order': 20, 'placeholder': '800x600', 'text': 'Team'},
            {'description': 'Project Demo', 'type': 'photo', 'order': 30, 'placeholder': '800x600', 'text': 'Demo'},
        ]

        created_count = 0
        for item in carousel_items:
            photo_data, mime_type = self.download_placeholder_image(800, 600, item.get('text', ''))

            carousel = Carousel(
                description=item['description'],
                type=item['type'],
                order=item['order'],
            )

            if photo_data:
                carousel.photo_data = photo_data
                carousel.photo_mime_type = mime_type

            carousel.save()
            created_count += 1

        self.stdout.write(f'  ✓ Created {created_count} carousel items')

    def create_reviews(self):
        """Create review test items."""
        if Review.objects.exists():
            self.stdout.write('  - Reviews already exist')
            return

        reviews_data = [
            # English
            {'stars': 5, 'text': 'Excellent developer! Delivered the project on time with great quality.', 'author': 'Michael Brown', 'language': 'en', 'order': 10},
            {'stars': 5, 'text': 'Very professional and easy to work with. Highly recommended!', 'author': 'Sarah Johnson', 'language': 'en', 'order': 20},
            {'stars': 4, 'text': 'Good communication and technical skills. Would hire again.', 'author': 'David Wilson', 'language': 'en', 'order': 30},
            # Russian
            {'stars': 5, 'text': 'Отличный разработчик! Сдал проект вовремя с высоким качеством.', 'author': 'Михаил Браун', 'language': 'ru', 'order': 10},
            {'stars': 5, 'text': 'Очень профессиональный и приятный в работе. Рекомендую!', 'author': 'Сара Джонсон', 'language': 'ru', 'order': 20},
            {'stars': 4, 'text': 'Хорошая коммуникация и технические навыки. Буду работать снова.', 'author': 'Дэвид Уилсон', 'language': 'ru', 'order': 30},
            # Chinese
            {'stars': 5, 'text': '优秀的开发者！按时交付了高质量的项目。', 'author': '迈克尔·布朗', 'language': 'zh', 'order': 10},
            {'stars': 5, 'text': '非常专业，合作愉快。强烈推荐！', 'author': '萨拉·约翰逊', 'language': 'zh', 'order': 20},
            {'stars': 4, 'text': '良好的沟通和技术能力。愿意再次合作。', 'author': '大卫·威尔逊', 'language': 'zh', 'order': 30},
        ]

        created_count = 0
        for review_data in reviews_data:
            Review.objects.create(**review_data)
            created_count += 1

        self.stdout.write(f'  ✓ Created {created_count} review entries')

    def create_prices(self):
        """Create price/service test items."""
        if Price.objects.exists():
            self.stdout.write('  - Prices already exist')
            return

        prices_data = [
            # English
            {'name': 'Website Development', 'price': 1500.00, 'currency': 'USD', 'language': 'en', 'order': 10},
            {'name': 'Mobile App Development', 'price': 3000.00, 'currency': 'USD', 'language': 'en', 'order': 20},
            {'name': 'API Integration', 'price': 500.00, 'currency': 'USD', 'language': 'en', 'order': 30},
            {'name': 'Consulting (per hour)', 'price': 100.00, 'currency': 'USD', 'language': 'en', 'order': 40},
            # Russian
            {'name': 'Разработка веб-сайта', 'price': 150000.00, 'currency': 'RUB', 'language': 'ru', 'order': 10},
            {'name': 'Разработка мобильного приложения', 'price': 300000.00, 'currency': 'RUB', 'language': 'ru', 'order': 20},
            {'name': 'Интеграция API', 'price': 50000.00, 'currency': 'RUB', 'language': 'ru', 'order': 30},
            {'name': 'Консультация (в час)', 'price': 10000.00, 'currency': 'RUB', 'language': 'ru', 'order': 40},
            # Chinese
            {'name': '网站开发', 'price': 10000.00, 'currency': 'CNY', 'language': 'zh', 'order': 10},
            {'name': '移动应用开发', 'price': 20000.00, 'currency': 'CNY', 'language': 'zh', 'order': 20},
            {'name': 'API集成', 'price': 3500.00, 'currency': 'CNY', 'language': 'zh', 'order': 30},
            {'name': '咨询（每小时）', 'price': 700.00, 'currency': 'CNY', 'language': 'zh', 'order': 40},
        ]

        created_count = 0
        for price_data in prices_data:
            Price.objects.create(**price_data)
            created_count += 1

        self.stdout.write(f'  ✓ Created {created_count} price entries')
