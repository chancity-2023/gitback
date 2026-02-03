# Tournament Registration Backend - Quick Reference

## 🚀 Quick Start Commands

### Local Development
```powershell
# Navigate to backend
cd "c:\Users\Rakshit\Desktop\Git projects\chancity.github.io\backend"

# Activate virtual environment
.\venv\Scripts\activate

# Start server
uvicorn app.main:app --reload --port 8000
```

### Testing
```powershell
# Health check
curl http://localhost:8000/health

# View API docs
# Open: http://localhost:8000/docs
```

---

## 📝 Appwrite Credentials Format

Save these from Appwrite Console:

```
Project ID:    507f1f77bcf86cd799439011
Database ID:   65d8f1234567890abcdef123
Collection ID: 65d8f9876543210fedcba987
API Key:       standard_xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🔧 Environment Variables (.env)

```env
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=your_database_id
APPWRITE_COLLECTION_ID=your_collection_id
CORS_ORIGINS=https://rahulj-crypto.github.io
ENVIRONMENT=development
DEBUG=true
```

---

## 📊 Collection Schema (14 Attributes)

| # | Attribute | Type | Size | Required | Default |
|---|-----------|------|------|----------|---------|
| 1 | registration_id | String | 36 | ✓ | - |
| 2 | team_name | String | 200 | ✓ | - |
| 3 | category | String | 20 | ✓ | - |
| 4 | team_size | Integer | - | ✓ | - |
| 5 | contact_name | String | 100 | ✓ | - |
| 6 | designation | String | 50 | ✓ | - |
| 7 | email | Email | 255 | ✓ | - |
| 8 | phone | String | 20 | ✓ | - |
| 9 | alt_phone | String | 20 | ✗ | - |
| 10 | players | String | 2000 | ✓ | - |
| 11 | terms_accepted | Boolean | - | ✓ | - |
| 12 | newsletter_subscribed | Boolean | - | ✓ | false |
| 13 | status | String | 50 | ✓ | pending |
| 14 | created_at | String | 50 | ✓ | - |

---

## 📍 Important URLs

### Development
- Backend: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:8080/registration.html`

### Production
- Frontend: `https://rahulj-crypto.github.io/chancity.github.io/registration.html`
- Backend: `https://your-app-name.onrender.com` (replace after deployment)
- Appwrite: `https://cloud.appwrite.io`

---

## 🎯 API Endpoints

### POST /api/v1/registrations
Create new registration

**Request**:
```json
{
  "team_name": "Test Warriors",
  "category": "senior",
  "team_size": 10,
  "contact_name": "John Doe",
  "designation": "coach",
  "email": "test@example.com",
  "phone": "+919876543210",
  "alt_phone": "",
  "players": "1. Player One - 25 - Raider",
  "terms_accepted": true,
  "newsletter_subscribed": false
}
```

**Response** (201):
```json
{
  "registration_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2026-01-31T22:00:00Z",
  "message": "Registration submitted successfully"
}
```

### GET /health
Health check
```json
{
  "status": "healthy",
  "timestamp": "2026-01-31T22:00:00Z",
  "version": "1.0.0"
}
```

---

## 🔍 Common Issues

| Issue | Solution |
|-------|----------|
| Module not found | Activate virtual environment |
| Appwrite error | Check credentials in `.env` |
| CORS error | Update `CORS_ORIGINS`, restart server |
| Phone validation fails | Use format `+919876543210` or `9876543210` |

---

## ✅ Deployment Checklist

- [ ] Appwrite project created
- [ ] Database & collection configured
- [ ] All 14 attributes added
- [ ] 4 indexes created
- [ ] Permissions set correctly
- [ ] API key generated
- [ ] Local backend running
- [ ] Frontend tested locally
- [ ] Code committed to GitHub
- [ ] Render web service created
- [ ] Environment variables added
- [ ] Production tested
- [ ] Domain updated in API client

---

For full documentation, see: `backend/README.md`  
For step-by-step walkthrough, see: `walkthrough.md`
