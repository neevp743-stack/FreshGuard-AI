from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="USER", nullable=False, index=True) # USER, ADMIN
    created_at = Column(DateTime, default=datetime.utcnow)

    memberships = relationship("HouseholdMember", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    device_tokens = relationship("DeviceToken", back_populates="user", cascade="all, delete-orphan")

class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    join_code = Column(String, unique=True, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("HouseholdMember", back_populates="household", cascade="all, delete-orphan")
    inventory_items = relationship("Inventory", back_populates="household", cascade="all, delete-orphan")
    carts = relationship("ShoppingCart", back_populates="household", cascade="all, delete-orphan")

class HouseholdMember(Base):
    __tablename__ = "household_members"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="member") # owner, member

    household = relationship("Household", back_populates="members")
    user = relationship("User", back_populates="memberships")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, index=True, nullable=True)
    product_name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    category = Column(String, nullable=False, default="Other")
    default_unit = Column(String, default="pcs")
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    product_name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, default="Other", index=True)
    brand = Column(String, nullable=True)
    quantity = Column(Float, nullable=False, default=1.0)
    unit = Column(String, nullable=False, default="pcs")
    storage_location = Column(String, nullable=False, default="Pantry") # Refrigerator, Freezer, Pantry, Shelf, Other
    purchase_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True, index=True)
    opened_date = Column(DateTime, nullable=True)
    estimated_remaining_quantity = Column(Float, nullable=True)
    barcode = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String, default="Healthy") # Healthy, Expiring Soon, Expired, Running Low
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    household = relationship("Household", back_populates="inventory_items")
    consumption_logs = relationship("ConsumptionLog", back_populates="inventory", cascade="all, delete-orphan")

class ConsumptionLog(Base):
    __tablename__ = "consumption_logs"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id", ondelete="SET NULL"), nullable=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    quantity_consumed = Column(Float, nullable=False)
    unit = Column(String, default="pcs")
    date_consumed = Column(DateTime, default=datetime.utcnow, index=True)
    log_type = Column(String, default="consumed") # consumed, wasted, expired, donated
    waste_value = Column(Float, default=0.0) # estimated monetary loss if wasted

    inventory = relationship("Inventory", back_populates="consumption_logs")

class PurchaseHistory(Base):
    __tablename__ = "purchase_history"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False, default="Other")
    quantity = Column(Float, nullable=False, default=1.0)
    unit = Column(String, default="pcs")
    price = Column(Float, default=0.0)
    purchase_date = Column(DateTime, default=datetime.utcnow)

class ExpiryEvent(Base):
    __tablename__ = "expiry_events"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    product_name = Column(String, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False) # Urgent, Soon, Expired
    alert_sent_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, default="expiry") # EXPIRING_SOON, EXPIRED, RUNNING_LOW, REORDER_RECOMMENDATION, AI_INSIGHT
    priority = Column(String, default="normal") # urgent, high, normal, low
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

class DeviceToken(Base):
    __tablename__ = "device_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, index=True, nullable=False)
    platform = Column(String, default="android") # android, ios, web
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="device_tokens")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, default="Other")
    suggested_quantity = Column(Float, default=1.0)
    unit = Column(String, default="pcs")
    reason = Column(String, nullable=False)
    urgency = Column(String, default="Medium") # High, Medium, Low
    priority = Column(Integer, default=1)
    added_to_cart = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ShoppingCart(Base):
    __tablename__ = "shopping_cart"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    total_estimated_price = Column(Float, default=0.0)
    status = Column(String, default="active") # active, confirmed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    household = relationship("Household", back_populates="carts")
    items = relationship("ShoppingCartItem", back_populates="cart", cascade="all, delete-orphan")

class ShoppingCartItem(Base):
    __tablename__ = "shopping_cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("shopping_cart.id"), nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Float, default=1.0)
    unit = Column(String, default="pcs")
    estimated_price = Column(Float, default=0.0)
    reason = Column(String, nullable=True)
    priority = Column(String, default="Normal")
    confirmed = Column(Boolean, default=False)

    cart = relationship("ShoppingCart", back_populates="items")

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    dark_mode = Column(Boolean, default=True)
    notification_days_before = Column(Integer, default=3)
    expiry_alert_enabled = Column(Boolean, default=True)
    runout_alert_enabled = Column(Boolean, default=True)
