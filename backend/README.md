# Sports Event Management System - Backend

## Project Overview

The Sports Event Management System is a comprehensive web application designed to manage multi-sport events and tournaments. The system enables administrators to organize multiple sports tournaments, manage team registrations, schedule games, track scores, and determine the best team based on cumulative performance.

The backend is built with Django and Django REST Framework, providing a robust API for frontend clients and mobile applications.

## Key Features

- **Multi-Sport Events:** Support for various sports (Football, Basketball, Cricket, etc.) played concurrently
- **Role-Based Access:** Separate interfaces for Admins, Team Captains, Scorekeepers, and Public Users
- **Team Management:** Registration, player management, and assignment
- **Game Scheduling:** Creation and management of game schedules for multiple concurrent events
- **Real-Time Scoring:** Live score updates and tracking
- **Leaderboards:** Automatic calculation of team standings and rankings

## Project Structure

```
backend/
├── apps/                      # Django applications
│   ├── events/                # Sport events management
│   ├── games/                 # Game scheduling and management
│   ├── leaderboards/          # Rankings and standings
│   ├── scores/                # Score tracking and management
│   ├── teams/                 # Team and player management
│   └── users/                 # User authentication and authorization
├── config/                    # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL routing
│   ├── asgi.py                # ASGI configuration
│   └── wsgi.py                # WSGI configuration
├── media/                     # User-uploaded files
├── static/                    # Static files (CSS, JS, images)
├── templates/                 # HTML templates
├── utils/                     # Utility functions and classes
├── venv/                      # Virtual environment
├── .env                       # Environment variables
├── .env.dist                  # Environment variables template
├── manage.py                  # Django management script
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## Technical Specifications

- **Backend Framework:** Django 5.1.6 with Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (JSON Web Tokens) via SimpleJWT
- **API Documentation:** Swagger/ReDoc via drf-spectacular
- **Development Tools:** Django Debug Toolbar
- **Static Files:** Served via WhiteNoise
- **CORS Support:** django-cors-headers for cross-origin requests
- **Environment Management:** python-dotenv for environment variables

## Installation and Setup

### Prerequisites

- Python 3.9+ (recommended)
- PostgreSQL
- Git

### Setup Steps

1. **Clone the repository**

```bash
git clone <repository_url>
cd Sports_Event_Management/backend
```

2. **Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file based on the `.env.dist` template:

```bash
cp .env.dist .env
```

Edit the `.env` file to set the following variables:

```
# Django settings
SECRET_KEY=your_secure_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=sports_event_db
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Localization
LANGUAGE_CODE=en-us
TIME_ZONE=UTC

# REST Framework
REST_PAGE_SIZE=20

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
JWT_ROTATE_REFRESH_TOKENS=True
JWT_BLACKLIST_AFTER_ROTATION=True

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **Create a PostgreSQL database**

```bash
# Log into PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE sports_event_db;
CREATE USER your_database_user WITH PASSWORD 'your_database_password';
GRANT ALL PRIVILEGES ON DATABASE sports_event_db TO your_database_user;
\q
```

Alternatively, you can use these simplified commands:

```bash
# Connect to PostgreSQL
psql -U postgres

# In PostgreSQL prompt
CREATE DATABASE sports_event_db;
\q
```

6. **Apply migrations**

Since migration files are already included, you just need to apply them:

```bash
python manage.py migrate
```

7. **Create a superuser (admin)**

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

8. **Collect static files**

```bash
python manage.py collectstatic
```

9. **Run the development server**

```bash
python manage.py runserver
```

The server will start at http://127.0.0.1:8000/

## API Documentation

Once the server is running, you can access:
- API Root: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/
- Swagger UI: http://127.0.0.1:8000/api/swagger/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- API Schema: http://127.0.0.1:8000/api/schema/

## API Endpoints

The following API endpoints are available:

- Authentication: `/api/auth/`, `/api/token/`
- Users: `/api/users/`
- Events: `/api/events/`
- Teams: `/api/teams/`
- Games: `/api/games/`
- Scores: `/api/scores/`
- Leaderboards: `/api/leaderboards/`

## Authentication

The API uses JWT authentication:
- Obtain token: POST to `/api/token/`
- Refresh token: POST to `/api/token/refresh/`
- Verify token: POST to `/api/token/verify/`

## Development

### Creating a new app

```bash
cd apps
python ../manage.py startapp new_app_name
```

Remember to add the new app to INSTALLED_APPS in settings.py.

### Running tests

```bash
python manage.py test
```

## Troubleshooting

If you encounter any issues:

1. Check that your database credentials are correct in the `.env` file
2. Ensure PostgreSQL service is running
3. Verify that all dependencies were installed correctly
4. Check the Django error logs for specific error messages

For database connection issues, you may need to adjust the PostgreSQL authentication settings in `pg_hba.conf` or try using `localhost` instead of `127.0.0.1` as the DB_HOST.

## Deployment Considerations

For production deployment:
- Set DEBUG=False in .env
- Configure proper ALLOWED_HOSTS
- Use a production-grade web server (Gunicorn, uWSGI)
- Set up proper database credentials
- Configure proper security settings