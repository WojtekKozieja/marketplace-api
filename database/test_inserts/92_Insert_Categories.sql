-- migrate:up

TRUNCATE TABLE public.subcategories RESTART IDENTITY CASCADE;
TRUNCATE TABLE public.categories RESTART IDENTITY CASCADE;

INSERT INTO public.categories (category_name) VALUES
('Electronics'),
('Vehicles'),
('Real Estate'),
('Home & Garden'),
('Fashion'),
('Sports & Hobby'),
('Health & Beauty'),
('Books & Media'),
('Kids'),
('Pets');

INSERT INTO public.subcategories (category_id, subcategory_name) VALUES
-- Electronics (1)
(1, 'Phones'),
(1, 'Computers'),
(1, 'TV & Audio'),
(1, 'Gaming'),
(1, 'Accessories'),
(1, 'Other Electronics'),

-- Vehicles (2)
(2, 'Cars'),
(2, 'Motorcycles'),
(2, 'Trucks'),
(2, 'Parts'),
(2, 'Other Vehicles'),

-- Real Estate (3)
(3, 'Apartments'),
(3, 'Houses'),
(3, 'Rooms'),
(3, 'Land'),
(3, 'Commercial'),
(3, 'Other Real Estate'),

-- Home & Garden (4)
(4, 'Furniture'),
(4, 'Appliances'),
(4, 'Garden'),
(4, 'Decor'),
(4, 'Tools'),
(4, 'Other Home & Garden'),

-- Fashion (5)
(5, 'Men Clothing'),
(5, 'Women Clothing'),
(5, 'Shoes'),
(5, 'Accessories'),
(5, 'Watches'),
(5, 'Other Fashion'),

-- Sports & Hobby (6)
(6, 'Fitness'),
(6, 'Cycling'),
(6, 'Outdoor'),
(6, 'Music'),
(6, 'Collectibles'),
(6, 'Other Sports & Hobby'),

-- Health & Beauty (7)
(7, 'Skincare'),
(7, 'Makeup'),
(7, 'Perfumes'),
(7, 'Hair Care'),
(7, 'Supplements'),
(7, 'Other Health & Beauty'),

-- Books & Media (8)
(8, 'Books'),
(8, 'Movies & TV'),
(8, 'Music & Vinyl'),
(8, 'Video Games'),
(8, 'Other Media'),

-- Kids (9)
(9, 'Toys'),
(9, 'Clothing'),
(9, 'Strollers'),
(9, 'Furniture'),
(9, 'Other Kids'),

-- Pets (10)
(10, 'Dogs'),
(10, 'Cats'),
(10, 'Fish'),
(10, 'Accessories'),
(10, 'Other Pets');


-- migrate:down

TRUNCATE TABLE public.subcategories RESTART IDENTITY CASCADE;
TRUNCATE TABLE public.categories RESTART IDENTITY CASCADE;
