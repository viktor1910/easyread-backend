import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motoparts.settings')
django.setup()

from category.models import Category
from motopart.models import Motopart

# Clear existing data
print("Clearing existing data...")
Motopart.objects.all().delete()
Category.objects.all().delete()

# Create Categories
print("Creating categories...")
categories = [
    {
        'name': 'Phanh',
        'slug': 'phanh',
    },
    {
        'name': 'Lốp xe',
        'slug': 'lop-xe',
    },
    {
        'name': 'Đèn',
        'slug': 'den',
    },
    {
        'name': 'Gương',
        'slug': 'guong',
    },
    {
        'name': 'Yên xe',
        'slug': 'yen-xe',
    },
    {
        'name': 'Nhớt động cơ',
        'slug': 'nhot-dong-co',
    },
]

category_objects = []
for cat_data in categories:
    category = Category.objects.create(**cat_data)
    category_objects.append(category)
    print(f"Created category: {category.name}")

# Create Motoparts
print("\nCreating motoparts...")
motoparts = [
    # Phanh
    {
        'name': 'Má phanh trước Honda Air Blade',
        'slug': 'ma-phanh-truoc-honda-air-blade',
        'description': 'Má phanh chính hãng Honda cho Air Blade 125/150, chất lượng cao, độ bền tốt',
        'price': 250000,
        'discount': 10,
        'stock': 50,
        'status': 'active',
        'category': category_objects[0],
        'supplier': 'Honda Việt Nam',
        'manufacture_year': 2023,
    },
    {
        'name': 'Má phanh sau Yamaha Exciter',
        'slug': 'ma-phanh-sau-yamaha-exciter',
        'description': 'Má phanh sau dành cho Yamaha Exciter 150/155, êm ái, không ồn',
        'price': 180000,
        'discount': 5,
        'stock': 30,
        'status': 'active',
        'category': category_objects[0],
        'supplier': 'Yamaha Motor',
        'manufacture_year': 2023,
    },
    {
        'name': 'Dầu phanh DOT 4 Castrol',
        'slug': 'dau-phanh-dot-4-castrol',
        'description': 'Dầu phanh cao cấp DOT 4, dung tích 500ml, phù hợp mọi loại xe',
        'price': 120000,
        'discount': 0,
        'stock': 100,
        'status': 'active',
        'category': category_objects[0],
        'supplier': 'Castrol',
        'manufacture_year': 2024,
    },

    # Lốp xe
    {
        'name': 'Lốp Michelin Pilot Street 80/90-17',
        'slug': 'lop-michelin-pilot-street-80-90-17',
        'description': 'Lốp Michelin cao cấp, độ bám đường tốt, tuổi thọ cao',
        'price': 450000,
        'discount': 15,
        'stock': 25,
        'status': 'active',
        'category': category_objects[1],
        'supplier': 'Michelin',
        'manufacture_year': 2024,
    },
    {
        'name': 'Lốp Dunlop TT900 90/90-17',
        'slug': 'lop-dunlop-tt900-90-90-17',
        'description': 'Lốp Dunlop chất lượng, giá tốt, phù hợp xe số',
        'price': 380000,
        'discount': 10,
        'stock': 40,
        'status': 'active',
        'category': category_objects[1],
        'supplier': 'Dunlop',
        'manufacture_year': 2023,
    },
    {
        'name': 'Lốp IRC 100/80-17',
        'slug': 'lop-irc-100-80-17',
        'description': 'Lốp IRC chính hãng, độ bền cao, phù hợp xe côn tay',
        'price': 420000,
        'discount': 12,
        'stock': 35,
        'status': 'active',
        'category': category_objects[1],
        'supplier': 'IRC Tire',
        'manufacture_year': 2024,
    },

    # Đèn
    {
        'name': 'Đèn pha LED Honda SH Mode',
        'slug': 'den-pha-led-honda-sh-mode',
        'description': 'Đèn pha LED chính hãng Honda cho SH Mode, sáng mạnh, tiết kiệm điện',
        'price': 850000,
        'discount': 8,
        'stock': 20,
        'status': 'active',
        'category': category_objects[2],
        'supplier': 'Honda Việt Nam',
        'manufacture_year': 2023,
    },
    {
        'name': 'Đèn xi nhan Yamaha Sirius',
        'slug': 'den-xi-nhan-yamaha-sirius',
        'description': 'Đèn xi nhan zin Yamaha Sirius, chất lượng tốt',
        'price': 95000,
        'discount': 0,
        'stock': 60,
        'status': 'active',
        'category': category_objects[2],
        'supplier': 'Yamaha Motor',
        'manufacture_year': 2023,
    },
    {
        'name': 'Đèn hậu LED Wave Alpha',
        'slug': 'den-hau-led-wave-alpha',
        'description': 'Đèn hậu LED độ cho Wave Alpha, thiết kế đẹp',
        'price': 280000,
        'discount': 5,
        'stock': 45,
        'status': 'active',
        'category': category_objects[2],
        'supplier': 'Đồ Chơi Xe',
        'manufacture_year': 2024,
    },

    # Gương
    {
        'name': 'Gương chiếu hậu Honda Vision',
        'slug': 'guong-chieu-hau-honda-vision',
        'description': 'Gương chiếu hậu chính hãng Honda Vision, rõ nét',
        'price': 320000,
        'discount': 0,
        'stock': 30,
        'status': 'active',
        'category': category_objects[3],
        'supplier': 'Honda Việt Nam',
        'manufacture_year': 2023,
    },
    {
        'name': 'Gương Rizoma Spy R',
        'slug': 'guong-rizoma-spy-r',
        'description': 'Gương Rizoma cao cấp, thiết kế thể thao, phù hợp xe côn',
        'price': 650000,
        'discount': 15,
        'stock': 15,
        'status': 'active',
        'category': category_objects[3],
        'supplier': 'Rizoma',
        'manufacture_year': 2024,
    },

    # Yên xe
    {
        'name': 'Yên độ Winner X chính hãng',
        'slug': 'yen-do-winner-x-chinh-hang',
        'description': 'Yên độ Winner X, êm ái, thoáng khí, chất liệu cao cấp',
        'price': 580000,
        'discount': 10,
        'stock': 25,
        'status': 'active',
        'category': category_objects[4],
        'supplier': 'Honda Việt Nam',
        'manufacture_year': 2023,
    },
    {
        'name': 'Yên Air Blade 2023 zin',
        'slug': 'yen-air-blade-2023-zin',
        'description': 'Yên zin Air Blade 2023, nguyên bản từ Honda',
        'price': 450000,
        'discount': 0,
        'stock': 18,
        'status': 'active',
        'category': category_objects[4],
        'supplier': 'Honda Việt Nam',
        'manufacture_year': 2023,
    },

    # Nhớt động cơ
    {
        'name': 'Nhớt Motul 7100 10W40 1L',
        'slug': 'nhot-motul-7100-10w40-1l',
        'description': 'Nhớt Motul 7100 4T 10W40, dành cho xe số và xe tay ga, 1 lít',
        'price': 280000,
        'discount': 5,
        'stock': 80,
        'status': 'active',
        'category': category_objects[5],
        'supplier': 'Motul',
        'manufacture_year': 2024,
    },
    {
        'name': 'Nhớt Castrol Power1 10W40 1L',
        'slug': 'nhot-castrol-power1-10w40-1l',
        'description': 'Nhớt Castrol Power1 4T 10W40, bảo vệ động cơ tối ưu',
        'price': 195000,
        'discount': 8,
        'stock': 120,
        'status': 'active',
        'category': category_objects[5],
        'supplier': 'Castrol',
        'manufacture_year': 2024,
    },
    {
        'name': 'Nhớt Shell Advance AX7 10W40 800ml',
        'slug': 'nhot-shell-advance-ax7-10w40-800ml',
        'description': 'Nhớt Shell Advance AX7 bán tổng hợp, 800ml, phù hợp xe số',
        'price': 115000,
        'discount': 0,
        'stock': 150,
        'status': 'active',
        'category': category_objects[5],
        'supplier': 'Shell',
        'manufacture_year': 2024,
    },
    {
        'name': 'Nhớt Liqui Moly Street 10W40 1L',
        'slug': 'nhot-liqui-moly-street-10w40-1l',
        'description': 'Nhớt Liqui Moly cao cấp Đức, bảo vệ động cơ vượt trội',
        'price': 350000,
        'discount': 12,
        'stock': 50,
        'status': 'active',
        'category': category_objects[5],
        'supplier': 'Liqui Moly',
        'manufacture_year': 2024,
    },
]

for moto_data in motoparts:
    motopart = Motopart.objects.create(**moto_data)
    print(f"Created motopart: {motopart.name}")

print("\n" + "="*50)
print("Sample data inserted successfully!")
print(f"Total categories: {Category.objects.count()}")
print(f"Total motoparts: {Motopart.objects.count()}")
print("="*50)
