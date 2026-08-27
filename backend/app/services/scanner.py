import requests
from typing import Optional
from app.schemas.schemas import BarcodeLookupResponse

# Local curated barcode lookup database fallback for offline/demo reliability
LOCAL_PRODUCT_DATABASE = {
    "8901058000147": {
        "product_name": "Amul Taaza Toned Milk 1L",
        "brand": "Amul",
        "category": "Dairy",
        "default_unit": "L",
        "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300"
    },
    "8901058852319": {
        "product_name": "Amul Pasteurised Butter 100g",
        "brand": "Amul",
        "category": "Dairy",
        "default_unit": "g",
        "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=300"
    },
    "8901262010056": {
        "product_name": "Britannia Whole Wheat Bread",
        "brand": "Britannia",
        "category": "Bakery",
        "default_unit": "pack",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"
    },
    "8901725111234": {
        "product_name": "Farm Fresh Organic Eggs 6 Pack",
        "brand": "EggFirst",
        "category": "Eggs",
        "default_unit": "pack",
        "image_url": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=300"
    },
    "8901030000011": {
        "product_name": "Greek Natural Yogurt 400g",
        "brand": "Epigamia",
        "category": "Dairy",
        "default_unit": "g",
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300"
    },
    "8901020030011": {
        "product_name": "Fresh Red Apples 1kg",
        "brand": "Orchard Fresh",
        "category": "Fruits",
        "default_unit": "kg",
        "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300"
    }
}

def lookup_barcode(barcode: str) -> BarcodeLookupResponse:
    cleaned = barcode.strip()
    
    # 1. Check local lookup dictionary first
    if cleaned in LOCAL_PRODUCT_DATABASE:
        item = LOCAL_PRODUCT_DATABASE[cleaned]
        return BarcodeLookupResponse(
            found=True,
            barcode=cleaned,
            product_name=item["product_name"],
            brand=item["brand"],
            category=item["category"],
            default_unit=item["default_unit"],
            image_url=item.get("image_url")
        )
    
    # 2. Query official Open Food Facts API
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{cleaned}.json"
        res = requests.get(url, timeout=3.5)
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == 1:
                p = data.get("product", {})
                name = p.get("product_name") or p.get("product_name_en") or "Unknown Product"
                brand = p.get("brands") or "Generic"
                categories = p.get("categories", "")
                cat = "Other"
                if "dairy" in categories.lower() or "milk" in name.lower():
                    cat = "Dairy"
                elif "fruit" in categories.lower():
                    cat = "Fruits"
                elif "vegetable" in categories.lower():
                    cat = "Vegetables"
                elif "bakery" in categories.lower() or "bread" in name.lower():
                    cat = "Bakery"
                elif "beverage" in categories.lower() or "drink" in categories.lower():
                    cat = "Beverages"
                
                img = p.get("image_front_small_url") or p.get("image_url")
                
                return BarcodeLookupResponse(
                    found=True,
                    barcode=cleaned,
                    product_name=name,
                    brand=brand,
                    category=cat,
                    default_unit="pcs",
                    image_url=img
                )
    except Exception:
        pass
    
    # If not found, return clean not found response allowing user manual entry
    return BarcodeLookupResponse(
        found=False,
        barcode=cleaned
    )
