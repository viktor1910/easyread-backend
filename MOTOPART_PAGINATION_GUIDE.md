# Motopart API Pagination Guide

## Overview

The Motopart API now includes comprehensive pagination, filtering, and ordering capabilities.

## Pagination Features

### Basic Pagination

- **Default page size**: 20 items per page
- **Customizable page size**: Use `page_size` parameter (max 100)
- **Page navigation**: Use `page` parameter

### API Endpoints

```
GET /motoparts/?page=1&page_size=10
```

### Response Format

```json
{
  "pagination": {
    "count": 150,
    "next": "http://localhost:8000/motoparts/?page=2",
    "previous": null,
    "current_page": 1,
    "total_pages": 15,
    "page_size": 10
  },
  "results": [
    {
      "id": 1,
      "name": "Engine Oil Filter",
      "slug": "engine-oil-filter",
      "price": 25.99,
      "discount": 10.0,
      "discounted_price": 23.39,
      "stock": 50,
      "status": "active",
      "description": "High-quality engine oil filter",
      "image_url": "https://example.com/image.jpg",
      "category": {
        "id": 1,
        "name": "Filters",
        "slug": "filters"
      },
      "manufacture_year": 2023,
      "supplier": "MotoParts Co.",
      "is_available": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
    // ... more items
  ]
}
```

## Filtering Options

### Available Filters

- `category`: Filter by category ID
- `status`: Filter by status (active, inactive, out_of_stock)
- `manufacture_year`: Filter by manufacture year
- `supplier`: Filter by supplier name

### Filter Examples

```bash
# Filter by category
GET /motoparts/?category=1

# Filter by status
GET /motoparts/?status=active

# Filter by manufacture year
GET /motoparts/?manufacture_year=2023

# Filter by supplier
GET /motoparts/?supplier=MotoParts Co.

# Combine multiple filters
GET /motoparts/?category=1&status=active&manufacture_year=2023
```

## Search Functionality

### Search Fields

- `name`: Search in product name
- `description`: Search in product description
- `supplier`: Search in supplier name

### Search Examples

```bash
# Search for products containing "filter"
GET /motoparts/?search=filter

# Search with pagination
GET /motoparts/?search=engine&page=1&page_size=5
```

## Ordering Options

### Available Ordering Fields

- `name`: Sort by product name
- `price`: Sort by original price
- `discounted_price`: Sort by discounted price
- `stock`: Sort by stock quantity
- `manufacture_year`: Sort by manufacture year
- `created_at`: Sort by creation date (default: newest first)

### Ordering Examples

```bash
# Sort by price (ascending)
GET /motoparts/?ordering=price

# Sort by price (descending)
GET /motoparts/?ordering=-price

# Sort by multiple fields
GET /motoparts/?ordering=-created_at,name

# Sort by discounted price
GET /motoparts/?ordering=discounted_price
```

## Combined Usage Examples

### Example 1: Active products, sorted by price, with pagination

```bash
GET /motoparts/?status=active&ordering=price&page=1&page_size=15
```

### Example 2: Search for filters, show available only, latest first

```bash
GET /motoparts/?search=filter&status=active&ordering=-created_at&page=1
```

### Example 3: Products from specific year and supplier

```bash
GET /motoparts/?manufacture_year=2023&supplier=MotoParts Co.&page_size=25
```

## Implementation Details

### Pagination Class

- Custom `MotopartPagination` class provides enhanced response format
- Includes detailed pagination metadata
- Configurable page sizes with reasonable limits

### Performance Considerations

- Default ordering by `-created_at` for consistent results
- Database indexes on commonly filtered fields recommended
- Search uses icontains lookup for case-insensitive matching

### Error Handling

- Invalid page numbers return 404
- Page size exceeding max limit (100) uses max limit
- Invalid filter values are ignored gracefully
