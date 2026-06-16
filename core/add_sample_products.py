"""
Run once to add sample products to database.
python core/add_sample_products.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grwmvs_project.settings')
django.setup()

from core.models import Product

products = [
    # MALE EYEWEAR
    dict(name='Aviator Sunglasses', category='face',  gender='male',   brand='RayBan',   price=2499, trend_score=95, trend_label='#1 Trending'),
    dict(name='Wayfarer Frames',    category='face',  gender='male',   brand='RayBan',   price=1999, trend_score=88, trend_label='Classic'),
    dict(name='Sport Goggles',      category='face',  gender='male',   brand='Nike',     price=1499, trend_score=75, trend_label='Streetwear'),
    dict(name='Round Metal Frames', category='face',  gender='male',   brand='Fastrack', price=999,  trend_score=70, trend_label='Vintage'),
    # FEMALE EYEWEAR
    dict(name='Cat Eye Sunglasses', category='face',  gender='female', brand='Vogue',    price=2299, trend_score=96, trend_label='#1 Trending'),
    dict(name='Oversized Frames',   category='face',  gender='female', brand='Gucci',    price=3499, trend_score=85, trend_label='Y2K Style'),
    dict(name='Tinted Lenses',      category='face',  gender='female', brand='Zara',     price=1799, trend_score=80, trend_label='Hot Pick'),
    dict(name='Butterfly Frames',   category='face',  gender='female', brand='H&M',      price=1299, trend_score=72, trend_label='New Arrival'),
    # MALE NECK
    dict(name='Gold Cuban Chain',   category='neck',  gender='male',   brand='Tanishq',  price=4999, trend_score=92, trend_label='#1 Trending'),
    dict(name='Silver Dog Tag',     category='neck',  gender='male',   brand='Fossil',   price=1499, trend_score=78, trend_label='Streetwear'),
    dict(name='Rope Chain',         category='neck',  gender='male',   brand='CaratLane',price=3499, trend_score=72, trend_label='Classic'),
    # FEMALE NECK
    dict(name='Pearl Necklace',     category='neck',  gender='female', brand='Tanishq',  price=5999, trend_score=94, trend_label='#1 Trending'),
    dict(name='Diamond Pendant',    category='neck',  gender='female', brand='Malabar',  price=8999, trend_score=90, trend_label='Luxury'),
    dict(name='Layered Gold Chain', category='neck',  gender='female', brand='CaratLane',price=4499, trend_score=85, trend_label='Hot Pick'),
    # MALE TOPS
    dict(name='Oversized Tee',      category='chest', gender='male',   brand='H&M',      price=799,  trend_score=96, trend_label='#1 Trending'),
    dict(name='Linen Shirt',        category='chest', gender='male',   brand='Zara',     price=1499, trend_score=85, trend_label='Smart Casual'),
    dict(name='Bomber Jacket',      category='chest', gender='male',   brand='Jack&Jones',price=2999,trend_score=88, trend_label='Streetwear'),
    dict(name='Polo Shirt',         category='chest', gender='male',   brand='Lacoste',  price=2499, trend_score=75, trend_label='Classic'),
    # FEMALE TOPS
    dict(name='Crop Top',           category='chest', gender='female', brand='H&M',      price=699,  trend_score=97, trend_label='#1 Trending'),
    dict(name='Off Shoulder Blouse',category='chest', gender='female', brand='Zara',     price=1299, trend_score=88, trend_label='Chic'),
    dict(name='Denim Jacket',       category='chest', gender='female', brand='Levis',    price=2499, trend_score=82, trend_label='Classic'),
    dict(name='Floral Kurti',       category='chest', gender='female', brand='Libas',    price=899,  trend_score=78, trend_label='Ethnic'),
    # MALE LEGS
    dict(name='Slim Fit Jeans',     category='legs',  gender='male',   brand='Levis',    price=1999, trend_score=95, trend_label='#1 Trending'),
    dict(name='Cargo Shorts',       category='legs',  gender='male',   brand='H&M',      price=999,  trend_score=82, trend_label='Streetwear'),
    dict(name='Chino Pants',        category='legs',  gender='male',   brand='Zara',     price=1799, trend_score=78, trend_label='Smart Casual'),
    dict(name='Athletic Joggers',   category='legs',  gender='male',   brand='Nike',     price=1499, trend_score=85, trend_label='Sporty'),
    # FEMALE LEGS
    dict(name='High Waist Jeans',   category='legs',  gender='female', brand='Levis',    price=2199, trend_score=96, trend_label='#1 Trending'),
    dict(name='Mini Skirt',         category='legs',  gender='female', brand='Zara',     price=1299, trend_score=88, trend_label='Y2K Style'),
    dict(name='Wide Leg Pants',     category='legs',  gender='female', brand='H&M',      price=1499, trend_score=82, trend_label='Chic'),
    # MALE FEET
    dict(name='Air Force Sneakers', category='feet',  gender='male',   brand='Nike',     price=7999, trend_score=98, trend_label='#1 Trending'),
    dict(name='Leather Loafers',    category='feet',  gender='male',   brand='Clarks',   price=4999, trend_score=80, trend_label='Smart'),
    dict(name='High Top Boots',     category='feet',  gender='male',   brand='Timberland',price=8999,trend_score=85, trend_label='Streetwear'),
    dict(name='Sport Slippers',     category='feet',  gender='male',   brand='Adidas',   price=1499, trend_score=75, trend_label='Casual'),
    # FEMALE FEET
    dict(name='Block Heels',        category='feet',  gender='female', brand='Steve Madden',price=3999,trend_score=94,trend_label='#1 Trending'),
    dict(name='Platform Sneakers',  category='feet',  gender='female', brand='Nike',     price=5999, trend_score=88, trend_label='Y2K Style'),
    dict(name='Ballet Flats',       category='feet',  gender='female', brand='Clarks',   price=2499, trend_score=80, trend_label='Elegant'),
]

Product.objects.all().delete()
for p in products:
    Product.objects.create(**p)
    print(f"Added: {p['name']}")

print(f"\n✅ {len(products)} products added to database!")