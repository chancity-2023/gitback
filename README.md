# Tournament Registration Backend

Production-ready Python FastAPI backend for the Chancity Sports Club tournament registration system with Appwrite Cloud database integration.

## 🚀 Features

- ✅ FastAPI REST API with automatic OpenAPI documentation
- ✅ Appwrite Cloud database integration
- ✅ Comprehensive input validation with Pydantic
- ✅ Indian phone number validation
- ✅ XSS prevention and input sanitization
- ✅ CORS configuration for GitHub Pages
- ✅ Structured logging with correlation
- ✅ Comprehensive error handling
- ✅ Health check endpoint for monitoring
- ✅ Production-ready for Render deployment

## 📋 Prerequisites

- Python 3.10 or higher
- Appwrite Cloud account
- Git

## 🔧 Appwrite Setup Guide

### Step 1: Create Appwrite Project

1. Go to [Appwrite Cloud Console](https://cloud.appwrite.io)
2. Sign in or create a new account
3. Click **"Create Project"**
4. Enter project name: `Chancity Tournament Registration`
5. Click **"Create"**
6. **Copy your Project ID** - you'll need this later

### Step 2: Create Database

1. In your project dashboard, click **"Databases"** in the left sidebar
2. Click **"Create Database"**
3. Enter database name: `tournament_db`
4. Click **"Create"**
5. **Copy the Database ID** - you'll need this later

### Step 3: Create Collection

1. Click **"Create Collection"** inside your database
2. Enter collection name: `registrations`
3. Click **"Create"**
4. **Copy the Collection ID** - you'll need this later

### Step 4: Configure Collection Attributes

Click **"Attributes"** tab and add the following attributes:

| Attribute | Type | Size | Required | Array | Default |
|-----------|------|------|----------|-------|---------|
| `registration_id` | String | 36 | ✓ | ✗ | - |
| `team_name` | String | 200 | ✓ | ✗ | - |
| `category` | String | 20 | ✓ | ✗ | - |
| `team_size` | Integer | - | ✓ | ✗ | - |
| `contact_name` | String | 100 | ✓ | ✗ | - |
| `designation` | String | 50 | ✓ | ✗ | - |
| `email` | Email | 255 | ✓ | ✗ | - |
| `phone` | String | 20 | ✓ | ✗ | - |
| `alt_phone` | String | 20 | ✗ | ✗ | - |
| `players` | String | 2000 | ✓ | ✗ | - |
| `terms_accepted` | Boolean | - | ✓ | ✗ | - |
| `newsletter_subscribed` | Boolean | - | ✓ | ✗ | false |
| `status` | String | 50 | ✓ | ✗ | pending |
| `created_at` | String | 50 | ✓ | ✗ | - |

**Important**: Add each attribute one by one using the **"Create attribute"** button.

### Step 5: Create Indexes

Click **"Indexes"** tab and create these indexes:

1. **Index 1**: `registration_id_index`
   - Type: Unique
   - Attribute: `registration_id`

2. **Index 2**: `email_index`
   - Type: Key
   - Attribute: `email`

3. **Index 3**: `created_at_index`
   - Type: Key
   - Attribute: `created_at`

4. **Index 4**: `status_index`
   - Type: Key
   - Attribute: `status`

### Step 6: Configure Permissions

1. Click **"Settings"** tab
2. Under **"Permissions"**, configure:
   - **Create**: Select **"Any"** (allows public registration submissions)
   - **Read**: Select **"Users"** (only authenticated users can view)
   - **Update**: Select **"Users"** (only authenticated users can update)
   - **Delete**: Select **"Users"** (only authenticated users can delete)

### Step 7: Generate API Key

1. Go to **"Settings"** in the left sidebar (project settings)
2. Click **"API Keys"** tab
3. Click **"Create API Key"**
4. Enter name: `Backend Server Key`
5. Select scopes:
   - ✓ `databases.read`
   - ✓ `databases.write`
6. Click **"Create"**
7. **Copy the API Key** - you'll need this IMMEDIATELY (it won't be shown again!)

### ✅ Appwrite Setup Complete!

You should now have:
- ✓ Project ID
- ✓ Database ID
- ✓ Collection ID
- ✓ API Key

---

## 💻 Local Development Setup

### 1. Clone and Navigate to Backend

```bash
cd c:\Users\Rakshit\Desktop\Git projects\chancity.github.io\backend
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
# source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
copy .env.example .env
```

Edit `.env` and add your Appwrite credentials:

```env
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id_here
APPWRITE_API_KEY=your_api_key_here
APPWRITE_DATABASE_ID=your_database_id_here
APPWRITE_COLLECTION_ID=your_collection_id_here

# CORS Configuration
CORS_ORIGINS=https://rahulj-crypto.github.io,http://localhost:8080

# Application Configuration
ENVIRONMENT=development
DEBUG=true
```

### 5. Run Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

### 6. Test the API

Open a new terminal and test:

