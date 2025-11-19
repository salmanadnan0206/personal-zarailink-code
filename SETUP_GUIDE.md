# Quick Setup Guide

## 🚀 Getting Started

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

   **IMPORTANT:** If you see "ModuleNotFoundError: No module named 'django'", make sure you activated the virtual environment (step 2)!

5. **Create a superuser (optional but recommended):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Django server:**
   ```bash
   python manage.py runserver
   ```

   You should see:
   ```
   Starting development server at http://127.0.0.1:8000/
   ```

### Frontend Setup

1. **Navigate to frontend directory (in a new terminal):**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```

   The app will open at `http://localhost:3000`

## ✅ Testing the Authentication

1. Make sure **BOTH** servers are running:
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

2. Go to `http://localhost:3000/signup`
3. Create a new account
4. You should be redirected to the email verification page
5. Then try logging in at `http://localhost:3000/login`
6. After successful login, you'll be redirected to the dashboard

## 🔧 Troubleshooting

### "Cannot connect to server" error

**Symptom:** You see "Cannot connect to server. Make sure the backend is running on http://localhost:8000"

**Solution:**
- Check if Django server is running on port 8000
- Look for the terminal running `python manage.py runserver`
- If not running, start it with the command above

### CORS errors in browser console

**Symptom:** You see errors like "Access to XMLHttpRequest at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy"

**Solution:**
- This has been fixed! CORS is now properly configured in `backend/zarailink/settings.py`
- Make sure you're using the latest code
- Restart the Django server after pulling the latest changes

### "Invalid email or password" error

**Symptom:** Login fails even with correct credentials

**Possible causes:**
1. The user doesn't exist in the database
2. Password is incorrect
3. You're trying to login with an account that hasn't been created yet

**Solution:**
- Create an account first via the signup page
- Or create a user via Django admin or `createsuperuser`
- Check the Django console for error messages

### Signup validation errors

**Symptom:** Form shows validation errors

**Common issues:**
- Password must be at least 8 characters
- Passwords must match
- Email must be valid format
- All fields are required

## 🗄️ Database

The project is configured for PostgreSQL but uses SQLite by default for development.

### Current database: `db.sqlite3`

To view/manage the database:
```bash
cd backend
python manage.py dbshell
```

Or use Django admin:
1. Go to `http://localhost:8000/admin`
2. Login with superuser credentials

## 📝 API Endpoints

Base URL: `http://localhost:8000`

### Authentication Endpoints:
- `POST /accounts/api/signup/` - Create new account
- `POST /accounts/api/login/` - Login
- `POST /accounts/api/logout/` - Logout
- `POST /accounts/api/forgot-password/` - Request password reset

### Testing with cURL:

**Signup:**
```bash
curl -X POST http://localhost:8000/accounts/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpass123",
    "country": "Pakistan"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/accounts/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

## 🔍 Debugging

### Check Django logs:
The terminal running `python manage.py runserver` shows all requests and errors

### Check browser console:
Open Developer Tools (F12) → Console tab to see frontend errors

### Check Network tab:
Open Developer Tools (F12) → Network tab to see API requests/responses

## 📦 Dependencies

### Backend (Python):
- Django 4.2.7
- djangorestframework 3.14.0
- django-cors-headers 4.3.1 ✅ Now configured!
- djangorestframework-simplejwt 5.3.0

### Frontend (JavaScript):
- React 19.2.0
- react-router-dom 7.9.6
- axios (for API calls)
- Tailwind CSS

## 🎯 Next Steps

Once everything is working:

1. Review the `SECURITY_ANALYSIS.md` file
2. Fix the critical security issues before production
3. Implement the remaining features (suppliers, buyers, etc.)
4. Set up proper environment variables
5. Configure production database
