# EasyRead API Usage Guide

## 🚀 How to Login and Use the API

### 📋 Prerequisites

1. Start the Django server: `python manage.py runserver`
2. Server will be available at: `http://127.0.0.1:8000`

---

## 🔧 Using Postman

### 1. User Registration

**Method:** `POST`  
**URL:** `http://127.0.0.1:8000/users/register/`  
**Headers:**

```
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "mypassword123",
  "password_confirmation": "mypassword123",
  "role": "user"
}
```

### 2. User Login

**Method:** `POST`  
**URL:** `http://127.0.0.1:8000/users/login/`  
**Headers:**

```
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "email": "john@example.com",
  "password": "mypassword123"
}
```

**Expected Response:**

```json
{
  "message": "Login successful",
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "role": "user",
    "first_name": "John Doe",
    "last_name": "",
    "is_active": true,
    "date_joined": "2025-09-29T10:30:00Z"
  }
}
```

### 3. Using Token for Protected Endpoints

**Method:** `GET`  
**URL:** `http://127.0.0.1:8000/users/` (Admin only)  
**Headers:**

```
Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
Content-Type: application/json
```

### 4. User Logout

**Method:** `POST`  
**URL:** `http://127.0.0.1:8000/users/logout/`  
**Headers:**

```
Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
Content-Type: application/json
```

---

## 💻 Using JavaScript

### 1. Login Function

```javascript
async function loginUser(email, password) {
  try {
    const response = await fetch("http://127.0.0.1:8000/users/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      // Store token for future requests
      localStorage.setItem("authToken", data.token);
      localStorage.setItem("userData", JSON.stringify(data.user));

      console.log("Login successful:", data);
      return { success: true, data: data };
    } else {
      console.error("Login failed:", data);
      return { success: false, error: data };
    }
  } catch (error) {
    console.error("Network error:", error);
    return { success: false, error: error.message };
  }
}

// Usage example
loginUser("john@example.com", "mypassword123").then((result) => {
  if (result.success) {
    console.log("Logged in successfully!");
    console.log("Token:", result.data.token);
  } else {
    console.log("Login failed:", result.error);
  }
});
```

### 2. Register Function

```javascript
async function registerUser(name, email, password, role = "user") {
  try {
    const response = await fetch("http://127.0.0.1:8000/users/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
        password: password,
        password_confirmation: password,
        role: role,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      console.log("Registration successful:", data);
      return { success: true, data: data };
    } else {
      console.error("Registration failed:", data);
      return { success: false, error: data };
    }
  } catch (error) {
    console.error("Network error:", error);
    return { success: false, error: error.message };
  }
}
```

### 3. Making Authenticated Requests

```javascript
async function makeAuthenticatedRequest(url, method = "GET", body = null) {
  const token = localStorage.getItem("authToken");

  if (!token) {
    throw new Error("No authentication token found. Please log in first.");
  }

  const options = {
    method: method,
    headers: {
      Authorization: `Token ${token}`,
      "Content-Type": "application/json",
    },
  };

  if (body && (method === "POST" || method === "PUT" || method === "PATCH")) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, options);
    const data = await response.json();

    if (response.ok) {
      return { success: true, data: data };
    } else {
      return { success: false, error: data };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Usage examples:
// Get user list (admin only)
makeAuthenticatedRequest("http://127.0.0.1:8000/users/").then((result) =>
  console.log(result)
);

// Get books
makeAuthenticatedRequest("http://127.0.0.1:8000/books/").then((result) =>
  console.log(result)
);
```

### 4. Logout Function

```javascript
async function logoutUser() {
  const token = localStorage.getItem("authToken");

  if (!token) {
    console.log("User is not logged in");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/users/logout/", {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();

    if (response.ok) {
      // Clear stored data
      localStorage.removeItem("authToken");
      localStorage.removeItem("userData");

      console.log("Logout successful:", data);
      return { success: true, data: data };
    } else {
      console.error("Logout failed:", data);
      return { success: false, error: data };
    }
  } catch (error) {
    console.error("Network error:", error);
    return { success: false, error: error.message };
  }
}
```

### 5. Complete Login Form Example (HTML + JavaScript)

```html
<!DOCTYPE html>
<html>
  <head>
    <title>EasyRead Login</title>
  </head>
  <body>
    <div id="loginForm">
      <h2>Login</h2>
      <input type="email" id="email" placeholder="Email" required />
      <input type="password" id="password" placeholder="Password" required />
      <button onclick="handleLogin()">Login</button>
    </div>

    <div id="userInfo" style="display: none;">
      <h2>Welcome!</h2>
      <p id="userDetails"></p>
      <button onclick="handleLogout()">Logout</button>
    </div>

    <script>
      async function handleLogin() {
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const result = await loginUser(email, password);

        if (result.success) {
          document.getElementById("loginForm").style.display = "none";
          document.getElementById("userInfo").style.display = "block";
          document.getElementById(
            "userDetails"
          ).textContent = `Logged in as: ${result.data.user.email} (${result.data.user.role})`;
        } else {
          alert("Login failed: " + JSON.stringify(result.error));
        }
      }

      async function handleLogout() {
        const result = await logoutUser();

        if (result.success) {
          document.getElementById("loginForm").style.display = "block";
          document.getElementById("userInfo").style.display = "none";
          document.getElementById("email").value = "";
          document.getElementById("password").value = "";
        }
      }

      // Check if user is already logged in
      window.onload = function () {
        const token = localStorage.getItem("authToken");
        const userData = localStorage.getItem("userData");

        if (token && userData) {
          const user = JSON.parse(userData);
          document.getElementById("loginForm").style.display = "none";
          document.getElementById("userInfo").style.display = "block";
          document.getElementById(
            "userDetails"
          ).textContent = `Logged in as: ${user.email} (${user.role})`;
        }
      };

      // Include the login/logout functions here...
      // (Copy the loginUser and logoutUser functions from above)
    </script>
  </body>
</html>
```

---

## 🔍 Testing Steps

### Step 1: Start Django Server

```bash
cd /d/EasyRead-Python/easyread
python manage.py runserver
```

### Step 2: Test with Postman or JavaScript

1. First register a user
2. Then login to get a token
3. Use the token for authenticated requests

### Step 3: Common Issues & Solutions

**CORS Issues (if calling from browser):**
Add to `settings.py`:

```python
# Install django-cors-headers first: pip install django-cors-headers

INSTALLED_APPS = [
    # ... existing apps
    'corsheaders',
]

MIDDLEWARE = [
    # ... existing middleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Allow all origins (for development only)
CORS_ALLOW_ALL_ORIGINS = True
```

**Authentication Required Error:**
Make sure to include the `Authorization: Token YOUR_TOKEN` header in all protected requests.

---

## 📝 Available Endpoints Summary

| Method | Endpoint           | Auth Required       | Description       |
| ------ | ------------------ | ------------------- | ----------------- |
| POST   | `/users/register/` | No                  | Register new user |
| POST   | `/users/login/`    | No                  | Login user        |
| POST   | `/users/logout/`   | Yes                 | Logout user       |
| GET    | `/users/`          | Yes (Admin)         | List all users    |
| GET    | `/books/`          | Depends on settings | List books        |
| GET    | `/categories/`     | Depends on settings | List categories   |

Remember to replace `127.0.0.1:8000` with your actual server URL in production!
