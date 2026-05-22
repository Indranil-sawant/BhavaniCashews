import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category
print("Categories:", Category.objects.count())
print("Products:", Product.objects.count())
for p in Product.objects.all():
    print(f"- {p.name} (${p.price}) [Featured: {p.is_featured}]")
