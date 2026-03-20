# 🚀 MindCare Backend Setup Guide

## Phase 1: Django REST API Backend ✅ COMPLETE

### What's Been Implemented

✅ **Django Project Structure**
- Project config with REST Framework & CORS
- 3 Main apps: Users, Assessments, Clinics
- SQLite database (ready for MySQL upgrade)

✅ **Database Models (50+ fields)**

**Users App:**
- Custom User model (extending Django's AbstractUser)
- User Health Profile (depression tracking, risk assessment)
- User Journal & Journal Entries (wellness tracking)

**Assessments App:**
- Quiz templates with questions & options
- Quiz Results with confidence scores
- Video Analysis with emotion detection
- Frame-by-frame emotion tracking
- Assessment History tracking

**Clinics App:**
- Clinic information & location data
- Clinic Recommendations based on AI assessment

✅ **Database Migrations** - All models registered and migrated

---

## 🔧 Running the Backend

### 1. Install Dependencies
```bash
cd backend
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

### 2. Run Migrations (Already Done)
```bash
.\venv\Scripts\python manage.py migrate
```

### 3. Start Development Server
```bash
.\venv\Scripts\python manage.py runserver
```
Server will run on: `http://localhost:8000`

### 4. Create Admin User (Optional)
```bash
.\venv\Scripts\python manage.py createsuperuser
```
Access admin panel at: `http://localhost:8000/admin`

---

## 📁 Project Structure

```
backend/
├── config/
│   ├── settings.py          # Django settings (REST, CORS, DB config)
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── users/
│   ├── models.py            # User, HealthProfile, Journal models
│   ├── views.py             # API views (to be created)
│   ├── serializers.py       # DRF serializers (to be created)
│   └── admin.py
├── assessments/
│   ├── models.py            # Quiz, VideoAnalysis, EmotionFrame models
│   ├── views.py             # Assessment endpoints (to be created)
│   └── serializers.py       # DRF serializers (to be created)
├── clinics/
│   ├── models.py            # Clinic & Recommendation models
│   ├── views.py             # Clinic endpoints (to be created)
│   └── serializers.py       # DRF serializers (to be created)
├── manage.py
├── requirements.txt         # Python dependencies
└── db.sqlite3              # SQLite database
```

---

## 📊 Database Models Overview

### Users App Models

#### CustomUser
- Extends Django's AbstractUser
- Health information: is_diagnosed, current_treatment
- Privacy: is_public_profile
- Profile: phone, date_of_birth, gender, bio, profile_picture

#### UserHealthProfile  
- Depression type: NONE, MILD, MODERATE, SEVERE, ANXIETY, PTSD, BIPOLAR
- Severity score (0-100)
- Risk level: LOW, MEDIUM, HIGH
- Family history, medications tracking

#### UserJournal & JournalEntry
- Personal wellness journal
- Mood tracking (Happy, Sad, Anxious, Calm, Angry, Neutral)
- Mood scores (1-10)

### Assessments App Models

#### Quiz & QuizQuestion & QuizOption
- Quiz templates (PHQ-9, GAD, etc.)
- Multiple question types: Radio, Checkbox, Scale, Text
- Scoring system for each option

#### QuizResult
- Stores completed quiz results
- Score, percentage, diagnosis
- Confidence score from Naive Bayes model
- Time taken, device type tracking
- Category-wise scoring breakdown

#### VideoAnalysis & EmotionFrame
- Video file storage & processing
- Overall emotion detection
- Frame-by-frame emotion tracking
- Depression risk scoring (0-100)
- Face detection metrics: eyes, smile count, blink rate
- Behavioral indicators: eye contact, smile count, speaking rate

#### AssessmentHistory
- Unified tracking of all assessments (quiz + video)
- Overall diagnosis & risk level

### Clinics App Models

#### Clinic
- Clinic information: name, address, contact
- Location coordinates: latitude, longitude
- Specializations & ratings
- Verification status
- Services: insurance, telemedicine

#### ClinicRecommendation
- AI-generated recommendations per user
- Match percentage & distance
- Tracking if viewed/contacted

---

## 🔑 Configuration Details

### REST Framework Settings
- Authentication: Token-based
- Pagination: 10 items per page
- Filters: Search & Ordering
- CORS: Enabled for localhost:3000 (Next.js frontend)

### Database Options
- **Development**: SQLite (already configured)
- **Production**: MySQL (uncommented in settings.py)

### Custom Auth
- Custom User model replaces default User
- Health profile linked to each user

---

## 🎯 Phase 2: REST API Endpoints (Next Steps)

The following API endpoints need to be created:

### User Endpoints
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile
- `GET /api/users/health-profile/` - Get health info

### Assessment Endpoints
- `GET /api/assessments/quizzes/` - List available quizzes
- `POST /api/assessments/quiz-results/` - Submit quiz
- `GET /api/assessments/quiz-results/` - Get quiz history
- `POST /api/assessments/video-upload/` - Upload video
- `GET /api/assessments/video-results/` - Get video analysis results

### Clinic Endpoints
- `GET /api/clinics/` - List clinics
- `GET /api/clinics/{id}/` - Clinic details
- `GET /api/clinics/nearest/` - Nearest clinics (geo-location)
- `GET /api/recommendations/` - Get clinic recommendations

### Journal Endpoints
- `GET /api/journal/entries/` - Get journal entries
- `POST /api/journal/entries/` - Create journal entry
- `PUT /api/journal/entries/{id}/` - Update entry
- `DELETE /api/journal/entries/{id}/` - Delete entry

---

## 📝 Serializers to Implement

Each app needs serializers for DRF:
- `UserSerializer`
- `UserHealthProfileSerializer`
- `QuizSerializer`
- `QuizResultSerializer`
- `VideoAnalysisSerializer`
- `ClinicSerializer`
- `ClinicRecommendationSerializer`

---

## 🔌 Frontend Integration

The Next.js frontend (`http://localhost:3000`) is configured to communicate with this backend:

```javascript
// API Base URL
const API_URL = 'http://localhost:8000/api/'

// Examples for frontend
fetch(API_URL + 'users/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, email, password })
})
```

---

## 🚨 Common Issues & Fixes

### Port Already in Use
```bash
# Use different port
.\venv\Scripts\python manage.py runserver 8001
```

### Database Locked
```bash
# Reset database
del db.sqlite3
.\venv\Scripts\python manage.py migrate
```

### CORS Issues
- Update `CORS_ALLOWED_ORIGINS` in settings.py
- Add `Access-Control-Allow-*` headers

---

## ✅ Checklist for Phase 2

- [ ] Create serializers for all models
- [ ] Implement REST API views
- [ ] Set up JWT/Token authentication
- [ ] Create URL routing
- [ ] Test API endpoints with Postman
- [ ] Document API with Swagger/drf-spectacular
- [ ] Integrate with Next.js frontend
- [ ] Connect ML models (Naive Bayes, CNN)
- [ ] Deploy to production

---

## 📚 Resources

- [Django Official Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Jose Authentication](https://python-jose.readthedocs.io/)

---

**Next: Phase 2 - REST API Endpoints & Frontend Integration** 🚀
