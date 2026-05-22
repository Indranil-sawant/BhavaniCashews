import os
import urllib.request
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product, ProductGallery, ProductReview

# Helper function to download images
def download_image(url, filename, subdir='products'):
    os.makedirs(f'media/{subdir}', exist_ok=True)
    filepath = f'media/{subdir}/{filename}'
    if not os.path.exists(filepath):
        try:
            print(f"Downloading {url} to {filepath}...")
            # Set User-Agent to avoid HTTP 403 Forbidden
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Successfully downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            # Write a fallback blank file if download fails
            with open(filepath, 'wb') as out_file:
                out_file.write(b"")
    return f"{subdir}/{filename}"

# Image URLs from the static templates
IMG_MAIN_HERO = "https://lh3.googleusercontent.com/aida-public/AB6AXuD4mn7QQqtbcO5K8-68N_6MsX6yMZoVX3wjqQD8p58b8sHJzB-_ImtaoWTX2oWgWa3RFXipgwDdGHtdXIuml1TENvn1aSS8n513awCyW1xjsvMddD2-R0A9YnCjWHjhgycOhZeyDn1gFt6X8dU3SgrvdtPVGZkrT_SnQbH8TiRDTffTdCw2sDcSKf2FjEwghmA0dB1nKbfrU61uQkoCGaRleRNGEi5A1rypkt03iFPh4gEX-pme0mgSK_SaU3Oyfuy87y2qVpdbEco"
IMG_WHOLE_JAR = "https://lh3.googleusercontent.com/aida-public/AB6AXuDvp47-uThmEPoewIb4nHU6RWwQqkYy1ILziS2skA0B4vIBAcBu5FUIxpobY6AWDp50JBGKaIZpIAUb-XuFSA3OQsB_39XTye22WrB8i-upGQzgDnLp3AGx1Tdz69_iEY7Azq8nEAvXbyklcMb4hFNAzntyZrnoB_vUY47BrsBHdXA8RAYG3qE--XF57Q-yKO2y3W7mI02NIEGxDTHA95FvarxQO_fOrrJGRoRBG8DkLAmx_nU3ygtFrBjFIUQUm3czOBgwbJaFfaI"
IMG_FLAVORED_BOWLS = "https://lh3.googleusercontent.com/aida-public/AB6AXuC2CmvvWobgXjP7JLOwWXTcP_eOJr-aHkQUfWOyvrwBHnL1tlSm-IUDJwPaoOjaPczKJmnajd8nelI45jPeuBzOoR3yrt1MdNuqGY26xfKN7Log0ITk1J7pqEc5buR5FDl5fHjHGOoyjAFjvourwVJhrDy55C6cNX_cPLYRvuyo1C059X4KCc7GAqSwq90K-hPFRIRNMLv07k6SMTXr-7l_rHKISQYJ3tvYpjocdpmmMXOLlsclpkRqd7Z3xo4E2rtVBC5aOcfbeQY"
IMG_PIECES_SALAD = "https://lh3.googleusercontent.com/aida-public/AB6AXuBBo4JgSiF0QYaNYfSPg_IROA78E4_un2GlekakkmbyIp7LJJzJjMo8Yj1fGC3ggLqyN5AUFGuVl3kuF4o72203073-Ykwb_qvG8aZIPq9jLFJAJEtVOuSxYOUw4JlDVNnH50fTDJDEh3c5jPiE7z7ljWQ2APcfqnEm3BZX0gej6izGKmXuiZgPLRRIb3ISlzI4AGasVpnH4qI_-9HWEDoFSLdRea1NNfuv9QrdeRPSq3_iHbd8diBmk22wvYYxNfveoQl3KNv44lQ"
IMG_BULK_SACKS = "https://lh3.googleusercontent.com/aida-public/AB6AXuDQBbtbNBuismyVHC2LGgnpuYkZttB_hP5mG5xm2i-p9voX7TBq4Woe5on_EOE-Fpum_UTa1mYlrbR1Q1vIStUWVhE9-B5m6PPl1rHBSbFZIn0uwjKB05oiDLljoJSfTXfuB1gg-3y-B6uFQ-fJhjovnxeAod8mI6uK9WRaexEHhPDfAFv-tQi410utCz9TMnEfGUChhCNMApUoO3rs33WaA9FUtC1PG5Iu5lW-1CI1kGyxduZdTYEc1jN29vS13D8jIynO3au754U"
IMG_ARTISAN_HANDS = "https://lh3.googleusercontent.com/aida-public/AB6AXuAFTVDbNWjwQbdaT6BBjcuGXf8SJ4EXHWXomYy71kNVwBaaPwVmVXAT8yHds8M0EuShQxSiqSG_j6yqnkR-1HUdPTcAywzXqdzDD4vhCfNiTy5RK3ZBxE0BCeo_S8INyKINLL-6AY2OaTOhs5zMRhf8lh14YVCceSnHk2RyP_i8Cbk4sm5eFLmhSAPbtlu3rrAqJ6LnhmfmlnOML80Ozzc--J4j1fjk46xqeFBwSLOmp9sG19ABOaVLmljBNPjoy53GFS56UGNuzR8"

