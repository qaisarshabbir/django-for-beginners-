import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import (
    Category, 
    Brand, 
    Supplier, 
    Products, 
    ProductDetail
)

class Command(BaseCommand):
    help = 'Seeds the database with dummy data for categories, brands, suppliers, products, and product details.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database seeding...')

        # 1. Create 100 Categories
        self.stdout.write('Creating categories...')
        categories = []
        category_types = ['Electronics', 'Home & Kitchen', 'Apparel', 'Sports', 'Beauty', 'Books', 'Toys', 'Automotive', 'Health', 'Garden']
        for i in range(1, 101):
            name = f"{random.choice(category_types)} Item Type {i}"
            base_slug = slugify(name)
            slug = f"{base_slug}-{i}"
            
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': f"Explore our wide collection of high-quality {name}.",
                    'is_active': True
                }
            )
            categories.append(category)

        # 2. Create 100 Brands
        self.stdout.write('Creating brands...')
        brands = []
        brand_names = ['Apex', 'Nova', 'Vortex', 'Zenith', 'Prime', 'Pioneer', 'Echo', 'Omni', 'Fusion', 'Titan']
        for i in range(1, 101):
            name = f"{random.choice(brand_names)} Brand {i}"
            brand, _ = Brand.objects.get_or_create(
                name=name,
                defaults={
                    'description': f"Official products manufactured by {name}.",
                    'is_active': True
                }
            )
            brands.append(brand)

        # 3. Create 50 Suppliers
        self.stdout.write('Creating suppliers...')
        suppliers = []
        for i in range(1, 51):
            code = f"SUP-{i:03d}"
            supplier, _ = Supplier.objects.get_or_create(
                supplier_code=code,
                defaults={
                    'company_name': f"Global Distribution Corp {i}",
                    'phone': f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    'email': f"contact.supplier{i}@example.com",
                    'address': f"{i}00 Industrial Parkway, Suite {i}, Commerce City"
                }
            )
            suppliers.append(supplier)

        # 4. Create 500 Products
        self.stdout.write('Creating products...')
        products = []
        statuses = ["DF", "PB", "OOS"]
        product_adjectives = ['Smart', 'Pro', 'Ultra', 'Portable', 'Wireless', 'Ergonomic', 'Advanced', 'Heavy-Duty']
        product_nouns = ['Widget', 'Device', 'Appliance', 'Kit', 'Tool', 'System', 'Gadget', 'Unit']

        for i in range(1, 501):
            sku = f"SKU{i:05d}"
            name = f"{random.choice(product_adjectives)} {random.choice(product_nouns)} {i}"
            
            product, created = Products.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'description': f"High-performance {name} designed for durability and efficiency. Ideal for everyday use.",
                    'price': round(random.uniform(9.99, 999.99), 2),
                    'status': random.choices(statuses, weights=[10, 75, 15], k=1)[0],
                    'category': random.choice(categories),
                    'brand': random.choice(brands),
                }
            )
            
            if created:
                # Assign 1 to 3 random suppliers to the product's ManyToMany field
                assigned_suppliers = random.sample(suppliers, k=random.randint(1, 3))
                product.suppliers.set(assigned_suppliers)
                
            products.append(product)

        # 5. Create 400 Product Details (Linked to the first 400 products)
        self.stdout.write('Creating product details...')
        materials = ['Aluminum', 'Plastic', 'Stainless Steel', 'Carbon Fiber', 'Silicone', 'Wood', 'Glass']
        
        # Get products that don't have details yet
        products_without_details = [p for p in products if not hasattr(p, 'details')][:400]
        
        detail_count = 0
        for product in products_without_details:
            ProductDetail.objects.get_or_create(
                product=product,
                defaults={
                    'weight_kg': round(random.uniform(0.05, 15.0), 2),
                    'dimensions': f"{random.randint(5, 40)} x {random.randint(5, 40)} x {random.randint(2, 20)} cm",
                    'warranty_months': random.choice([0, 6, 12, 24, 36]),
                    'material': random.choice(materials),
                    'care_instructions': "Wipe clean with a dry cloth. Avoid exposure to extreme moisture."
                }
            )
            detail_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded:\n"
            f"- {len(categories)} Categories\n"
            f"- {len(brands)} Brands\n"
            f"- {len(suppliers)} Suppliers\n"
            f"- {len(products)} Products\n"
            f"- {detail_count} Product Details"
        ))