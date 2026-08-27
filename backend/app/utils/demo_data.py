from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.models import User, Household, HouseholdMember, Inventory, ConsumptionLog, PurchaseHistory, Recommendation, Notification, UserPreference, ShoppingCart, ShoppingCartItem

def seed_demo_data():
    """
    Populates rich, realistic demo account data for FreshGuard AI.
    Demo Credentials:
    Email: demo@freshguard.ai
    Password: password123
    """
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if demo user already exists
        user = db.query(User).filter(User.email == "demo@freshguard.ai").first()
        if user:
            print("Demo data already seeded.")
            return

        # 1. Create Demo User & Household
        user = User(
            email="demo@freshguard.ai",
            password_hash=hash_password("password123"),
            full_name="Alex Morgan"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        pref = UserPreference(user_id=user.id, dark_mode=True)
        db.add(pref)

        household = Household(
            name="Morgan Family Kitchen",
            join_code="FG-DEMO26",
            owner_id=user.id
        )
        db.add(household)
        db.commit()
        db.refresh(household)

        member = HouseholdMember(household_id=household.id, user_id=user.id, role="owner")
        db.add(member)
        db.commit()

        now = datetime.utcnow()

        # 2. Populate Example Inventory (Milk, Bread, Apples, Bananas, Eggs, Cheese, Tomatoes, Rice, Yogurt)
        demo_items = [
            {
                "product_name": "Amul Taaza Toned Milk",
                "category": "Dairy",
                "brand": "Amul",
                "quantity": 0.5,
                "unit": "L",
                "storage_location": "Refrigerator",
                "expiry_date": now + timedelta(days=1), # Expiring Soon / Tomorrow
                "barcode": "8901058000147",
                "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300",
                "notes": "1/2 Litre remaining"
            },
            {
                "product_name": "Britannia Whole Wheat Bread",
                "category": "Bakery",
                "brand": "Britannia",
                "quantity": 1.0,
                "unit": "pack",
                "storage_location": "Pantry",
                "expiry_date": now + timedelta(days=2), # Expiring Soon
                "barcode": "8901262010056",
                "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"
            },
            {
                "product_name": "Fresh Red Apples",
                "category": "Fruits",
                "brand": "Orchard Fresh",
                "quantity": 2.0,
                "unit": "pcs",
                "storage_location": "Pantry",
                "expiry_date": now + timedelta(days=5),
                "barcode": "8901020030011",
                "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300"
            },
            {
                "product_name": "Organic Bananas 1 Dozen",
                "category": "Fruits",
                "brand": "Nature Best",
                "quantity": 6.0,
                "unit": "pcs",
                "storage_location": "Pantry",
                "expiry_date": now + timedelta(days=3),
                "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300"
            },
            {
                "product_name": "Farm Fresh Organic Eggs",
                "category": "Eggs",
                "brand": "EggFirst",
                "quantity": 3.0,
                "unit": "pcs",
                "storage_location": "Refrigerator",
                "expiry_date": now + timedelta(days=8),
                "barcode": "8901725111234",
                "image_url": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=300"
            },
            {
                "product_name": "Cheddar Cheese Block",
                "category": "Dairy",
                "brand": "Amul",
                "quantity": 1.0,
                "unit": "pack",
                "storage_location": "Refrigerator",
                "expiry_date": now + timedelta(days=12),
                "barcode": "8901058852319",
                "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=300"
            },
            {
                "product_name": "Fresh Tomatoes 1kg",
                "category": "Vegetables",
                "brand": "Local Farm",
                "quantity": 4.0,
                "unit": "pcs",
                "storage_location": "Refrigerator",
                "expiry_date": now + timedelta(days=2),
                "image_url": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300"
            },
            {
                "product_name": "Basmati Rice 5kg",
                "category": "Grains",
                "brand": "India Gate",
                "quantity": 3.5,
                "unit": "kg",
                "storage_location": "Kitchen Shelf",
                "expiry_date": now + timedelta(days=180),
                "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300"
            },
            {
                "product_name": "Greek Natural Yogurt",
                "category": "Dairy",
                "brand": "Epigamia",
                "quantity": 1.0,
                "unit": "cup",
                "storage_location": "Refrigerator",
                "expiry_date": now - timedelta(days=1), # Expired Item
                "barcode": "8901030000011",
                "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300"
            }
        ]

        inv_objects = []
        for item_data in demo_items:
            days = (item_data["expiry_date"] - now).days
            st = "Healthy"
            if days < 0:
                st = "Expired"
            elif days <= 2:
                st = "Expiring Soon"
            elif item_data["quantity"] <= 0.5:
                st = "Running Low"

            inv = Inventory(
                user_id=user.id,
                household_id=household.id,
                product_name=item_data["product_name"],
                category=item_data["category"],
                brand=item_data["brand"],
                quantity=item_data["quantity"],
                unit=item_data["unit"],
                storage_location=item_data["storage_location"],
                purchase_date=now - timedelta(days=4),
                expiry_date=item_data["expiry_date"],
                opened_date=now - timedelta(days=2),
                estimated_remaining_quantity=item_data["quantity"],
                barcode=item_data.get("barcode"),
                image_url=item_data.get("image_url"),
                notes=item_data.get("notes"),
                status=st
            )
            db.add(inv)
            inv_objects.append(inv)

        db.commit()

        # 3. Add Realistic Historical Consumption Logs for AI Model Learning
        # Simulates Milk consumption pattern: 1L every 2 days
        milk_inv = inv_objects[0]
        consumption_dates = [now - timedelta(days=i) for i in [7, 5, 3, 1]]
        for d in consumption_dates:
            log = ConsumptionLog(
                inventory_id=milk_inv.id,
                household_id=household.id,
                product_name="Amul Taaza Toned Milk",
                category="Dairy",
                quantity_consumed=1.0,
                unit="L",
                date_consumed=d,
                log_type="consumed"
            )
            db.add(log)

        # Bananas log
        db.add(ConsumptionLog(
            household_id=household.id,
            product_name="Organic Bananas 1 Dozen",
            category="Fruits",
            quantity_consumed=3.0,
            unit="pcs",
            date_consumed=now - timedelta(days=2),
            log_type="consumed"
        ))

        # Wasted Yogurt log
        db.add(ConsumptionLog(
            household_id=household.id,
            product_name="Greek Natural Yogurt",
            category="Dairy",
            quantity_consumed=1.0,
            unit="cup",
            date_consumed=now - timedelta(days=1),
            log_type="wasted",
            waste_value=35.0
        ))

        # 4. Generate Initial Recommendations & Smart Cart Items
        rec1 = Recommendation(
            household_id=household.id,
            product_name="Amul Taaza Toned Milk 1L",
            category="Dairy",
            suggested_quantity=1.0,
            unit="L",
            reason="Running Low (Predicted run-out tomorrow)",
            urgency="High",
            priority=1
        )
        rec2 = Recommendation(
            household_id=household.id,
            product_name="Britannia Whole Wheat Bread",
            category="Bakery",
            suggested_quantity=1.0,
            unit="pack",
            reason="Expiring in 2 days",
            urgency="Medium",
            priority=2
        )
        db.add(rec1)
        db.add(rec2)

        # Create Active Cart
        cart = ShoppingCart(household_id=household.id, total_estimated_price=109.0, status="active")
        db.add(cart)
        db.commit()
        db.refresh(cart)

        cart_item1 = ShoppingCartItem(
            cart_id=cart.id,
            product_name="Amul Taaza Toned Milk 1L",
            quantity=1.0,
            unit="L",
            estimated_price=64.0,
            reason="Running low (1 day remaining)",
            priority="Urgent"
        )
        cart_item2 = ShoppingCartItem(
            cart_id=cart.id,
            product_name="Britannia Whole Wheat Bread",
            quantity=1.0,
            unit="pack",
            estimated_price=45.0,
            reason="Weekly purchase pattern",
            priority="Normal"
        )
        db.add(cart_item1)
        db.add(cart_item2)

        # 5. Populate Notifications
        n1 = Notification(
            user_id=user.id,
            title="🥛 Milk Expiring Soon",
            message="Amul Taaza Toned Milk expires tomorrow.",
            type="expiry",
            priority="high"
        )
        n2 = Notification(
            user_id=user.id,
            title="🤖 FreshGuard AI Restock Alert",
            message="FreshGuard AI found 2 items that need restocking.",
            type="runout",
            priority="normal"
        )
        db.add(n1)
        db.add(n2)

        db.commit()
        print("Demo account successfully seeded! Log in with demo@freshguard.ai / password123")

    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