# 1. Clear existing products & categories to start fresh
Product.objects.all().delete()
Category.objects.all().delete()

print("Database cleared.")

# 2. Download Category images & create Categories
cat_img_roasted = download_image(IMG_WHOLE_JAR, "slow_roasted_category.jpg", "categories")
cat_img_raw = download_image(IMG_ARTISAN_HANDS, "raw_organic_category.jpg", "categories")
cat_img_flavored = download_image(IMG_FLAVORED_BOWLS, "flavored_infusions_category.jpg", "categories")
cat_img_bulk = download_image(IMG_BULK_SACKS, "wholesale_bulk_category.jpg", "categories")

cat_roasted = Category.objects.create(
    name="Slow-Roasted",
    description="Carefully roasted at optimal temperatures to bring out a deep, buttery gold profile.",
    image=cat_img_roasted,
    is_active=True
)

cat_raw = Category.objects.create(
    name="Raw Organic",
    description="Handpicked ivory kernels in their purest form, packed with natural nutrients.",
    image=cat_img_raw,
    is_active=True
)

cat_flavored = Category.objects.create(
    name="Flavored Infusions",
    description="Artisanal flavor profiles from honey-glazed to chili-lime infusions.",
    image=cat_img_flavored,
    is_active=True
)

cat_bulk = Category.objects.create(
    name="Wholesale Bulk",
    description="Exquisite grades for gourmet kitchens and premium global export partners.",
    image=cat_img_bulk,
    is_active=True
)

print("Categories created successfully!")

# 3. Download Product images & create Products
img_w320 = download_image(IMG_WHOLE_JAR, "premium_w320.jpg", "products")
img_w320_sec = download_image(IMG_MAIN_HERO, "premium_w320_sec.jpg", "products")

img_jumbo = download_image(IMG_ARTISAN_HANDS, "organic_jumbo.jpg", "products")
img_jumbo_sec = download_image(IMG_WHOLE_JAR, "organic_jumbo_sec.jpg", "products")

img_himalayan = download_image(IMG_FLAVORED_BOWLS, "himalayan_roasted.jpg", "products")
img_himalayan_sec = download_image(IMG_MAIN_HERO, "himalayan_roasted_sec.jpg", "products")

img_chili = download_image(IMG_FLAVORED_BOWLS, "chili_lime.jpg", "products")
img_chili_sec = download_image(IMG_PIECES_SALAD, "chili_lime_sec.jpg", "products")

img_honey = download_image(IMG_MAIN_HERO, "honey_butter.jpg", "products")
img_honey_sec = download_image(IMG_FLAVORED_BOWLS, "honey_butter_sec.jpg", "products")

img_w180 = download_image(IMG_BULK_SACKS, "export_w180.jpg", "products")
img_w180_sec = download_image(IMG_WHOLE_JAR, "export_w180_sec.jpg", "products")

p1 = Product.objects.create(
    category=cat_roasted,
    name="Premium W320 Whole Cashews",
    short_description="Selected for immaculate white color and consistent sizing, medium roasted.",
    description="Our flagship product. Medium Amber roast, selected for immaculate white color and consistent sizing. Perfect for daily snacking or gifting, preserving the natural oils and buttery flavor profiles perfected over 40 years.",
    price=24.99,
    stock=120,
    minimum_order_quantity=1,
    image=img_w320,
    secondary_image=img_w320_sec,
    is_featured=True,
    is_available=True,
    sku="CAS-W320-500",
    weight=500.00
)

