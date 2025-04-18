from app.db.database import engine
from app.db.base import Base
from app.models.user import User, Role
from app.models.pricing_rule import PricingRule
from app.models.inventory import InventoryEntry
from app.models.product import Product
from app.models.alert import Alert

# import any other models here

def init():
    print("🛠️ Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables are ready!")

if __name__ == "__main__":
    init()
