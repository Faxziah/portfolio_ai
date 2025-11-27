# AI Portfolio

AI-powered portfolio website with intelligent chat assistant powered by Google Gemini 2.0.

## ✨ Features

- 🤖 **AI Chat Assistant** - Ask questions about your experience, skills, and projects
- 🌐 **Multi-language Support** - English and Russian (easily extensible)
- 🎨 **3 Color Themes** - Blue, Green, Purple
- 🌓 **Dark/Light Mode**
- 📱 **Responsive Design**
- 🐳 **Docker Ready**

## 🚀 Quick Start (5 minutes)

### Prerequisites

- Docker and Docker Compose installed

### Step 1: Clone and Setup

```bash
git clone https://github.com/yourusername/portfolio_ai.git
cd portfolio_ai
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### Step 2: Start the Project

```bash
docker compose up -d --build
```

### Step 3: Open Your Portfolio

**🌐 Portfolio:** http://localhost:8002

**⚙️ Admin Panel:** http://localhost:8003/admin
- Username: `admin`
- Password: `admin`
- Change password: http://localhost:8003/admin/auth/user/1/password/

### Step 4: Add Gemini API Key (Optional)

To enable AI chat:
1. Get a free API key: https://aistudio.google.com/app/apikey
2. Go to **Admin Panel** → **Settings** → `gemini_api_key`
3. Paste your API key

## 🌐 Adding a New Language

1. Go to **Admin Panel** → **Settings** → `site_languages`
2. Add your language to the JSON array:
```json
[
  {"code": "en", "name": "English", "flag": "🇺🇸"},
  {"code": "ru", "name": "Русский", "flag": "🇷🇺"},
  {"code": "es", "name": "Español", "flag": "🇪🇸"}
]
```
3. Save — all translations and content will be **automatically duplicated** from English (or another existing language)
4. Go to each section and correct translations