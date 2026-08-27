"""
FreshGuard AI — 35-Class Intelligent Shelf Life & Storage Rules Engine
Provides default storage locations, food categories, and estimated shelf-life rules
for all 35 FreshGuard Vision target classes.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional

CLASS_MAPPING_RULES: Dict[int, Dict[str, Any]] = {
    0: {"name": "milk", "display_name": "Milk", "category": "Dairy", "default_location": "Fridge", "shelf_life_days": 7},
    1: {"name": "bread", "display_name": "Bread", "category": "Bakery", "default_location": "Pantry", "shelf_life_days": 5},
    2: {"name": "apple", "display_name": "Apple", "category": "Fruits", "default_location": "Pantry", "shelf_life_days": 14},
    3: {"name": "banana", "display_name": "Banana", "category": "Fruits", "default_location": "Pantry", "shelf_life_days": 6},
    4: {"name": "egg", "display_name": "Egg", "category": "Dairy", "default_location": "Fridge", "shelf_life_days": 21},
    5: {"name": "tomato", "display_name": "Tomato", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 7},
    6: {"name": "potato", "display_name": "Potato", "category": "Vegetables", "default_location": "Pantry", "shelf_life_days": 30},
    7: {"name": "onion", "display_name": "Onion", "category": "Vegetables", "default_location": "Pantry", "shelf_life_days": 30},
    8: {"name": "rice", "display_name": "Rice", "category": "Grains", "default_location": "Pantry", "shelf_life_days": 180},
    9: {"name": "yogurt", "display_name": "Yogurt", "category": "Dairy", "default_location": "Fridge", "shelf_life_days": 10},
    10: {"name": "cheese", "display_name": "Cheese", "category": "Dairy", "default_location": "Fridge", "shelf_life_days": 14},
    11: {"name": "biscuit", "display_name": "Biscuit", "category": "Packaged Goods", "default_location": "Pantry", "shelf_life_days": 60},
    12: {"name": "juice", "display_name": "Juice", "category": "Beverages", "default_location": "Fridge", "shelf_life_days": 7},
    13: {"name": "water", "display_name": "Water", "category": "Beverages", "default_location": "Pantry", "shelf_life_days": 365},
    14: {"name": "packaged_snack", "display_name": "Packaged Snack", "category": "Packaged Goods", "default_location": "Pantry", "shelf_life_days": 90},
    15: {"name": "carrot", "display_name": "Carrot", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 14},
    16: {"name": "cabbage", "display_name": "Cabbage", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 14},
    17: {"name": "cauliflower", "display_name": "Cauliflower", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 7},
    18: {"name": "capsicum", "display_name": "Capsicum", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 7},
    19: {"name": "cucumber", "display_name": "Cucumber", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 7},
    20: {"name": "brinjal", "display_name": "Brinjal", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 5},
    21: {"name": "broccoli", "display_name": "Broccoli", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 5},
    22: {"name": "spinach", "display_name": "Spinach", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 4},
    23: {"name": "peas", "display_name": "Peas", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 5},
    24: {"name": "corn", "display_name": "Corn", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 5},
    25: {"name": "garlic", "display_name": "Garlic", "category": "Vegetables", "default_location": "Pantry", "shelf_life_days": 60},
    26: {"name": "ginger", "display_name": "Ginger", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 21},
    27: {"name": "okra", "display_name": "Okra", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 5},
    28: {"name": "beetroot", "display_name": "Beetroot", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 14},
    29: {"name": "radish", "display_name": "Radish", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 10},
    30: {"name": "pumpkin", "display_name": "Pumpkin", "category": "Vegetables", "default_location": "Pantry", "shelf_life_days": 30},
    31: {"name": "bitter_gourd", "display_name": "Bitter Gourd", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 5},
    32: {"name": "bottle_gourd", "display_name": "Bottle Gourd", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 7},
    33: {"name": "green_chilli", "display_name": "Green Chilli", "category": "Vegetables", "default_location": "Fridge", "shelf_life_days": 10},
    34: {"name": "sweet_potato", "display_name": "Sweet Potato", "category": "Vegetables", "default_location": "Pantry", "shelf_life_days": 21},
}

CLASS_NAME_TO_ID: Dict[str, int] = {rule["name"]: cid for cid, rule in CLASS_MAPPING_RULES.items()}

def get_class_rule(class_identifier: Any) -> Optional[Dict[str, Any]]:
    """
    Looks up rule dictionary by class ID (int) or class name (str).
    Returns None if class_identifier is unknown.
    """
    if isinstance(class_identifier, int):
        return CLASS_MAPPING_RULES.get(class_identifier)
    elif isinstance(class_identifier, str):
        cname = class_identifier.lower().strip()
        cid = CLASS_NAME_TO_ID.get(cname)
        if cid is not None:
            return CLASS_MAPPING_RULES.get(cid)
    return None

def calculate_estimated_expiry(class_identifier: Any, purchase_date: Optional[datetime] = None) -> datetime:
    """
    Calculates estimated expiration date based on 35-class rules.
    Defaults to purchase_date or now + default shelf life days (or 7 days if unknown).
    """
    base_date = purchase_date or datetime.utcnow()
    rule = get_class_rule(class_identifier)
    days = rule["shelf_life_days"] if rule else 7
    return base_date + timedelta(days=days)
