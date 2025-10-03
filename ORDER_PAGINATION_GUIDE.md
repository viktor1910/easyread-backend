# Order API Pagination Guide

## Overview

The Order API now includes comprehensive pagination, filtering, search, and ordering capabilities for both user and admin endpoints.

## Pagination Classes

### OrderPagination (User Endpoints)

- **Default page size**: 10 items per page
- **Customizable page size**: Use `page_size` parameter (max 50)
- **Page navigation**: Use `page` parameter

### OrderAdminPagination (Admin Endpoints)

- **Default page size**: 25 items per page
- **Customizable page size**: Use `page_size` parameter (max 100)
- **Page navigation**: Use `page` parameter

## API Endpoints

### 1. OrderListCreateView (User/Admin)

```
GET /orders/?page=1&page_size=10
POST /orders/
```

### 2. OrderListAdminView (Admin Only)

```
GET /admin/orders/?page=1&page_size=25
```

### 3. get_user_orders (Deprecated - Use OrderListCreateView)

```
GET /user/orders/?page=1&page_size=10
```

## Response Format

### Standard Pagination Response

```json
{
  "pagination": {
    "count": 150,
    "next": "http://localhost:8000/orders/?page=2",
    "previous": null,
    "current_page": 1,
    "total_pages": 15,
    "page_size": 10
  },
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
      },
      "status": "pending",
      "total_amount": "99.99",
      "shipping_address": "123 Main St, City, State",
      "billing_address": "123 Main St, City, State",
      "notes": "Please deliver after 5 PM",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
    // ... more orders
  ]
}
```

### Admin List Response (OrderListAdminView)

```json
{
  "pagination": {
    "count": 500,
    "next": "http://localhost:8000/admin/orders/?page=2",
    "previous": null,
    "current_page": 1,
    "total_pages": 20,
    "page_size": 25
  },
  "results": [
    {
      "id": 1,
      "user_email": "user@example.com",
      "status": "pending",
      "total_amount": "99.99",
      "created_at": "2024-01-15T10:30:00Z"
    }
    // ... more orders
  ]
}
```

## Filtering Options

### Available Filters

#### OrderListCreateView & OrderListAdminView

- `status`: Filter by order status
- `user`: Filter by user ID (admin only)
- `created_at`: Filter by creation date (admin only)

#### Order Status Options

- `pending`
- `confirmed`
- `processing`
- `shipped`
- `delivered`
- `cancelled`
- `refunded`

### Filter Examples

```bash
# Filter by status
GET /orders/?status=pending

# Filter by user (admin only)
GET /admin/orders/?user=1

# Filter by multiple statuses (admin)
GET /admin/orders/?status=pending&status=confirmed

# Filter by date range (admin)
GET /admin/orders/?created_at__gte=2024-01-01&created_at__lte=2024-01-31
```

## Search Functionality

### Search Fields

#### OrderListCreateView

- `user__email`: User's email address
- `user__first_name`: User's first name
- `user__last_name`: User's last name
- `shipping_address`: Shipping address content

#### OrderListAdminView (Extended Search)

- `user__email`: User's email address
- `user__first_name`: User's first name
- `user__last_name`: User's last name
- `id`: Order ID
- `shipping_address`: Shipping address content

### Search Examples

```bash
# Search for orders by user email
GET /orders/?search=john@example.com

# Search by user name
GET /orders/?search=John

# Search by shipping address
GET /orders/?search="123 Main St"

# Search with pagination
GET /orders/?search=john&page=1&page_size=5
```

## Ordering Options

### Available Ordering Fields

#### OrderListCreateView

- `created_at`: Order creation date
- `updated_at`: Last update date
- `total_amount`: Order total amount
- `status`: Order status

#### OrderListAdminView (Extended Ordering)

- `created_at`: Order creation date
- `updated_at`: Last update date
- `total_amount`: Order total amount
- `status`: Order status
- `user__email`: User's email address

### Ordering Examples

```bash
# Sort by total amount (ascending)
GET /orders/?ordering=total_amount

# Sort by total amount (descending)
GET /orders/?ordering=-total_amount

# Sort by creation date (newest first - default)
GET /orders/?ordering=-created_at

# Sort by creation date (oldest first)
GET /orders/?ordering=created_at

# Sort by user email (admin only)
GET /admin/orders/?ordering=user__email

# Multiple field ordering
GET /orders/?ordering=-created_at,total_amount
```

## Combined Usage Examples

### Example 1: User's pending orders, sorted by date

```bash
GET /orders/?status=pending&ordering=-created_at&page=1&page_size=5
```

### Example 2: Admin search for orders by user email

```bash
GET /admin/orders/?search=john@example.com&ordering=-total_amount
```

### Example 3: Admin view recent orders with large page size

```bash
GET /admin/orders/?ordering=-created_at&page_size=50
```

### Example 4: Filter completed orders by amount

```bash
GET /orders/?status=delivered&ordering=-total_amount&page=1
```

## Permissions & Access Control

### User Endpoints (OrderListCreateView)

- **Authentication**: Required
- **GET**: Users see only their own orders
- **POST**: Users can create orders for themselves
- **Admin**: Can see all orders and create for any user

### Admin Endpoints (OrderListAdminView)

- **Authentication**: Required
- **Permission**: Admin users only
- **Access**: All orders in the system

### Function-based View (get_user_orders) - Deprecated

- **Authentication**: Required
- **Access**: User's own orders only
- **Pagination**: Basic pagination support

## Performance Considerations

### Database Optimization

- Default ordering by `-created_at` with database index
- Filtered queries use appropriate indexes
- Search uses icontains lookup for case-insensitive matching

### Pagination Limits

- User endpoints: Max 50 items per page
- Admin endpoints: Max 100 items per page
- Default page sizes optimized for typical use cases

### Query Optimization

- Related fields (user) are properly selected to avoid N+1 queries
- Admin list view uses simplified serializer for better performance

## Django Admin Integration

### Admin Panel Features

- **Pagination**: 25 items per page
- **Search**: User email, name, and order ID
- **Filtering**: Status, creation date, update date
- **Date Hierarchy**: By creation date
- **Ordering**: Newest orders first

### Admin Display

- List view shows ID, user, status, amount, and creation date
- Fieldsets organize form fields logically
- Read-only timestamp fields
- Proper field organization for better UX

## Migration Notes

### Breaking Changes

- All list endpoints now return paginated responses
- Simple list responses are replaced with pagination wrapper
- `get_user_orders` function-based view is deprecated

### Backward Compatibility

- Function-based view maintains basic pagination
- Existing filters and search parameters continue to work
- Response format is enhanced but maintains result structure

## Error Handling

### Common Errors

- **Invalid page number**: Returns 404
- **Page size exceeding limit**: Uses maximum allowed size
- **Invalid filter values**: Ignored gracefully
- **Invalid ordering fields**: Ignored, uses default ordering

### Permission Errors

- **Non-admin accessing admin endpoints**: 403 Forbidden
- **Unauthenticated requests**: 401 Unauthorized
