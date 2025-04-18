from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.product import Product
from app.models.user import User, Role
from app.models.inventory import InventoryEntry
from app.models.pricing_rule import PricingRule
from app.models.alert import Alert
from datetime import datetime, timedelta
import random
import bcrypt

# Create a session
db = SessionLocal()

# Seed Users
def create_users():
    roles_to_create = ["admin", "user"]
    for role_name in roles_to_create:
        existing = db.query(Role).filter_by(name=role_name).first()
        if not existing:
            new_role = Role(name=role_name)
            db.add(new_role)
    db.commit()
    db.commit()

    # Create admin user
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    admin_user = User(
        username="admin",
        email="admin@example.com",
        password=bcrypt.hashpw("adminpassword".encode(), bcrypt.gensalt()).decode(),
        role_id=admin_role.id,
        is_active=True,
    )
    db.add(admin_user)

    # Create regular user
    user_role = db.query(Role).filter(Role.name == "user").first()
    regular_user = User(
        username="user",
        email="user@example.com",
        password=bcrypt.hashpw("userpassword".encode(), bcrypt.gensalt()).decode(),
        role_id=user_role.id,
        is_active=True,
    )
    db.add(regular_user)
    db.commit()

# Seed Products
def create_products():
    for i in range(10):
        product = Product(
            name=f"Product-{i}",
            description=f"Description of product-{i}",
            stock=random.randint(10, 100),
            expiration_date=datetime.utcnow() + timedelta(days=random.randint(1, 30)),
            price=random.randint(100, 1000),
        )
        db.add(product)
    db.commit()

# Seed Inventory Entries
def create_inventory_entries():
    products = db.query(Product).all()
    for product in products:
        inventory_entry = InventoryEntry(
            product_id=product.id,
            quantity=random.randint(10, 100),
            added_at=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
        )
        db.add(inventory_entry)
    db.commit()

# Seed Pricing Rules
def create_pricing_rules():
    products = db.query(Product).all()
    for product in products:
        pricing_rule = PricingRule(
            product_id=product.id,
            price_change_percentage=random.randint(5, 20),
            applies_before_expiration=datetime.utcnow() + timedelta(days=random.randint(1, 15)),
        )
        db.add(pricing_rule)
    db.commit()

# Seed Alerts
def create_alerts():
    low_stock_products = db.query(Product).filter(Product.stock <= 10).all()
    for product in low_stock_products:
        alert = Alert(
            product_id=product.id,
            alert_type="Low Stock",
            message=f"Product '{product.name}' has low stock ({product.stock})",
            created_at=datetime.utcnow(),
        )
        db.add(alert)
    db.commit()

# Run all seeding functions
def seed_all():
    create_users()
    create_products()
    create_inventory_entries()
    create_pricing_rules()
    create_alerts()
    print("Seeding completed.")

if __name__ == "__main__":
    seed_all()
    db.close()
