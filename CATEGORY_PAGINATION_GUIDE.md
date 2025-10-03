# Category API Pagination Guide

## Overview

The Category API now includes pagination, search, and ordering capabilities similar to the Motopart API.

## Pagination Features

### Basic Pagination

- **Default page size**: 15 items per page
- **Customizable page size**: Use `page_size` parameter (max 50)
- **Page navigation**: Use `page` parameter

### API Endpoints

```
GET /categories/?page=1&page_size=10
```

### Response Format

```json
{
  "pagination": {
    "count": 25,
    "next": "http://localhost:8000/categories/?page=2",
    "previous": null,
    "current_page": 1,
    "total_pages": 3,
    "page_size": 10
  },
  "results": [
    {
      "id": 1,
      "name": "Engine Parts",
      "slug": "engine-parts",
      "image": "https://example.com/engine-parts.jpg",
      "motoparts_count": 25,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
    // ... more categories
  ]
}
```

## Search Functionality

### Search Fields

- `name`: Search in category name
- `slug`: Search in category slug

### Search Examples

```bash
# Search for categories containing "engine"
GET /categories/?search=engine

# Search with pagination
GET /categories/?search=parts&page=1&page_size=5
```

## Ordering Options

### Available Ordering Fields

- `name`: Sort by category name
- `created_at`: Sort by creation date (default: newest first)

### Ordering Examples

```bash
# Sort by name (ascending)
GET /categories/?ordering=name

# Sort by name (descending)
GET /categories/?ordering=-name

# Sort by creation date (newest first - default)
GET /categories/?ordering=-created_at

# Sort by creation date (oldest first)
GET /categories/?ordering=created_at
```

## Combined Usage Examples

### Example 1: Search and sort by name

```bash
GET /categories/?search=engine&ordering=name
```

### Example 2: Get latest categories with pagination

```bash
GET /categories/?ordering=-created_at&page=1&page_size=5
```

### Example 3: Search with custom page size

```bash
GET /categories/?search=parts&page_size=20
```

## Enhanced Features

### Motoparts Count

Each category now includes a `motoparts_count` field showing the number of active motoparts in that category.

### Permissions

- **GET requests**: Public access (no authentication required)
- **POST requests**: Admin users only
- **PUT/PATCH/DELETE requests**: Admin users only

## Implementation Details

### Pagination Class

- Custom `CategoryPagination` class with smaller default page size (15)
- Maximum page size limited to 50 for performance
- Enhanced response format with detailed pagination metadata

### Performance Considerations

- Default ordering by `-created_at` for consistent results
- Efficient counting of motoparts using filtered queries
- Search uses icontains lookup for case-insensitive matching

### API Consistency

- Similar pagination format to Motopart API
- Consistent error handling and response structure
- Compatible with existing frontend implementations

## Usage Tips

1. **For browsing categories**: Use default pagination without filters

   ```bash
   GET /categories/
   ```

2. **For searching specific categories**: Use search parameter

   ```bash
   GET /categories/?search=brake
   ```

3. **For category lists with counts**: The motoparts_count is automatically included

   ```bash
   GET /categories/?ordering=name
   ```

4. **For admin operations**: Ensure proper authentication for POST/PUT/DELETE operations
