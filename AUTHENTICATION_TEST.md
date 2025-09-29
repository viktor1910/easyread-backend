# Testing the Authentication System

## How to Test the Login System

### 1. Start the Django Server

```bash
cd /d/EasyRead-Python/easyread
python manage.py runserver
```

### 2. Test User Registration (POST /users/register/)

```bash
curl -X POST http://127.0.0.1:8000/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpassword123",
    "password_confirmation": "testpassword123",
    "role": "user"
  }'
```

### 3. Test User Login (POST /users/login/)

```bash
curl -X POST http://127.0.0.1:8000/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

Expected Response:

```json
{
  "message": "Login successful",
  "token": "a1b2c3d4e5f6g7h8i9j0...",
  "user": {
    "id": 1,
    "username": "test",
    "email": "test@example.com",
    "role": "user",
    "first_name": "Test User",
    "last_name": "",
    "is_active": true,
    "date_joined": "2025-09-29T..."
  }
}
```

### 4. Test Protected Endpoint (GET /users/ - Admin Only)

```bash
# This should fail without token
curl -X GET http://127.0.0.1:8000/users/

# This should fail with user token (not admin)
curl -X GET http://127.0.0.1:8000/users/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# This should work with admin token
curl -X GET http://127.0.0.1:8000/users/ \
  -H "Authorization: Token ADMIN_TOKEN_HERE"
```

### 5. Test Logout (POST /users/logout/)

```bash
curl -X POST http://127.0.0.1:8000/users/logout/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 6. Create an Admin User for Testing

```bash
# In Django shell
python manage.py shell

# Then run:
from user.models import CustomUser
admin_user = CustomUser.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='adminpass123',
    role='admin'
)
```

## Permission Classes Usage Examples

### In Your Views:

```python
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdminUser, IsOwnerOrAdmin

# Only authenticated users can access
class SomeView(APIView):
    permission_classes = [IsAuthenticated]

# Only admin users can access
class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

# User can access their own data, admin can access all
class UserDataView(APIView):
    permission_classes = [IsOwnerOrAdmin]
```

## API Authentication Headers

For all protected endpoints, include the authorization header:

```
Authorization: Token a1b2c3d4e5f6g7h8i9j0...
```

## Summary

✅ Token-based authentication implemented
✅ Email-based login system
✅ Role-based permissions (admin/user)  
✅ Login/logout endpoints
✅ Custom permission classes
✅ Database migrations applied
