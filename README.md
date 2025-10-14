# EasyRead Motoparts - Backend API

EasyRead là một hệ thống thương mại điện tử bán phụ tùng xe máy được xây dựng bằng Django REST Framework.

## 📋 Tổng quan dự án

### Kiến trúc hệ thống

- **Backend**: Django REST Framework
- **Database**: SQLite3 (development), MySQL (production)
- **Authentication**: Email-based với role-based access control
- **Structure**: Microservice-like app organization

### Các module chính

- `user` - Quản lý người dùng và xác thực
- `category` - Danh mục sản phẩm
- `motopart` - Sản phẩm phụ tùng xe máy
- `carts` - Giỏ hàng
- `cartitem` - Chi tiết giỏ hàng
- `orders` - Đơn hàng (đang phát triển)
- `orderitem` - Chi tiết đơn hàng (đang phát triển)
- `transactions` - Giao dịch thanh toán (đang phát triển)

## 🚀 Cài đặt và chạy dự án

### Yêu cầu hệ thống

- Python 3.8+
- pip (Python package manager)
- Git

### 1. Clone repository

```bash
git clone https://github.com/viktor1910/easyread-backend.git
cd easyread-backend
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình database

```bash
cd motoparts

# Tạo migration files
python manage.py makemigrations

# Chạy migration để tạo database
python manage.py migrate
```

### 4. Tạo superuser (admin)

```bash
python manage.py createsuperuser
```

### 5. Chạy development server

```bash
python manage.py runserver
```

Server sẽ chạy tại: `http://127.0.0.1:8000/`

## 📊 Import dữ liệu mẫu

### Tự động import bằng Python script (Khuyến nghị)

Dự án đã có sẵn script Python để import dữ liệu mẫu tương thích với SQLite3:

```bash
# Di chuyển đến thư mục project
cd motoparts

# Chạy script import
python import_sample_data.py
```

Script sẽ hỏi bạn có muốn xóa dữ liệu cũ không:

- Nhấn `y` để xóa dữ liệu cũ và import mới
- Nhấn `n` hoặc `Enter` để giữ dữ liệu cũ và chỉ thêm dữ liệu mới

### Dữ liệu mẫu bao gồm:

#### 8 Danh mục sản phẩm:

1. Phụ tùng động cơ
2. Phụ tùng phanh
3. Đèn và điện
4. Lốp xe
5. Yên xe và tay lái
6. Pô và ống xả
7. Dầu nhớt
8. Phụ kiện trang trí

#### 27 Sản phẩm phụ tùng xe máy:

- Piston, nhớt động cơ, lọc gió
- Má phanh, dầu phanh, đĩa phanh
- Đèn LED, bình ắc quy
- Lốp Michelin, Dunlop
- Yên độ, tay lái racing
- Pô Akrapovic, Yoshimura
- Nhớt Castrol, Shell, Liqui Moly
- Baga, kính chắn gió, thùng đồ

### Kiểm tra dữ liệu đã import

```bash
# Kiểm tra số lượng categories và motoparts
python manage.py shell -c "
from category.models import Category
from motopart.models import Motopart
print(f'Categories: {Category.objects.count()}')
print(f'Motoparts: {Motopart.objects.count()}')
"
```

## 🔧 Cấu hình phát triển

### Database Settings

- **Development**: SQLite3 (`db.sqlite3`)
- **Production**: MySQL (cấu hình trong `settings.py`)

### API Endpoints chính

#### Categories

- `GET /categories/` - Danh sách danh mục
- `POST /categories/` - Tạo danh mục mới
- `GET /categories/{id}/` - Chi tiết danh mục
- `PUT /categories/{id}/` - Cập nhật danh mục
- `DELETE /categories/{id}/` - Xóa danh mục

#### Motoparts

- `GET /motoparts/` - Danh sách sản phẩm
- `POST /motoparts/` - Tạo sản phẩm mới
- `GET /motoparts/{id}/` - Chi tiết sản phẩm
- `PUT /motoparts/{id}/` - Cập nhật sản phẩm
- `DELETE /motoparts/{id}/` - Xóa sản phẩm

#### Users

- `POST /users/register/` - Đăng ký
- `POST /users/login/` - Đăng nhập
- `GET /users/profile/` - Thông tin profile

#### Carts

- `GET /carts/` - Giỏ hàng của user
- `POST /carts/` - Tạo giỏ hàng
- `PUT /carts/{id}/` - Cập nhật giỏ hàng

### Django Admin

Truy cập Django Admin tại: `http://127.0.0.1:8000/admin/`

## 📁 Cấu trúc thư mục

```
EasyRead-Python/
├── motoparts/                  # Django project root
│   ├── manage.py              # Django management script
│   ├── db.sqlite3             # SQLite database
│   ├── import_sample_data.py  # Script import dữ liệu mẫu
│   ├── motoparts/             # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── user/                  # User management app
│   ├── category/              # Category management app
│   ├── motopart/              # Product management app
│   ├── carts/                 # Shopping cart app
│   ├── cartitem/              # Cart items app
│   ├── orders/                # Orders app (in development)
│   ├── orderitem/             # Order items app (in development)
│   └── transactions/          # Payment transactions app (in development)
├── requirements.txt           # Python dependencies
├── sample_data.sql           # Original MySQL sample data
├── easyread_schema.dbml      # Database schema
└── README.md                 # This file
```

## 🛠️ Development Commands

### Tạo app mới

```bash
python manage.py startapp <app_name>
```

### Database operations

```bash
# Tạo migration files
python manage.py makemigrations

# Xem SQL sẽ được thực thi
python manage.py sqlmigrate <app_name> <migration_number>

# Chạy migrations
python manage.py migrate

# Reset database (xóa tất cả data)
python manage.py flush
```

### Debugging

```bash
# Chạy Django shell
python manage.py shell

# Kiểm tra cấu hình
python manage.py check

# Thu thập static files (production)
python manage.py collectstatic
```

## 🔍 Testing API với Postman

Dự án có sẵn Postman collection: `EasyRead_Postman_Collection.json`

Import file này vào Postman để test các API endpoints.

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **ModuleNotFoundError**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Database locked**:

   ```bash
   # Đảm bảo không có process nào đang sử dụng database
   python manage.py migrate
   ```

3. **Port already in use**:

   ```bash
   # Sử dụng port khác
   python manage.py runserver 8001
   ```

4. **Import sample data fails**:
   ```bash
   # Kiểm tra database đã được migrate chưa
   python manage.py showmigrations
   python manage.py migrate
   ```

## 📝 Notes cho Developer

### Model Conventions:

- Tất cả models có `created_at` và `updated_at`
- Sử dụng `STATUS_CHOICES` cho các trường status
- Foreign keys sử dụng `related_name` để reverse lookup
- Override `__str__()` method cho tất cả models

### API Patterns:

- Sử dụng Django REST Framework Generic Views
- Serializers có nested relationships với `read_only=True`
- Computed properties như `discounted_price`, `is_available`

### Security:

- Email-based authentication
- Role-based access control (`admin`/`user`)
- CORS configured for frontend integration

## 🚧 Roadmap

### Đang phát triển:

- [ ] Orders workflow
- [ ] Payment integration
- [ ] Email notifications
- [ ] Product reviews
- [ ] Inventory management

### Hoàn thành:

- [x] User authentication
- [x] Category management
- [x] Product management
- [x] Shopping cart
- [x] Sample data import

## 📞 Liên hệ

- **Repository**: https://github.com/viktor1910/easyread-backend
- **Developer**: viktor1910

---

**Happy Coding! 🚀**
