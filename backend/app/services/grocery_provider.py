from abc import ABC, abstractmethod
from typing import List, Dict, Any

class GroceryProvider(ABC):
    """Abstract interface for future official grocery delivery platform integrations."""

    @abstractmethod
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_price(self, product_name: str) -> float:
        pass

    @abstractmethod
    def create_cart(self, household_id: int) -> str:
        pass

    @abstractmethod
    def add_to_cart(self, cart_id: str, product_name: str, quantity: float) -> bool:
        pass

    @abstractmethod
    def checkout(self, cart_id: str) -> Dict[str, Any]:
        pass

class MockGroceryProvider(GroceryProvider):
    """
    Development & Mock Grocery Provider implementation.
    Simulates price lookup and ordering workflow cleanly without calling unofficial APIs.
    """

    MOCK_PRICE_CATALOG = {
        "milk": 64.0,
        "amul taaza": 66.0,
        "bread": 45.0,
        "eggs": 75.0,
        "apples": 160.0,
        "bananas": 50.0,
        "cheese": 140.0,
        "tomatoes": 40.0,
        "rice": 120.0,
        "yogurt": 35.0
    }

    def search_products(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        results = []
        for name, price in self.MOCK_PRICE_CATALOG.items():
            if q in name:
                results.append({
                    "product_name": name.title(),
                    "price": price,
                    "provider": "Mock Fresh Express"
                })
        return results

    def get_price(self, product_name: str) -> float:
        q = product_name.lower()
        for key, price in self.MOCK_PRICE_CATALOG.items():
            if key in q:
                return price
        return 65.0 # default estimated price in INR

    def create_cart(self, household_id: int) -> str:
        return f"mock_cart_h{household_id}_2026"

    def add_to_cart(self, cart_id: str, product_name: str, quantity: float) -> bool:
        return True

    def checkout(self, cart_id: str) -> Dict[str, Any]:
        return {
            "status": "success",
            "message": "Mock Order successfully created. Explicit user approval recorded.",
            "order_id": f"ORD_{cart_id}_99",
            "provider": "Mock Grocery Provider"
        }
