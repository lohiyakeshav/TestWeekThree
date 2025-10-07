# Mini Order Management Service

A production-ready FastAPI-based order management system with JWT authentication, role-based access control, transactional order processing, and email notifications.

## 🚀 Features

- **JWT Authentication**: Secure login with role-based access (Admin/User)
- **Order Management**: Create orders with success/failure simulation
- **Email Notifications**: HTML email templates for order success/failure
- **Database Persistence**: SQLite database with proper schema
- **Rate Limiting**: 5 requests per minute protection
- **Monitoring**: Prometheus metrics and health checks
- **Logging**: Decorator-based logging for all operations
- **Testing**: Comprehensive unit, integration, and load tests

## 📋 API Endpoints

### Authentication

#### POST `/auth/register`
Register a new user (Admin only)

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "user" | "admin"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "newuser",
  "email": "newuser@example.com",
  "role": "user",
  "created_at": "2025-10-07T05:58:11"
}
```

#### POST `/auth/login`
Login and get JWT token

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_info": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "created_at": "2025-10-07T05:58:11"
  }
}
```

#### GET `/auth/me`
Get current user information

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin",
  "created_at": "2025-10-07T05:58:11"
}
```

### Order Management

#### POST `/orders/create`
Create a new order

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "success": true
}
```

**Response (Success):**
```json
{
  "id": 1,
  "user_id": 1,
  "success": true,
  "created_at": "2025-10-07T05:58:36"
}
```

**Response (Failure):**
```json
{
  "id": 2,
  "user_id": 1,
  "success": false,
  "created_at": "2025-10-07T05:59:33"
}
```

#### GET `/orders/`
Get orders (user sees their orders, admin sees all orders)

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "orders": [
    {
      "id": 1,
      "user_id": 1,
      "success": true,
      "created_at": "2025-10-07T05:58:36"
    }
  ]
}
```

### System Endpoints

#### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1759816698.022571,
  "version": "1.0.0",
  "environment": "development"
}
```

#### GET `/metrics`
Prometheus metrics endpoint

**Response:** Prometheus metrics format

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Virtual environment (recommended)

### Installation

1. **Clone and setup virtual environment:**
```bash
cd /Users/lohiyakeshav/Desktop/Test3
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize database:**
```bash
python init_db.py
```

4. **Start the application:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Environment Configuration

The application uses environment files for configuration:

- **Development:** `.env.dev`
- **Production:** `.env.prod`

Key configuration variables:
- `DATABASE_URL`: SQLite database path
- `SECRET_KEY`: JWT secret key
- `EMAIL_USER`: Gmail username
- `EMAIL_PASS`: Gmail app password
- `RATE_LIMIT_REQUESTS`: Rate limit (default: 5/minute)

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest app/tests/ -v

# Run specific test categories
python -m pytest app/tests/integration/ -v
python -m pytest app/tests/load/ -v
```

### Test Coverage
- **Unit Tests**: Service layer logic
- **Integration Tests**: Full API flow testing
- **Load Tests**: Concurrent request handling

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Metrics
```bash
curl http://localhost:8000/metrics/
```

### Logs
Application logs are written to `logs/app.log` with rotation support.

## 🔐 Security Features

- **Password Complexity**: Minimum 8 characters with uppercase, lowercase, digit, and special character
- **JWT Tokens**: Secure authentication with configurable expiration
- **Rate Limiting**: Protection against abuse (5 requests/minute)
- **Role-Based Access**: Admin and User roles with appropriate permissions

## 📧 Email Notifications

The system sends HTML email notifications for:
- **Order Success**: Confirmation email with success message
- **Order Failure**: Notification email with retry suggestion

Email templates are customizable in `app/services/email_service.py`.

## 🏗️ Architecture

```
app/
├── api/           # API routes
├── core/          # Configuration, security, logging
├── db/            # Database models and session
├── schemas/       # Pydantic models
├── services/      # Business logic
├── repositories/  # Data access layer
├── utils/         # Utilities and decorators
└── tests/         # Test suites
```

## 🚀 Production Deployment

1. **Set production environment:**
```bash
export ENVIRONMENT=production
```

2. **Use production configuration:**
```bash
cp .env.prod .env
```

3. **Run with production server:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📝 Default Credentials

After running `python init_db.py`:
- **Username:** admin
- **Password:** Admin123
- **Role:** admin

## 🔧 Development

### Code Quality
- Follows SOLID, KISS, and DRY principles
- Decorator-based logging for all operations
- Clean separation of concerns
- Comprehensive error handling

### Database
- SQLite for simplicity and portability
- Persistent storage across restarts
- Automatic table creation on startup

## 📄 License

This project is part of a technical demonstration and follows best practices for production-ready FastAPI applications.