p2 = Product.objects.create(
    category=cat_raw,
    name="Organic Jumbo Raw Cashews",
    short_description="Unrivaled size and purity. Certified organic raw cashew kernels.",
    description="Unrivaled size and purity. Certified organic raw cashew kernels, hand-cracked and gently dehydrated to preserve active enzymes and creamy textures. Packed with vitamins and heart-healthy fats.",
    price=34.50,
    stock=45,
    minimum_order_quantity=1,
    image=img_jumbo,
    secondary_image=img_jumbo_sec,
    is_featured=True,
    is_available=True,
    sku="CAS-RAW-JMB",
    weight=1000.00
)

p3 = Product.objects.create(
    category=cat_roasted,
    name="Himalayan Pink Salt Roasted Cashews",
    short_description="Crispy golden hue and dusted with finely ground Himalayan Pink Salt.",
    description="Slow-roasted to a crispy golden hue and dusted with finely ground Himalayan Pink Salt. Subtle saltiness accentuates the cashew's natural sweet profile, making it a delicious, low-sodium savory snack.",
    price=18.00,
    stock=85,
    minimum_order_quantity=1,
    image=img_himalayan,
    secondary_image=img_himalayan_sec,
    is_featured=True,
    is_available=True,
    sku="CAS-HIM-ROAST",
    weight=250.00
)

p4 = Product.objects.create(
    category=cat_flavored,
    name="Chili Lime Sizzler Cashews",
    short_description="Zesty Mexican lime and fiery birds-eye chili infusion.",
    description="Zesty Mexican lime and fiery birds-eye chili infusion. An exquisite culinary pairing designed for sophisticated palates. Adds a gourmet kick to salads, cheese platters, and fine drinks.",
    price=15.99,
    stock=60,
    minimum_order_quantity=1,
    image=img_chili,
    secondary_image=img_chili_sec,
    is_featured=False,
    is_available=True,
    sku="CAS-CHILI-LIME",
    weight=250.00
)

p5 = Product.objects.create(
    category=cat_flavored,
    name="Honey Butter Glazed Cashews",
    short_description="Glazed in sweet clover honey and organic creamery butter.",
    description="Glazed in sweet clover honey and organic creamery butter. A delicate crispy coating with a highly addictive sweet-savory finish, slow baked in small artisanal batches.",
    price=16.50,
    stock=70,
    minimum_order_quantity=1,
    image=img_honey,
    secondary_image=img_honey_sec,
    is_featured=False,
    is_available=True,
    sku="CAS-HONEY-BUTTER",
    weight=250.00
)

p6 = Product.objects.create(
    category=cat_bulk,
    name="Export Grade W180 Giant Cashews",
    short_description="The King of Cashews. Exceptionally rich flavor and massive size.",
    description="The 'King of Cashews'. W180 is the largest whole grade available in the global market. Exceptionally rich flavor and texture, reserved for global exports and premium confectioneries.",
    price=145.00,
    stock=15,
    minimum_order_quantity=1,
    image=img_w180,
    secondary_image=img_w180_sec,
    is_featured=True,
    is_available=True,
    sku="CAS-EXP-W180",
    weight=5000.00
)

print("Products created successfully!")

# 4. Create Product Gallery Images
ProductGallery.objects.create(product=p1, image=img_w320_sec)
ProductGallery.objects.create(product=p1, image=img_w320)
ProductGallery.objects.create(product=p2, image=img_jumbo_sec)
ProductGallery.objects.create(product=p3, image=img_himalayan_sec)

print("Gallery images created!")

# 5. Create Reviews
ProductReview.objects.create(product=p1, name="Sophia Sterling", rating=5, review="Absolutely premium. The crunch and flavor are unmatched. Buying another pack immediately!")
ProductReview.objects.create(product=p1, name="Arthur Pendelton", rating=5, review="Excellent white whole grade. Beautifully packaged, feels very luxury.")
ProductReview.objects.create(product=p1, name="Markus Vance", rating=4, review="Very buttery and roasted exactly to perfection. Minor delay in shipping but well worth the wait.")
ProductReview.objects.create(product=p2, name="Elena Rostova", rating=5, review="These jumbo raw cashews are huge! Super rich, creamy, and perfect for raw vegan sauces.")
ProductReview.objects.create(product=p3, name="Chef Julian", rating=5, review="Subtle saltiness that elevates the natural sweetness of the cashew. Excellent product.")

print("Reviews created!")
print("Database seeding completed successfully!")