```bash
# Health check
curl http://localhost:8000/health

# Test registration (replace with your data)
curl -X POST http://localhost:8000/api/v1/registrations \
  -H "Content-Type: application/json" \
  -d "{\"team_name\":\"Test Team\",\"category\":\"senior\",\"team_size\":10,\"contact_name\":\"John Doe\",\"designation\":\"coach\",\"email\":\"test@example.com\",\"phone\":\"+919876543210\",\"players\":\"1. Player One - 25 - Raider\",\"terms_accepted\":true,\"newsletter_subscribed\":false}"
```

### 7. Test with Frontend

1. Update `js/api-client.js` to use `http://localhost:8000`
2. Serve frontend with Live Server or:
   ```bash
   python -m http.server 8080
   ```
3. Open http://localhost:8080/registration.html
4. Fill and submit the form
5. Check Appwrite Console for the new registration

---

## 🚢 Render Deployment Guide

### Step 1: Prepare for Deployment

1. Ensure all files are committed to GitHub
2. Push to your repository:
   ```bash
   git add .
   git commit -m "Add Python backend with Appwrite integration"
   git push origin main
   ```

### Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the `chancity.github.io` repository
5. Configure the service:

   **Basic Settings:**
   - Name: `chancity-registration-api`
   - Region: Choose closest to your users
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`

   **Build Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

   **Instance Type:**
   - Free (or Starter for better performance)

### Step 3: Configure Environment Variables

In Render dashboard, add these environment variables:

```
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id_here
APPWRITE_API_KEY=your_api_key_here
APPWRITE_DATABASE_ID=your_database_id_here
APPWRITE_COLLECTION_ID=your_collection_id_here
CORS_ORIGINS=https://rahulj-crypto.github.io
ENVIRONMENT=production
DEBUG=false
```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment to complete (5-10 minutes)
3. Copy your Render URL: `https://chancity-registration-api.onrender.com`

### Step 5: Update Frontend

Update `js/api-client.js` with your Render URL:

```javascript
const API_CONFIG = {
    baseURL: 'https://chancity-registration-api.onrender.com',
    // ...
};
```

Commit and push changes:

```bash
git add js/api-client.js
git commit -m "Update API URL to Render deployment"
git push origin main
```

### Step 6: Test Production Deployment

1. Visit your GitHub Pages site
2. Go to the registration page
3. Submit a test registration
4. Verify in Appwrite Console that data was saved

---

## 📚 API Documentation

### Base URL

**Development**: `http://localhost:8000`  
**Production**: `https://your-app-name.onrender.com`

### Endpoints

#### Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-31T22:00:00Z",
  "version": "1.0.0",
  "environment": "production"
}
```

#### Create Registration
```http
POST /api/v1/registrations
```

**Request Body**:
```json
{
  "team_name": "Chancity Warriors",
  "category": "senior",
  "team_size": 10,
  "contact_name": "John Doe",
  "designation": "coach",
  "email": "john@example.com",
  "phone": "+919876543210",
  "alt_phone": "+919123456789",
  "players": "1. Player One - 25 - Raider\n2. Player Two - 24 - Defender",
  "terms_accepted": true,
  "newsletter_subscribed": false
}
```

**Success Response** (201 Created):
```json
{
  "registration_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2026-01-31T22:00:00Z",
  "message": "Registration submitted successfully"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "ValidationError",
  "detail": "Invalid phone number format",
  "timestamp": "2026-01-31T22:00:00Z"
}
```

#### Get Registration
```http
GET /api/v1/registrations/{registration_id}
```

**Success Response** (200 OK):
```json
{
  "registration_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2026-01-31T22:00:00Z",
  "message": "Registration found"
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "NotFound",
  "detail": "Registration 550e8400-e29b-41d4-a716-446655440000 not found",
  "timestamp": "2026-01-31T22:00:00Z"
}
```

---

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_registration.py -v
```

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   └── registration.py    # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── appwrite_service.py # Appwrite integration
│   ├── routes/
│   │   ├── __init__.py
│   │   └── registration.py    # API endpoints
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── conftest.py
├── .env.example                # Environment template
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

---

## 🔒 Security

- ✅ **Input Validation**: All inputs validated with Pydantic
- ✅ **XSS Prevention**: Text fields sanitized
- ✅ **CORS**: Strict CORS policy
- ✅ **API Keys**: Server-side only, never exposed
- ✅ **HTTPS**: Enforced in production
- ✅ **Error Messages**: Generic messages to prevent information leakage

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution**: Make sure you're in the `backend` directory and virtual environment is activated.

### Issue: "Appwrite Exception: Project not found"

**Solution**: Verify your `APPWRITE_PROJECT_ID` in `.env` file matches the ID in Appwrite Console.

### Issue: "CORS Error in Browser"

**Solution**: 
1. Check `CORS_ORIGINS` in `.env` includes your frontend domain
2. Restart the server after changing `.env`
3. Clear browser cache

### Issue: "Phone number validation fails"

**Solution**: Ensure phone numbers are in format `+919876543210` or `9876543210` (starting with 6-9).

---

## 📞 Support

For issues or questions:
- Check Appwrite Console logs
- Check Render deployment logs
- Review browser console for frontend errors
- Verify all environment variables are set correctly

---

## 📝 License

© 2026 Chancity Sports Club. All Rights Reserved.
