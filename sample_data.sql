-- ============================================================
-- EasyRead Motoparts - Sample Data SQL Script (MySQL Version)
-- ============================================================
-- This script inserts sample data for categories and motoparts
-- Run with: mysql -u username -p database_name < sample_data.sql
-- ============================================================

-- Clear existing data (optional - comment out if you want to keep existing data)
-- DELETE FROM motopart_motopart;
-- DELETE FROM category_category;

-- ============================================================
-- CATEGORIES
-- ============================================================

REPLACE INTO category_category (id, name, slug, image, created_at, updated_at) VALUES
(1, 'Phụ tùng động cơ', 'phu-tung-dong-co', 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800', NOW(), NOW()),
(2, 'Phụ tùng phanh', 'phu-tung-phanh', 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800', NOW(), NOW()),
(3, 'Đèn và điện', 'den-va-dien', 'https://images.unsplash.com/photo-1449247666642-264389f5f5b1?w=800', NOW(), NOW()),
(4, 'Lốp xe', 'lop-xe', 'https://images.unsplash.com/photo-1629870055365-e0ed3c0c49a2?w=800', NOW(), NOW()),
(5, 'Yên xe và tay lái', 'yen-xe-va-tay-lai', 'https://images.unsplash.com/photo-1558980664-769d59546b3d?w=800', NOW(), NOW()),
(6, 'Pô và ống xả', 'po-va-ong-xa', 'https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=800', NOW(), NOW()),
(7, 'Dầu nhớt', 'dau-nhot', 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=800', NOW(), NOW()),
(8, 'Phụ kiện trang trí', 'phu-kien-trang-tri', 'https://images.unsplash.com/photo-1609630875171-b1321377ee65?w=800', NOW(), NOW());

-- ============================================================
-- MOTOPARTS - Phụ tùng động cơ (category_id = 1)
-- ============================================================

REPLACE INTO motopart_motopart
(id, name, slug, price, discount, stock, status, description, image_url, category_id, manufacture_year, supplier, created_at, updated_at)
VALUES
(1, 'Piston Honda Wave 110 STD', 'piston-honda-wave-110-std', 250000, 10.0, 50, 'active',
 'Piston chính hãng Honda Wave 110, kích thước chuẩn STD, chất liệu hợp kim nhôm cao cấp, độ bền cao',
 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80', 1, 2024, 'Honda Official', NOW(), NOW()),

(2, 'Nhớt động cơ Motul 7100 10W40', 'nhot-dong-co-motul-7100-10w40', 320000, 5.0, 100, 'active',
 'Dầu nhớt tổng hợp 100% Motul 7100, độ nhớt 10W40, phù hợp động cơ 4 thì',
 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=800&q=80', 1, 2024, 'Motul', NOW(), NOW()),

(3, 'Lọc gió động cơ Yamaha Exciter 150', 'loc-gio-dong-co-yamaha-exciter-150', 85000, 0, 75, 'active',
 'Lọc gió động cơ chính hãng Yamaha Exciter 150, chất liệu lọc cao cấp',
 'https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=800&q=80', 1, 2024, 'Yamaha Official', NOW(), NOW()),

(4, 'Xích nhông dĩa Honda Winner X', 'xich-nhong-dia-honda-winner-x', 450000, 15.0, 30, 'active',
 'Bộ xích nhông dĩa chính hãng Honda Winner X, độ bền cao, giảm ồn tốt',
 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&fit=crop', 1, 2024, 'Honda Official', NOW(), NOW());

-- ============================================================
-- MOTOPARTS - Phụ tùng phanh (category_id = 2)
-- ============================================================

REPLACE INTO motopart_motopart
(id, name, slug, price, discount, stock, status, description, image_url, category_id, manufacture_year, supplier, created_at, updated_at)
VALUES
(5, 'Má phanh trước Yamaha NVX 155', 'ma-phanh-truoc-yamaha-nvx-155', 180000, 8.0, 60, 'active',
 'Má phanh đĩa trước chính hãng Yamaha NVX 155, lực phanh tốt, ít bụi',
 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80', 2, 2024, 'Yamaha Official', NOW(), NOW()),

(6, 'Dầu phanh Motul DOT 4', 'dau-phanh-motul-dot-4', 95000, 0, 120, 'active',
 'Dầu phanh Motul DOT 4, điểm sôi cao, chống ăn mòn hệ thống phanh',
 'https://images.unsplash.com/photo-1485291571150-772bcfc10da5?w=800&q=80', 2, 2024, 'Motul', NOW(), NOW()),

(7, 'Đĩa phanh trước Honda Winner X', 'dia-phanh-truoc-honda-winner-x', 550000, 12.0, 25, 'active',
 'Đĩa phanh trước chính hãng Honda Winner X, đường kính 296mm, chất liệu thép không gỉ',
 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&sat=-100', 2, 2024, 'Honda Official', NOW(), NOW());

-- ============================================================
-- MOTOPARTS - Đèn và điện (category_id = 3)
-- ============================================================

REPLACE INTO motopart_motopart
(id, name, slug, price, discount, stock, status, description, image_url, category_id, manufacture_year, supplier, created_at, updated_at)
VALUES
(8, 'Đèn pha LED Yamaha Exciter 155', 'den-pha-led-yamaha-exciter-155', 850000, 10.0, 40, 'active',
 'Đèn pha LED chính hãng Yamaha Exciter 155, độ sáng cao, tiết kiệm điện',
 'https://images.unsplash.com/photo-1449247666642-264389f5f5b1?w=800&q=80', 3, 2024, 'Yamaha Official', NOW(), NOW()),

(9, 'Bình ắc quy GS GTZ7V 12V-6Ah', 'binh-ac-quy-gs-gtz7v-12v-6ah', 380000, 5.0, 55, 'active',
 'Bình ắc quy khô GS GTZ7V, dung lượng 12V-6Ah, tuổi thọ cao',
 'https://images.unsplash.com/photo-1609269069235-33c50c27a3cf?w=800&q=80', 3, 2024, 'GS Battery', NOW(), NOW()),

(10, 'Đèn xi nhan LED Honda Wave RSX', 'den-xi-nhan-led-honda-wave-rsx', 120000, 0, 80, 'active',
 'Đèn xi nhan LED chính hãng Honda Wave RSX, thiết kế nhỏ gọn',
 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&hue=30', 3, 2024, 'Honda Official', NOW(), NOW());

-- ============================================================
-- MOTOPARTS - Lốp xe (category_id = 4)
-- ============================================================

REPLACE INTO motopart_motopart
(id, name, slug, price, discount, stock, status, description, image_url, category_id, manufacture_year, supplier, created_at, updated_at)
VALUES
(11, 'Lốp Michelin Pilot Street 90/80-17', 'lop-michelin-pilot-street-90-80-17', 680000, 8.0, 45, 'active',
 'Lốp Michelin Pilot Street, kích thước 90/80-17, độ bám đường tốt, chống trượt',
 'https://images.unsplash.com/photo-1629870055365-e0ed3c0c49a2?w=800&q=80', 4, 2024, 'Michelin', NOW(), NOW()),

(12, 'Lốp Dunlop D105 70/90-17', 'lop-dunlop-d105-70-90-17', 420000, 10.0, 60, 'active',
 'Lốp Dunlop D105, kích thước 70/90-17, phù hợp xe số',
 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&contrast=-50', 4, 2024, 'Dunlop', NOW(), NOW()),

(13, 'Ruột xe Michelin 14 inch', 'ruot-xe-michelin-14-inch', 85000, 0, 90, 'active',
 'Ruột xe Michelin 14 inch, chất liệu cao su bền bỉ',
 'https://images.unsplash.com/photo-1629870055365-e0ed3c0c49a2?w=800&q=80&fit=crop', 4, 2024, 'Michelin', NOW(), NOW());

-- ============================================================
-- MOTOPARTS - Yên xe và tay lái (category_id = 5)
-- ============================================================

REPLACE INTO motopart_motopart
(id, name, slug, price, discount, stock, status, description, image_url, category_id, manufacture_year, supplier, created_at, updated_at)
VALUES
(14, 'Yên độ Givi Honda Winner X', 'yen-do-givi-honda-winner-x', 1250000, 15.0, 20, 'active',
 'Yên độ Givi cao cấp cho Honda Winner X, chất liệu da cao cấp, êm ái',
 'https://images.unsplash.com/photo-1558980664-769d59546b3d?w=800&q=80', 5, 2024, 'Givi', NOW(), NOW()),

(15, 'Tay lái racing Yamaha Exciter 155', 'tay-lai-racing-yamaha-exciter-155', 580000, 10.0, 35, 'active',
 'Tay lái racing cho Yamaha Exciter 155, chất liệu nhôm, trọng lượng nhẹ',
 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&hue=90', 5, 2024, 'Racing Boy', NOW(), NOW()),

(16, 'Tay thắng Brembo RCS 19', 'tay-thang-brembo-rcs-19', 3500000, 8.0, 10, 'active',
 'Tay thắng Brembo RCS 19, chất liệu nhôm nguyên khối, điều chỉnh tỷ số',
 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80&hue=180', 5, 2024, 'Brembo', NOW(), NOW());

-- ============================================================
-- MOTOPARTS - Pô và ống xả (category_id = 6)
-- ============================================================

REPLACE INTO motopart_motopart
(id, name, slug, price, discount, stock, status, description, image_url, category_id, manufacture_year, supplier, created_at, updated_at)
VALUES
(17, 'Pô Akrapovic Carbon Honda Winner X', 'po-akrapovic-carbon-honda-winner-x', 4800000, 12.0, 15, 'active',
 'Pô Akrapovic full carbon cho Honda Winner X, tăng công suất, giảm trọng lượng',
 'https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=800&q=80', 6, 2024, 'Akrapovic', NOW(), NOW()),

(18, 'Pô Yoshimura R77 Yamaha Exciter 155', 'po-yoshimura-r77-yamaha-exciter-155', 3200000, 10.0, 20, 'active',
 'Pô Yoshimura R77 cho Yamaha Exciter 155, âm thanh trầm ấm',
 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&hue=210', 6, 2024, 'Yoshimura', NOW(), NOW()),

(19, 'Bô chặn pô titan Racing Boy', 'bo-chan-po-titan-racing-boy', 450000, 5.0, 40, 'active',
 'Bô chặn pô titan Racing Boy, chống mài mòn, giảm ồn',
 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80&hue=240', 6, 2024, 'Racing Boy', NOW(), NOW());

-- ============================================================
-- MOTOPARTS - Dầu nhớt (category_id = 7)
-- ============================================================

REPLACE INTO motopart_motopart
(id, name, slug, price, discount, stock, status, description, image_url, category_id, manufacture_year, supplier, created_at, updated_at)
VALUES
(20, 'Nhớt Castrol Power1 15W50', 'nhot-castrol-power1-15w50', 280000, 10.0, 100, 'active',
 'Dầu nhớt Castrol Power1 15W50, bán tổng hợp, bảo vệ động cơ tốt',
 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=800&q=80', 7, 2024, 'Castrol', NOW(), NOW()),

(21, 'Nhớt Shell Advance AX7 10W40', 'nhot-shell-advance-ax7-10w40', 195000, 8.0, 120, 'active',
 'Dầu nhớt Shell Advance AX7 10W40, khoáng chất, phù hợp xe số',
 'https://images.unsplash.com/photo-1485291571150-772bcfc10da5?w=800&q=80&hue=60', 7, 2024, 'Shell', NOW(), NOW()),

(22, 'Nhớt Liqui Moly Racing 10W60', 'nhot-liqui-moly-racing-10w60', 550000, 5.0, 50, 'active',
 'Dầu nhớt Liqui Moly Racing 10W60, tổng hợp 100%, cho xe đua',
 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?w=800&q=80&hue=120', 7, 2024, 'Liqui Moly', NOW(), NOW());

-- ============================================================
-- MOTOPARTS - Phụ kiện trang trí (category_id = 8)
-- ============================================================

REPLACE INTO motopart_motopart
(id, name, slug, price, discount, stock, status, description, image_url, category_id, manufacture_year, supplier, created_at, updated_at)
VALUES
(23, 'Baga sau Givi Honda Winner X', 'baga-sau-givi-honda-winner-x', 980000, 10.0, 30, 'active',
 'Baga sau Givi cho Honda Winner X, chất liệu inox 304, tải trọng 5kg',
 'https://images.unsplash.com/photo-1609630875171-b1321377ee65?w=800&q=80', 8, 2024, 'Givi', NOW(), NOW()),

(24, 'Kính chắn gió Puig Yamaha Exciter 155', 'kinh-chan-gio-puig-yamaha-exciter-155', 1450000, 8.0, 25, 'active',
 'Kính chắn gió Puig cho Yamaha Exciter 155, chất liệu acrylic, giảm gió hiệu quả',
 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80&hue=300', 8, 2024, 'Puig', NOW(), NOW()),

(25, 'Thùng đựng đồ Smart Box 32L', 'thung-dung-do-smart-box-32l', 750000, 12.0, 40, 'active',
 'Thùng đựng đồ Smart Box dung tích 32L, chất liệu nhựa ABS, khóa an toàn',
 'https://images.unsplash.com/photo-1609630875171-b1321377ee65?w=800&q=80&contrast=20', 8, 2024, 'Givi', NOW(), NOW()),

(26, 'Gù giảm xóc Rizoma', 'gu-giam-xoc-rizoma', 2800000, 10.0, 15, 'active',
 'Gù giảm xóc Rizoma, chất liệu nhôm CNC, thiết kế thể thao',
 'https://images.unsplash.com/photo-1558980664-769d59546b3d?w=800&q=80&hue=150', 8, 2024, 'Rizoma', NOW(), NOW()),

(27, 'Bảo vệ phuộc trước Carbon', 'bao-ve-phuoc-truoc-carbon', 450000, 5.0, 35, 'active',
 'Bảo vệ phuộc trước sợi carbon, nhẹ, bền, chống va đập',
 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&q=80&hue=270', 8, 2024, 'Racing Boy', NOW(), NOW());

-- ============================================================
-- Reset AUTO_INCREMENT (MySQL)
-- ============================================================
-- Uncomment if you need to reset AUTO_INCREMENT counters
-- ALTER TABLE category_category AUTO_INCREMENT = 9;
-- ALTER TABLE motopart_motopart AUTO_INCREMENT = 28;

-- ============================================================
-- Verification queries
-- ============================================================
-- SELECT COUNT(*) as total_categories FROM category_category;
-- SELECT COUNT(*) as total_motoparts FROM motopart_motopart;
-- SELECT c.name, COUNT(m.id) as motoparts_count
-- FROM category_category c
-- LEFT JOIN motopart_motopart m ON c.id = m.category_id
-- GROUP BY c.id, c.name;
