#!/usr/bin/env python
"""
Sample Data Import Script for EasyRead Motoparts
Converts the MySQL sample data to work with SQLite3 using Django ORM
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motoparts.settings')
django.setup()

from category.models import Category
from motopart.models import Motopart

def clear_existing_data():
    """Clear existing data (optional)"""
    print("Clearing existing data...")
    Motopart.objects.all().delete()
    Category.objects.all().delete()
    print("✓ Existing data cleared")

def import_categories():
    """Import sample categories"""
    print("Importing categories...")
    
    categories_data = [
        {
            'id': 1,
            'name': 'Phụ tùng động cơ',
            'slug': 'phu-tung-dong-co',
            'image': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800'
        },
        {
            'id': 2,
            'name': 'Phụ tùng phanh',
            'slug': 'phu-tung-phanh',
            'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800'
        },
        {
            'id': 3,
            'name': 'Đèn và điện',
            'slug': 'den-va-dien',
            'image': 'https://images.unsplash.com/photo-1449247666642-264389f5f5b1?w=800'
        },
        {
            'id': 4,
            'name': 'Lốp xe',
            'slug': 'lop-xe',
            'image': 'https://images.unsplash.com/photo-1629870055365-e0ed3c0c49a2?w=800'
        },
        {
            'id': 5,
            'name': 'Yên xe và tay lái',
            'slug': 'yen-xe-va-tay-lai',
            'image': 'https://images.unsplash.com/photo-1558980664-769d59546b3d?w=800'
        },
        {
            'id': 6,
            'name': 'Pô và ống xả',
            'slug': 'po-va-ong-xa',
            'image': 'https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=800'
        },
        {
            'id': 7,
            'name': 'Dầu nhớt',
            'slug': 'dau-nhot',
            'image': 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=800'
        },
        {
            'id': 8,
            'name': 'Phụ kiện trang trí',
            'slug': 'phu-kien-trang-tri',
            'image': 'https://images.unsplash.com/photo-1609630875171-b1321377ee65?w=800'
        }
    ]
    
    for category_data in categories_data:
        category, created = Category.objects.get_or_create(
            id=category_data['id'],
            defaults={
                'name': category_data['name'],
                'slug': category_data['slug'],
                'image': category_data['image']
            }
        )
        if created:
            print(f"✓ Created category: {category.name}")
        else:
            print(f"• Category already exists: {category.name}")

def import_motoparts():
    """Import sample motoparts"""
    print("Importing motoparts...")
    
    motoparts_data = [
        # Phụ tùng động cơ (category_id = 1)
        {
            'id': 1,
            'name': 'Piston Honda Wave 110 STD',
            'slug': 'piston-honda-wave-110-std',
            'price': 250000,
            'discount': 10.0,
            'stock': 50,
            'status': 'active',
            'description': 'Piston chính hãng Honda Wave 110, kích thước chuẩn STD, chất liệu hợp kim nhôm cao cấp, độ bền cao',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80',
            'category_id': 1,
            'manufacture_year': 2024,
            'supplier': 'Honda Official'
        },
        {
            'id': 2,
            'name': 'Nhớt động cơ Motul 7100 10W40',
            'slug': 'nhot-dong-co-motul-7100-10w40',
            'price': 320000,
            'discount': 5.0,
            'stock': 100,
            'status': 'active',
            'description': 'Dầu nhớt tổng hợp 100% Motul 7100, độ nhớt 10W40, phù hợp động cơ 4 thì',
            'image_url': 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=800&q=80',
            'category_id': 1,
            'manufacture_year': 2024,
            'supplier': 'Motul'
        },
        {
            'id': 3,
            'name': 'Lọc gió động cơ Yamaha Exciter 150',
            'slug': 'loc-gio-dong-co-yamaha-exciter-150',
            'price': 85000,
            'discount': 0,
            'stock': 75,
            'status': 'active',
            'description': 'Lọc gió động cơ chính hãng Yamaha Exciter 150, chất liệu lọc cao cấp',
            'image_url': 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=800&q=80',
            'category_id': 1,
            'manufacture_year': 2024,
            'supplier': 'Yamaha Official'
        },
        {
            'id': 4,
            'name': 'Xích nhông dĩa Honda Winner X',
            'slug': 'xich-nhong-dia-honda-winner-x',
            'price': 450000,
            'discount': 15.0,
            'stock': 30,
            'status': 'active',
            'description': 'Bộ xích nhông dĩa chính hãng Honda Winner X, độ bền cao, giảm ồn tốt',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&fit=crop',
            'category_id': 1,
            'manufacture_year': 2024,
            'supplier': 'Honda Official'
        },
        
        # Phụ tùng phanh (category_id = 2)
        {
            'id': 5,
            'name': 'Má phanh trước Yamaha NVX 155',
            'slug': 'ma-phanh-truoc-yamaha-nvx-155',
            'price': 180000,
            'discount': 8.0,
            'stock': 60,
            'status': 'active',
            'description': 'Má phanh đĩa trước chính hãng Yamaha NVX 155, lực phanh tốt, ít bụi',
            'image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80',
            'category_id': 2,
            'manufacture_year': 2024,
            'supplier': 'Yamaha Official'
        },
        {
            'id': 6,
            'name': 'Dầu phanh Motul DOT 4',
            'slug': 'dau-phanh-motul-dot-4',
            'price': 95000,
            'discount': 0,
            'stock': 120,
            'status': 'active',
            'description': 'Dầu phanh Motul DOT 4, điểm sôi cao, chống ăn mòn hệ thống phanh',
            'image_url': 'https://images.unsplash.com/photo-1485291571150-772bcfc10da5?w=800&q=80',
            'category_id': 2,
            'manufacture_year': 2024,
            'supplier': 'Motul'
        },
        {
            'id': 7,
            'name': 'Đĩa phanh trước Honda Winner X',
            'slug': 'dia-phanh-truoc-honda-winner-x',
            'price': 550000,
            'discount': 12.0,
            'stock': 25,
            'status': 'active',
            'description': 'Đĩa phanh trước chính hãng Honda Winner X, đường kính 296mm, chất liệu thép không gỉ',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&sat=-100',
            'category_id': 2,
            'manufacture_year': 2024,
            'supplier': 'Honda Official'
        },
        
        # Đèn và điện (category_id = 3)
        {
            'id': 8,
            'name': 'Đèn pha LED Yamaha Exciter 155',
            'slug': 'den-pha-led-yamaha-exciter-155',
            'price': 850000,
            'discount': 10.0,
            'stock': 40,
            'status': 'active',
            'description': 'Đèn pha LED chính hãng Yamaha Exciter 155, độ sáng cao, tiết kiệm điện',
            'image_url': 'https://images.unsplash.com/photo-1449247666642-264389f5f5b1?w=800&q=80',
            'category_id': 3,
            'manufacture_year': 2024,
            'supplier': 'Yamaha Official'
        },
        {
            'id': 9,
            'name': 'Bình ắc quy GS GTZ7V 12V-6Ah',
            'slug': 'binh-ac-quy-gs-gtz7v-12v-6ah',
            'price': 380000,
            'discount': 5.0,
            'stock': 55,
            'status': 'active',
            'description': 'Bình ắc quy khô GS GTZ7V, dung lượng 12V-6Ah, tuổi thọ cao',
            'image_url': 'https://images.unsplash.com/photo-1609269069235-33c50c27a3cf?w=800&q=80',
            'category_id': 3,
            'manufacture_year': 2024,
            'supplier': 'GS Battery'
        },
        {
            'id': 10,
            'name': 'Đèn xi nhan LED Honda Wave RSX',
            'slug': 'den-xi-nhan-led-honda-wave-rsx',
            'price': 120000,
            'discount': 0,
            'stock': 80,
            'status': 'active',
            'description': 'Đèn xi nhan LED chính hãng Honda Wave RSX, thiết kế nhỏ gọn',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&hue=30',
            'category_id': 3,
            'manufacture_year': 2024,
            'supplier': 'Honda Official'
        },
        
        # Lốp xe (category_id = 4)
        {
            'id': 11,
            'name': 'Lốp Michelin Pilot Street 90/80-17',
            'slug': 'lop-michelin-pilot-street-90-80-17',
            'price': 680000,
            'discount': 8.0,
            'stock': 45,
            'status': 'active',
            'description': 'Lốp Michelin Pilot Street, kích thước 90/80-17, độ bám đường tốt, chống trượt',
            'image_url': 'https://images.unsplash.com/photo-1629870055365-e0ed3c0c49a2?w=800&q=80',
            'category_id': 4,
            'manufacture_year': 2024,
            'supplier': 'Michelin'
        },
        {
            'id': 12,
            'name': 'Lốp Dunlop D105 70/90-17',
            'slug': 'lop-dunlop-d105-70-90-17',
            'price': 420000,
            'discount': 10.0,
            'stock': 60,
            'status': 'active',
            'description': 'Lốp Dunlop D105, kích thước 70/90-17, phù hợp xe số',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&contrast=-50',
            'category_id': 4,
            'manufacture_year': 2024,
            'supplier': 'Dunlop'
        },
        {
            'id': 13,
            'name': 'Ruột xe Michelin 14 inch',
            'slug': 'ruot-xe-michelin-14-inch',
            'price': 85000,
            'discount': 0,
            'stock': 90,
            'status': 'active',
            'description': 'Ruột xe Michelin 14 inch, chất liệu cao su bền bỉ',
            'image_url': 'https://images.unsplash.com/photo-1629870055365-e0ed3c0c49a2?w=800&q=80&fit=crop',
            'category_id': 4,
            'manufacture_year': 2024,
            'supplier': 'Michelin'
        },
        
        # Yên xe và tay lái (category_id = 5)
        {
            'id': 14,
            'name': 'Yên độ Givi Honda Winner X',
            'slug': 'yen-do-givi-honda-winner-x',
            'price': 1250000,
            'discount': 15.0,
            'stock': 20,
            'status': 'active',
            'description': 'Yên độ Givi cao cấp cho Honda Winner X, chất liệu da cao cấp, êm ái',
            'image_url': 'https://images.unsplash.com/photo-1558980664-769d59546b3d?w=800&q=80',
            'category_id': 5,
            'manufacture_year': 2024,
            'supplier': 'Givi'
        },
        {
            'id': 15,
            'name': 'Tay lái racing Yamaha Exciter 155',
            'slug': 'tay-lai-racing-yamaha-exciter-155',
            'price': 580000,
            'discount': 10.0,
            'stock': 35,
            'status': 'active',
            'description': 'Tay lái racing cho Yamaha Exciter 155, chất liệu nhôm, trọng lượng nhẹ',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&hue=90',
            'category_id': 5,
            'manufacture_year': 2024,
            'supplier': 'Racing Boy'
        },
        {
            'id': 16,
            'name': 'Tay thắng Brembo RCS 19',
            'slug': 'tay-thang-brembo-rcs-19',
            'price': 3500000,
            'discount': 8.0,
            'stock': 10,
            'status': 'active',
            'description': 'Tay thắng Brembo RCS 19, chất liệu nhôm nguyên khối, điều chỉnh tỷ số',
            'image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80&hue=180',
            'category_id': 5,
            'manufacture_year': 2024,
            'supplier': 'Brembo'
        },
        
        # Pô và ống xả (category_id = 6)
        {
            'id': 17,
            'name': 'Pô Akrapovic Carbon Honda Winner X',
            'slug': 'po-akrapovic-carbon-honda-winner-x',
            'price': 4800000,
            'discount': 12.0,
            'stock': 15,
            'status': 'active',
            'description': 'Pô Akrapovic full carbon cho Honda Winner X, tăng công suất, giảm trọng lượng',
            'image_url': 'https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=800&q=80',
            'category_id': 6,
            'manufacture_year': 2024,
            'supplier': 'Akrapovic'
        },
        {
            'id': 18,
            'name': 'Pô Yoshimura R77 Yamaha Exciter 155',
            'slug': 'po-yoshimura-r77-yamaha-exciter-155',
            'price': 3200000,
            'discount': 10.0,
            'stock': 20,
            'status': 'active',
            'description': 'Pô Yoshimura R77 cho Yamaha Exciter 155, âm thanh trầm ấm',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&hue=210',
            'category_id': 6,
            'manufacture_year': 2024,
            'supplier': 'Yoshimura'
        },
        {
            'id': 19,
            'name': 'Bô chặn pô titan Racing Boy',
            'slug': 'bo-chan-po-titan-racing-boy',
            'price': 450000,
            'discount': 5.0,
            'stock': 40,
            'status': 'active',
            'description': 'Bô chặn pô titan Racing Boy, chống mài mòn, giảm ồn',
            'image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80&hue=240',
            'category_id': 6,
            'manufacture_year': 2024,
            'supplier': 'Racing Boy'
        },
        
        # Dầu nhớt (category_id = 7)
        {
            'id': 20,
            'name': 'Nhớt Castrol Power1 15W50',
            'slug': 'nhot-castrol-power1-15w50',
            'price': 280000,
            'discount': 10.0,
            'stock': 100,
            'status': 'active',
            'description': 'Dầu nhớt Castrol Power1 15W50, bán tổng hợp, bảo vệ động cơ tốt',
            'image_url': 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=800&q=80',
            'category_id': 7,
            'manufacture_year': 2024,
            'supplier': 'Castrol'
        },
        {
            'id': 21,
            'name': 'Nhớt Shell Advance AX7 10W40',
            'slug': 'nhot-shell-advance-ax7-10w40',
            'price': 195000,
            'discount': 8.0,
            'stock': 120,
            'status': 'active',
            'description': 'Dầu nhớt Shell Advance AX7 10W40, khoáng chất, phù hợp xe số',
            'image_url': 'https://images.unsplash.com/photo-1485291571150-772bcfc10da5?w=800&q=80&hue=60',
            'category_id': 7,
            'manufacture_year': 2024,
            'supplier': 'Shell'
        },
        {
            'id': 22,
            'name': 'Nhớt Liqui Moly Racing 10W60',
            'slug': 'nhot-liqui-moly-racing-10w60',
            'price': 550000,
            'discount': 5.0,
            'stock': 50,
            'status': 'active',
            'description': 'Dầu nhớt Liqui Moly Racing 10W60, tổng hợp 100%, cho xe đua',
            'image_url': 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=800&q=80&hue=120',
            'category_id': 7,
            'manufacture_year': 2024,
            'supplier': 'Liqui Moly'
        },
        
        # Phụ kiện trang trí (category_id = 8)
        {
            'id': 23,
            'name': 'Baga sau Givi Honda Winner X',
            'slug': 'baga-sau-givi-honda-winner-x',
            'price': 980000,
            'discount': 10.0,
            'stock': 30,
            'status': 'active',
            'description': 'Baga sau Givi cho Honda Winner X, chất liệu inox 304, tải trọng 5kg',
            'image_url': 'https://images.unsplash.com/photo-1609630875171-b1321377ee65?w=800&q=80',
            'category_id': 8,
            'manufacture_year': 2024,
            'supplier': 'Givi'
        },
        {
            'id': 24,
            'name': 'Kính chắn gió Puig Yamaha Exciter 155',
            'slug': 'kinh-chan-gio-puig-yamaha-exciter-155',
            'price': 1450000,
            'discount': 8.0,
            'stock': 25,
            'status': 'active',
            'description': 'Kính chắn gió Puig cho Yamaha Exciter 155, chất liệu acrylic, giảm gió hiệu quả',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&hue=300',
            'category_id': 8,
            'manufacture_year': 2024,
            'supplier': 'Puig'
        },
        {
            'id': 25,
            'name': 'Thùng đựng đồ Smart Box 32L',
            'slug': 'thung-dung-do-smart-box-32l',
            'price': 750000,
            'discount': 12.0,
            'stock': 40,
            'status': 'active',
            'description': 'Thùng đựng đồ Smart Box dung tích 32L, chất liệu nhựa ABS, khóa an toàn',
            'image_url': 'https://images.unsplash.com/photo-1609630875171-b1321377ee65?w=800&q=80&contrast=20',
            'category_id': 8,
            'manufacture_year': 2024,
            'supplier': 'Givi'
        },
        {
            'id': 26,
            'name': 'Gù giảm xóc Rizoma',
            'slug': 'gu-giam-xoc-rizoma',
            'price': 2800000,
            'discount': 10.0,
            'stock': 15,
            'status': 'active',
            'description': 'Gù giảm xóc Rizoma, chất liệu nhôm CNC, thiết kế thể thao',
            'image_url': 'https://images.unsplash.com/photo-1558980664-769d59546b3d?w=800&q=80&hue=150',
            'category_id': 8,
            'manufacture_year': 2024,
            'supplier': 'Rizoma'
        },
        {
            'id': 27,
            'name': 'Bảo vệ phuộc trước Carbon',
            'slug': 'bao-ve-phuoc-truoc-carbon',
            'price': 450000,
            'discount': 5.0,
            'stock': 35,
            'status': 'active',
            'description': 'Bảo vệ phuộc trước sợi carbon, nhẹ, bền, chống va đập',
            'image_url': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80&hue=270',
            'category_id': 8,
            'manufacture_year': 2024,
            'supplier': 'Racing Boy'
        }
    ]
    
    for motopart_data in motoparts_data:
        try:
            category = Category.objects.get(id=motopart_data['category_id'])
            motopart, created = Motopart.objects.get_or_create(
                id=motopart_data['id'],
                defaults={
                    'name': motopart_data['name'],
                    'slug': motopart_data['slug'],
                    'price': motopart_data['price'],
                    'discount': motopart_data['discount'],
                    'stock': motopart_data['stock'],
                    'status': motopart_data['status'],
                    'description': motopart_data['description'],
                    'image_url': motopart_data['image_url'],
                    'category': category,
                    'manufacture_year': motopart_data['manufacture_year'],
                    'supplier': motopart_data['supplier']
                }
            )
            if created:
                print(f"✓ Created motopart: {motopart.name}")
            else:
                print(f"• Motopart already exists: {motopart.name}")
        except Category.DoesNotExist:
            print(f"✗ Category with id {motopart_data['category_id']} not found for {motopart_data['name']}")

def print_summary():
    """Print import summary"""
    print("\n" + "="*60)
    print("IMPORT SUMMARY")
    print("="*60)
    print(f"Total categories: {Category.objects.count()}")
    print(f"Total motoparts: {Motopart.objects.count()}")
    print("\nMotoparts by category:")
    
    for category in Category.objects.all():
        count = category.motoparts.count() # type: ignore
        print(f"  {category.name}: {count} motoparts")
    
    print("="*60)
    print("Sample data import completed successfully! ✓")

def main():
    """Main import function"""
    print("EasyRead Motoparts - Sample Data Import")
    print("="*60)
    
    try:
        # Ask user if they want to clear existing data
        response = input("Do you want to clear existing data first? (y/N): ").lower().strip()
        if response in ['y', 'yes']:
            clear_existing_data()
        
        # Import data
        import_categories()
        import_motoparts()
        
        # Print summary
        print_summary()
        
    except Exception as e:
        print(f"✗ Error during import: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()