"""
NLP-based transaction classifier for categorizing purchases.
"""
from typing import Dict, Tuple
import re


class TransactionClassifier:
    """
    Classifies transactions into carbon-relevant categories.
    Uses keyword matching and pattern recognition for fast, offline classification.
    """

    # Category definitions with keywords and average carbon intensity (kg CO2 per $)
    CATEGORIES = {
        "food_meat": {
            "keywords": ["beef", "steak", "burger", "meat", "chicken", "pork", "lamb", "butcher"],
            "carbon_per_dollar": 0.8,
            "description": "Meat and animal products"
        },
        "food_plant": {
            "keywords": ["vegetable", "fruit", "salad", "vegan", "organic", "produce", "grocery"],
            "carbon_per_dollar": 0.2,
            "description": "Plant-based foods"
        },
        "transportation_air": {
            "keywords": ["airline", "flight", "airport", "airways", "jetblue", "united", "delta"],
            "carbon_per_dollar": 2.5,
            "description": "Air travel"
        },
        "transportation_car": {
            "keywords": ["gas", "fuel", "shell", "chevron", "exxon", "petrol", "diesel"],
            "carbon_per_dollar": 1.2,
            "description": "Car fuel and transportation"
        },
        "transportation_public": {
            "keywords": ["metro", "subway", "bus", "train", "transit", "uber", "lyft", "taxi"],
            "carbon_per_dollar": 0.3,
            "description": "Public transportation and rideshare"
        },
        "energy": {
            "keywords": ["electric", "electricity", "power", "utility", "gas bill", "energy"],
            "carbon_per_dollar": 0.9,
            "description": "Home energy and utilities"
        },
        "retail_clothing": {
            "keywords": ["clothing", "fashion", "apparel", "zara", "h&m", "nike", "adidas"],
            "carbon_per_dollar": 0.6,
            "description": "Clothing and fashion"
        },
        "retail_electronics": {
            "keywords": ["electronics", "apple", "samsung", "computer", "phone", "laptop", "best buy"],
            "carbon_per_dollar": 0.7,
            "description": "Electronics and gadgets"
        },
        "retail_general": {
            "keywords": ["amazon", "walmart", "target", "store", "retail", "shop"],
            "carbon_per_dollar": 0.4,
            "description": "General retail"
        },
        "services": {
            "keywords": ["subscription", "streaming", "netflix", "spotify", "service"],
            "carbon_per_dollar": 0.1,
            "description": "Digital services"
        },
        "dining": {
            "keywords": ["restaurant", "cafe", "coffee", "starbucks", "mcdonald", "pizza", "dining"],
            "carbon_per_dollar": 0.5,
            "description": "Dining and restaurants"
        },
        "other": {
            "keywords": [],
            "carbon_per_dollar": 0.3,
            "description": "Uncategorized purchases"
        }
    }

    def __init__(self):
        """Initialize the classifier."""
        self.categories = self.CATEGORIES

    def classify(self, description: str, amount: float = None) -> Tuple[str, float, float]:
        """
        Classify a transaction based on its description.

        Args:
            description: Transaction description text
            amount: Transaction amount in dollars

        Returns:
            Tuple of (category, confidence_score, estimated_carbon_kg)
        """
        if not description:
            return "other", 0.0, 0.0

        description_lower = description.lower()
        best_match = "other"
        best_score = 0.0

        # Check each category for keyword matches
        for category, data in self.CATEGORIES.items():
            if category == "other":
                continue

            score = 0
            for keyword in data["keywords"]:
                if keyword in description_lower:
                    # Longer keywords get higher scores
                    score += len(keyword) / 10.0 + 1.0

            # Normalize score
            if data["keywords"]:
                normalized_score = min(score / len(data["keywords"]), 1.0)
                if normalized_score > best_score:
                    best_score = normalized_score
                    best_match = category

        # If no match found, use "other" category
        if best_score == 0.0:
            best_match = "other"
            best_score = 0.3  # Low confidence for uncategorized

        # Estimate carbon footprint
        carbon_kg = 0.0
        if amount:
            carbon_per_dollar = self.CATEGORIES[best_match]["carbon_per_dollar"]
            carbon_kg = amount * carbon_per_dollar

        return best_match, best_score, carbon_kg

    def get_category_info(self, category: str) -> Dict:
        """Get information about a specific category."""
        return self.CATEGORIES.get(category, self.CATEGORIES["other"])

    def get_all_categories(self) -> Dict:
        """Get all available categories."""
        return {
            cat: data["description"]
            for cat, data in self.CATEGORIES.items()
        }
