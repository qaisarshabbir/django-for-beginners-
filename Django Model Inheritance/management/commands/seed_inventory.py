# Install faker if you haven't already
# pip install faker

# Basic run — 400 products, 10 categories
# python manage.py seed_inventory

# Custom product count
# python manage.py seed_inventory --products 200

# Wipe existing data first, then re-seed
# python manage.py seed_inventory --clear

import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker

from products.models import Category, Brand, Unit, Product

User = get_user_model()
fake = Faker()


CATEGORIES = [
    ("Electronics", "Smartphones, laptops, accessories and gadgets"),
    ("Office Supplies", "Stationery, furniture, and office essentials"),
    ("Raw Materials", "Industrial inputs and manufacturing materials"),
    ("Packaging", "Boxes, bags, wrapping, and shipping materials"),
    ("Chemicals", "Cleaning agents, solvents, and industrial chemicals"),
    ("Food & Beverages", "Consumables, snacks, and drinks"),
    ("Machinery Parts", "Spare parts, tools, and mechanical components"),
    ("Safety Equipment", "PPE, helmets, gloves, and safety gear"),
    ("Furniture", "Desks, chairs, shelves, and storage units"),
    ("IT Equipment", "Servers, networking gear, and peripherals"),
]

UNITS = [
    ("Piece", "pcs"),
    ("Kilogram", "kg"),
    ("Gram", "g"),
    ("Liter", "L"),
    ("Milliliter", "mL"),
    ("Meter", "m"),
    ("Box", "box"),
    ("Carton", "ctn"),
    ("Dozen", "dz"),
    ("Pair", "pr"),
]

BRANDS = [
    "TechPro", "GlobalSupply", "PrimeParts", "SwiftGoods", "AlphaStore",
    "NovaBrand", "CoreTech", "PeakLine", "ZenithCo", "BridgeWorks",
    "FusionCraft", "OmniSource", "TrueValue", "NexGen", "SolidBase",
]

PRODUCT_TYPES = ["stock", "service", "digital"]


