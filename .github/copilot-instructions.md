# EasyRead Coding Guidelines

## Architecture Overview

EasyRead is a Django REST API-based book e-commerce system with a microservice-like app structure. Core domains: books, categories, users, shopping carts, orders, and transactions.

### Key Design Patterns

- **Custom User Model**: Uses `AUTH_USER_MODEL = 'user.CustomUser'` with email-based authentication and role-based access (`admin`/`user`)
- **String-based Foreign Keys**: CartItem references `'carts.Cart'` and `'book.Book'` as strings to avoid circular imports
- **Property-based Calculations**: Models use `@property` methods for computed fields (`discounted_price`, `is_available`, `subtotal`)
- **Defensive Programming**: Models override `save()` methods for data validation (e.g., CartItem ensures quantity > 0)

### Model Relationships & Business Logic

```python
# Core entities and their relationships:
Category (1) ← (many) Book ← (many) CartItem → (1) Cart → (1) CustomUser
```

**Key Model Conventions:**

- All models include `created_at`/`updated_at` timestamps with `auto_now_add`/`auto_now`
- Status fields use `CHOICES` tuples: `('active', 'Active')`, `('inactive', 'Inactive')`
- Use `related_name` for reverse relationships: `Category.books`, `Cart.items`
- Price calculations always consider discounts via `Book.discounted_price` property
- Cart totals use Django ORM aggregations with `F()` expressions for database-level calculations

### App Structure & Organization

- **Installed Apps Order**: Core Django apps → Custom business apps → Third-party (DRF)
- **Placeholder Apps**: `orders`, `orderitem`, `transactions` exist but are empty (models.py contains only imports)
- **Active Apps**: `user`, `category`, `book`, `cartitem`, `carts` contain full implementations

### API Patterns

- **Generic Views**: Use `generics.ListCreateAPIView` for standard CRUD operations
- **Serializer Patterns**:
  - Nested serializers with `read_only=True` for display (e.g., `CategorySerializer` in `BookSerializer`)
  - Separate `*_id` fields with `write_only=True` for creation/updates
  - `ReadOnlyField()` for computed properties like `discounted_price`, `is_available`
- **URL Structure**: Domain-based routing (`/books/`, `/categories/`) included in main `urls.py`

### Database Configuration

- **Development**: SQLite (`db.sqlite3`)
- **Production Ready**: MySQL client configured via `mysqlclient` dependency
- **Migrations**: Apps have migration files; recent addition is `cartitem` app

### Development Workflow

```bash
# Standard Django commands in easyread/ directory:
python manage.py startapp <appname>
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Code Quality Standards

- **Model Methods**: Always include meaningful `__str__()` methods
- **Meta Classes**: Define `ordering` (typically `['-created_at']`) and constraints (`unique_together`)
- **Import Organization**: Relative imports for same-app modules (`.models`, `.serializers`)
- **Validation**: Use model-level validation via `save()` overrides rather than serializer validation

### Current Development State

- **Working Features**: User management, categories, books, cart functionality
- **In Development**: Orders and transaction processing (placeholder apps created)
- **Next Steps**: Implement order workflow connecting carts → orders → transactions
