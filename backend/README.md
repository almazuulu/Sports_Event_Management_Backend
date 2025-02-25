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
- **API Documentation:** Swagger/ReDoc via drf-yasg
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
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database configuration
DB_NAME=sports_event_db
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=1
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

6. **Set up the app URLs**

Ensure all application URL files are properly configured with at least an empty urlpatterns list:

- users/urls.py
- users/auth_urls.py
- events/urls.py
- teams/urls.py
- games/urls.py
- scores/urls.py
- leaderboards/urls.py

7. **Apply migrations**

```bash
python manage.py migrate
```

8. **Create a superuser (admin)**

```bash
python manage.py createsuperuser
```

9. **Run the development server**

```bash
python manage.py runserver
```

The server will start at http://127.0.0.1:8000/

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

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

## Deployment Considerations

For production deployment:
- Set DEBUG=False in .env
- Configure proper ALLOWED_HOSTS
- Use a production-grade web server (Gunicorn, uWSGI)
- Set up proper database credentials
- Configure proper security settings