class Command(BaseCommand):
    help = "Seed inventory with 10 categories and 400 products"

    def add_arguments(self, parser):
        parser.add_argument(
            "--products", type=int, default=400,
            help="Number of products to create (default: 400)"
        )
        parser.add_argument(
            "--clear", action="store_true",
            help="Clear existing inventory data before seeding"
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing inventory data...")
            Product.objects.all().delete()
            Category.objects.all().delete()
            Brand.objects.all().delete()
            Unit.objects.all().delete()
            self.stdout.write(self.style.WARNING("  Cleared all inventory records."))

        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write(self.style.ERROR(
                "No superuser found. Create one first with: python manage.py createsuperuser"
            ))
            return

        categories = self._seed_categories(user)
        brands = self._seed_brands()
        units = self._seed_units()
        self._seed_products(options["products"], categories, brands, units, user)

        self.stdout.write(self.style.SUCCESS(
            f"\n✔ Seeding complete: "
            f"{len(categories)} categories, {len(brands)} brands, "
            f"{len(units)} units, {options['products']} products."
        ))

    # ------------------------------------------------------------------ #
    #  Seeders
    # ------------------------------------------------------------------ #

    def _seed_categories(self, user):
        self.stdout.write("Seeding categories...")
        categories = []

        for name, description in CATEGORIES:
            slug = self._unique_slug(Category, name)
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": description,
                    "is_active": True,
                    "created_by": user,
                },
            )
            categories.append(cat)
            status = "created" if created else "exists"
            self.stdout.write(f"  [{status}] {cat.name}")

        return categories

    def _seed_brands(self):
        self.stdout.write("Seeding brands...")
        brands = []

        for name in BRANDS:
            brand, created = Brand.objects.get_or_create(
                name=name,
                defaults={
                    "description": fake.sentence(nb_words=10),
                    "is_active": True,
                },
            )
            brands.append(brand)

        self.stdout.write(f"  {len(brands)} brands ready.")
        return brands

    def _seed_units(self):
        self.stdout.write("Seeding units...")
        units = []

        for name, short_name in UNITS:
            unit, created = Unit.objects.get_or_create(
                short_name=short_name,
                defaults={
                    "name": name,
                    "is_active": True,
                },
            )
            units.append(unit)

        self.stdout.write(f"  {len(units)} units ready.")
        return units

    def _seed_products(self, count, categories, brands, units, user):
        self.stdout.write(f"Seeding {count} products...")
        created_count = 0

        for i in range(count):
            product_name = self._unique_product_name()
            slug = self._unique_slug(Product, product_name)
            sku = self._unique_sku()

            cost_price = Decimal(str(round(random.uniform(10, 5000), 2)))
            selling_price = cost_price * Decimal(str(round(random.uniform(1.1, 2.5), 2)))
            wholesale_price = cost_price * Decimal(str(round(random.uniform(1.05, 1.5), 2)))
            current_stock = Decimal(str(random.randint(100, 5000)))
            minimum_stock = Decimal(str(random.randint(5, 50)))
            maximum_stock = minimum_stock * Decimal(str(random.randint(5, 20)))
            reorder_level = minimum_stock * Decimal("1.5")

            Product.objects.create(
                sku=sku,
                barcode=self._unique_barcode(),
                name=product_name,
                slug=slug,
                short_description=fake.sentence(nb_words=12),
                description=fake.paragraph(nb_sentences=4),
                category=random.choice(categories),
                brand=random.choice(brands + [None]),   # brand is optional
                unit=random.choice(units),
                tax=None,                                # extend if Tax records exist
                product_type=random.choice(PRODUCT_TYPES),
                cost_price=cost_price.quantize(Decimal("0.01")),
                selling_price=selling_price.quantize(Decimal("0.01")),
                wholesale_price=wholesale_price.quantize(Decimal("0.01")),
                current_stock=current_stock,
                minimum_stock=minimum_stock,
                maximum_stock=maximum_stock,
                reorder_level=reorder_level,
                weight=Decimal(str(round(random.uniform(0.1, 50), 2))),
                length=Decimal(str(round(random.uniform(1, 200), 2))),
                width=Decimal(str(round(random.uniform(1, 200), 2))),
                height=Decimal(str(round(random.uniform(1, 200), 2))),
                is_featured=random.random() < 0.15,
                is_active=random.random() < 0.90,
                allow_backorder=random.random() < 0.20,
                has_serial_number=random.random() < 0.30,
                has_expiry_date=random.random() < 0.25,
                notes=fake.sentence() if random.random() < 0.4 else "",
                created_by=user,
            )
            created_count += 1

            if created_count % 50 == 0:
                self.stdout.write(f"  ...{created_count}/{count} products created")

        self.stdout.write(f"  {created_count} products created.")

    # ------------------------------------------------------------------ #
    #  Helpers
    # ------------------------------------------------------------------ #

    def _unique_slug(self, model, name):
        base = slugify(name)
        slug = base
        n = 1
        while model.objects.filter(slug=slug).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    def _unique_product_name(self):
        adjectives = ["Premium", "Heavy-Duty", "Compact", "Industrial", "Standard",
                      "Professional", "Economy", "Advanced", "Ultra", "Classic"]
        nouns = ["Widget", "Module", "Component", "Unit", "Kit", "Set",
                 "Panel", "Pack", "Tool", "Device", "Cartridge", "Assembly"]
        return f"{random.choice(adjectives)} {fake.word().capitalize()} {random.choice(nouns)}"

    def _unique_sku(self):
        while True:
            sku = f"SKU-{fake.bothify('??##-####').upper()}"
            if not Product.objects.filter(sku=sku).exists():
                return sku

    def _unique_barcode(self):
        while True:
            barcode = fake.ean(length=13)
            if not Product.objects.filter(barcode=barcode).exists():
                return barcode
