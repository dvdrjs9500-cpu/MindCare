# 🧠 MindCare - Depression Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-Framework-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

> An intelligent mental health detection system that uses AI and machine learning to detect depression types and connect users with nearby psychiatric clinics.

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [System Overview](#system-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Requirements](#system-requirements)
- [How It Works](#how-it-works)
- [Modules](#modules)
- [Advantages](#advantages)
- [Limitations](#limitations)
- [Getting Started](#getting-started)
- [References](#references)

---

## 🎯 Problem Statement

Depression is a leading cause of mental illness affecting **300 million people worldwide**. Every year, **1 in 15 adults** suffer from depression, which is:

- Linked to increased risk of premature death
- A major contributor to suicidal thoughts
- Causing significant impairment in daily life

**Key Finding:** Linguistic characteristics and facial expressions can be analyzed and correlated with depression symptoms to help predict self-destructive behavior.

---

## 🔬 System Overview

MindCare is an AI-powered depression detection system that:
- ✅ Detects types of depression (Anxiety, PTSD, Bipolar, Major Depression)
- ✅ Recommends nearby psychiatric clinics
- ✅ Analyzes facial expressions through video analysis (1-minute recording)
- ✅ Conducts comprehensive quiz-based assessments
- ✅ Provides real-time location mapping to clinics

---

## ✨ Key Features

### 1. **Smart Quiz Detection**
- Evidence-based questionnaire using Naive Bayes classification
- Identifies specific depression type (Depression, Anxiety, PTSD, Bipolar)
- Instant results with severity assessment

### 2. **Facial Expression Analysis**
- Real-time video capture (1-minute recording)
- CNN-based emotion detection using custom-trained model
- Emotion scoring and depression prediction
- Processes facial micro-expressions

### 3. **Clinic Recommender**
- GPS-enabled real-time mapping
- Nearby psychiatrist clinic locator
- Direct directions and contact information

### 4. **Mental Health Information Hub**
- Educational content on mental diseases
- Self-awareness resources
- Symptom information

### 5. **Personal Wellness Journal**
- User workbook for thoughts and feelings
- Progress tracking
- Self-reflection tool

---

## 🛠️ Technology Stack

### Backend
- **Language:** Python
- **Framework:** Django
- **Database:** MySQL
- **Server:** XAMPP

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript**

### Machine Learning
- **Naive Bayes** - Quiz-based classification
- **CNN (Convolutional Neural Networks)** - Facial expression analysis
- **Custom Dataset** - Depression faces training data

### Additional Technologies
- **Real-time GPS Mapping** - Clinic locator
- **OpenCV** - Video processing
- **TensorFlow/PyTorch** - Deep learning framework

---

## 💻 System Requirements

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 7 | Windows 10+ |
| **Processor** | i3 | i5/i7 |
| **RAM** | 4 GB | 8 GB+ |
| **Storage** | 100 GB | 250 GB+ |
| **Webcam** | HD (720p) | Full HD (1080p) |

### Software Requirements

```
✓ Python 3.8+
✓ Django 3.2+
✓ MySQL 5.7+
✓ OpenCV 4.5+
✓ TensorFlow/PyTorch
✓ XAMPP Server
✓ Code Editor (VS Code / Sublime Text)
```

---

## 🔄 How It Works

### System Architecture

```
User Input
    ↓
┌───────────────────────┐
│   Authentication      │ (Login/Signup)
└───────────────────────┘
    ↓
┌───────────────────────────────┐
│  Detection Method Selection   │
├───────────────────────────────┤
│  1. Quiz-based (Naive Bayes)  │
│  2. Video-based (CNN)         │
└───────────────────────────────┘
    ↓
┌───────────────────────┐
│  AI Analysis          │
└───────────────────────┘
    ↓
┌───────────────────────────────┐
│  Depression Type Prediction   │
├───────────────────────────────┤
│  • Anxiety                    │
│  • PTSD                       │
│  • Bipolar Disorder           │
│  • Major Depression           │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│  Clinic Recommendation        │
│  (GPS Map Integration)        │
└───────────────────────────────┘
```

---

## 📦 Modules

### 1. **User Management Module**
```
├── User Registration
│   ├── Name
│   ├── Phone Number
│   ├── Email
│   ├── Password
│   └── Username
│
└── User Login
    ├── Username/Email
    └── Password
```

### 2. **Self-Assessment Module**
- **Quiz-based Depression Detection**
  - Multiple choice questions
  - Evidence-based questionnaire
  - Instant depression type classification
  - Clinic recommendations based on results

### 3. **Video Analysis Module**
- **Real-time camera access**
- **1-minute facial recording**
- **Emotion detection per frame**
- **Emotion scoring**
- **Depression severity assessment**
- **Clinic routing**

### 4. **Information Module**
- Mental health education
- Disease information
- Symptom guides
- Coping strategies

### 5. **Wellness Workbook Module**
- Digital journal
- Thought tracking
- Progress monitoring
- Personal reflections

---

## 🎯 Advantages

| Advantage | Description |
|-----------|-------------|
| **Self-Assessment** | Users can take self-tests to understand their mental health condition |
| **Easy Access** | Quick identification of depression type without complex procedures |
| **Clinic Locator** | Immediate access to nearby psychiatric clinics with GPS integration |
| **Privacy** | Users can screen themselves in private before seeking professional help |
| **Data-Driven** | AI-based predictions backed by research and machine learning |
| **Accessibility** | 24/7 availability for mental health screening |
| **Cost-Effective** | Reduces initial consultation costs for preliminary screening |

---

## ⚠️ Limitations & Disadvantages

| Limitation | Mitigation |
|-----------|-----------|
| **Emotion Expression** | Inaccurate results if emotions aren't properly expressed | Guidance videos and practice prompts |
| **Quiz Accuracy** | Incorrect predictions if quiz answers aren't truthful | Follow-up with professional assessment |
| **Audio Processing** | Audio doesn't recognize emotions in video analysis | Combine audio-visual analysis in future versions |
| **Network Dependency** | Requires internet for GPS clinic mapping | Offline map backup functionality |
| **Model Bias** | AI models trained on limited demographic data | Continuous model retraining with diverse datasets |

---

## 🚀 Getting Started

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/dvdrjs9500-cpu/MindCare.git
cd MindCare

# 2. Install dependencies
pip install -r requirements.txt

# 3. Database setup
python manage.py migrate

# 4. Run development server
python manage.py runserver

# 5. Access the application
# Open browser and navigate to: http://localhost:8000
```

### Running the Application

```bash
# Development server
python manage.py runserver

# Create superuser (for admin panel)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

---

## 🏥 Application Use Cases

1. **Individual Self-Screening** - Users screen themselves before professional consultation
2. **Workplace Mental Health** - HR departments use for employee wellness programs
3. **Educational Institutions** - Student mental health monitoring
4. **Psychiatric Clinics** - Pre-assessment tool for patients
5. **Research** - Gathering data on depression patterns and trends

---

## 📚 Project Lifecycle

This project follows the **Waterfall Model**:

```
Requirements
    ↓
Design
    ↓
Implementation (Python, Django, MySQL)
    ↓
Testing
    ↓
Deployment
    ↓
Maintenance
```

**Note:** The waterfall model follows a linear and sequential approach, developing systematically from one phase to another in a downward fashion.

---

## 📖 References

- [IEEE: Depression Detection Using Speech and Audio Features](https://ieeexplore.ieee.org/abstract/document/8389299)
- [Stevens University: Detecting Depression Using AI](https://www.stevens.edu/news/detecting-depression-using-ai)
- [Hindawi: Deep Learning for Depression Detection](https://www.hindawi.com/journals/cin/2022/4395358/)
- [ArXiv: Recent Advances in Depression Detection](https://arxiv.org/abs/2202.08210)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📞 Contact & Support

For questions, feedback, or collaboration inquiries, please reach out:
- **GitHub:** [@dvdrjs9500-cpu](https://github.com/dvdrjs9500-cpu)
- **Email:** (Add your email here)

---

## ⚠️ Disclaimer

**This system is designed for preliminary screening purposes only and should NOT be used as a substitute for professional medical diagnosis or treatment. Always consult with a licensed psychiatrist or mental health professional for proper evaluation and treatment.**

---
# File Tree: MindCare

**Generated:** 3/30/2026, 6:59:54 PM
**Root Path:** `c:\Users\KiTE\Downloads\MindCare`

```
├── 📁 app
│   ├── 📁 emotion-detect
│   │   └── 📄 page.tsx
│   ├── 📁 hooks
│   │   └── 📄 useApi.ts
│   ├── 📁 lib
│   │   └── 📄 api-client.ts
│   ├── 📁 login
│   │   └── 📄 page.tsx
│   ├── 📁 quiz
│   │   └── 📄 page.tsx
│   ├── 📁 signup
│   │   └── 📄 page.tsx
│   ├── 🎨 globals.css
│   ├── 📄 layout.tsx
│   └── 📄 page.tsx
├── 📁 backend
│   ├── 📁 assessments
│   │   ├── 📁 migrations
│   │   │   ├── 🐍 0001_initial.py
│   │   │   ├── 🐍 0002_initial.py
│   │   │   └── 🐍 __init__.py
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 admin.py
│   │   ├── 🐍 apps.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 serializers.py
│   │   ├── 🐍 tests.py
│   │   ├── 🐍 urls.py
│   │   └── 🐍 views.py
│   ├── 📁 clinics
│   │   ├── 📁 migrations
│   │   │   ├── 🐍 0001_initial.py
│   │   │   ├── 🐍 0002_initial.py
│   │   │   └── 🐍 __init__.py
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 admin.py
│   │   ├── 🐍 apps.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 serializers.py
│   │   ├── 🐍 tests.py
│   │   ├── 🐍 urls.py
│   │   └── 🐍 views.py
│   ├── 📁 config
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 asgi.py
│   │   ├── 🐍 settings.py
│   │   ├── 🐍 urls.py
│   │   └── 🐍 wsgi.py
│   ├── 📁 ml_models
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 emotion_detector.py
│   │   └── 🐍 quiz_scorer.py
│   ├── 📁 users
│   │   ├── 📁 migrations
│   │   │   ├── 🐍 0001_initial.py
│   │   │   └── 🐍 __init__.py
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 admin.py
│   │   ├── 🐍 apps.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 serializers.py
│   │   ├── 🐍 tests.py
│   │   ├── 🐍 urls.py
│   │   └── 🐍 views.py
│   ├── 📄 db.sqlite3
│   ├── 🐍 manage.py
│   ├── 📄 requirements.txt
│   └── 🐍 test_api.py
├── 📁 components
│   ├── 📁 quiz
│   │   ├── 📄 quiz-intro.tsx
│   │   ├── 📄 quiz-question.tsx
│   │   └── 📄 quiz-results.tsx
│   ├── 📁 ui
│   │   ├── 📄 accordion.tsx
│   │   ├── 📄 alert-dialog.tsx
│   │   ├── 📄 alert.tsx
│   │   ├── 📄 aspect-ratio.tsx
│   │   ├── 📄 avatar.tsx
│   │   ├── 📄 badge.tsx
│   │   ├── 📄 breadcrumb.tsx
│   │   ├── 📄 button-group.tsx
│   │   ├── 📄 button.tsx
│   │   ├── 📄 calendar.tsx
│   │   ├── 📄 card.tsx
│   │   ├── 📄 carousel.tsx
│   │   ├── 📄 chart.tsx
│   │   ├── 📄 checkbox.tsx
│   │   ├── 📄 collapsible.tsx
│   │   ├── 📄 command.tsx
│   │   ├── 📄 context-menu.tsx
│   │   ├── 📄 dialog.tsx
│   │   ├── 📄 drawer.tsx
│   │   ├── 📄 dropdown-menu.tsx
│   │   ├── 📄 empty.tsx
│   │   ├── 📄 field.tsx
│   │   ├── 📄 form.tsx
│   │   ├── 📄 hover-card.tsx
│   │   ├── 📄 input-group.tsx
│   │   ├── 📄 input-otp.tsx
│   │   ├── 📄 input.tsx
│   │   ├── 📄 item.tsx
│   │   ├── 📄 kbd.tsx
│   │   ├── 📄 label.tsx
│   │   ├── 📄 menubar.tsx
│   │   ├── 📄 navigation-menu.tsx
│   │   ├── 📄 pagination.tsx
│   │   ├── 📄 popover.tsx
│   │   ├── 📄 progress.tsx
│   │   ├── 📄 radio-group.tsx
│   │   ├── 📄 resizable.tsx
│   │   ├── 📄 scroll-area.tsx
│   │   ├── 📄 select.tsx
│   │   ├── 📄 separator.tsx
│   │   ├── 📄 sheet.tsx
│   │   ├── 📄 sidebar.tsx
│   │   ├── 📄 skeleton.tsx
│   │   ├── 📄 slider.tsx
│   │   ├── 📄 sonner.tsx
│   │   ├── 📄 spinner.tsx
│   │   ├── 📄 switch.tsx
│   │   ├── 📄 table.tsx
│   │   ├── 📄 tabs.tsx
│   │   ├── 📄 textarea.tsx
│   │   ├── 📄 toast.tsx
│   │   ├── 📄 toaster.tsx
│   │   ├── 📄 toggle-group.tsx
│   │   ├── 📄 toggle.tsx
│   │   ├── 📄 tooltip.tsx
│   │   ├── 📄 use-mobile.tsx
│   │   └── 📄 use-toast.ts
│   ├── 📄 cta-section.tsx
│   ├── 📄 features-section.tsx
│   ├── 📄 footer.tsx
│   ├── 📄 header.tsx
│   ├── 📄 hero-section.tsx
│   ├── 📄 how-it-works-section.tsx
│   ├── 📄 stats-section.tsx
│   └── 📄 theme-provider.tsx
├── 📁 hooks
│   ├── 📄 use-mobile.ts
│   └── 📄 use-toast.ts
├── 📁 lib
│   └── 📄 utils.ts
├── 📁 public
│   ├── 🖼️ apple-icon.png
│   ├── 🖼️ icon-dark-32x32.png
│   ├── 🖼️ icon-light-32x32.png
│   ├── 🖼️ icon.svg
│   ├── 🖼️ placeholder-logo.png
│   ├── 🖼️ placeholder-logo.svg
│   ├── 🖼️ placeholder-user.jpg
│   ├── 🖼️ placeholder.jpg
│   └── 🖼️ placeholder.svg
├── 📁 styles
│   └── 🎨 globals.css
├── ⚙️ .gitignore
├── 📝 BACKEND_SETUP.md
├── 📄 Dockerfile.backend
├── 📄 Dockerfile.frontend
├── 📝 README.md
├── ⚙️ components.json
├── ⚙️ docker-compose.yml
├── 📄 next-env.d.ts
├── 📄 next.config.mjs
├── ⚙️ package-lock.json
├── ⚙️ package.json
├── 📄 postcss.config.mjs
└── ⚙️ tsconfig.json
```
**Built with ❤️ for mental health awareness**
