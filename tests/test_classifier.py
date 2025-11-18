"""Tests for the transaction classifier."""
import pytest
from backend.classifier import TransactionClassifier


class TestTransactionClassifier:
    """Test cases for TransactionClassifier."""

    def setup_method(self):
        """Set up test fixtures."""
        self.classifier = TransactionClassifier()

    def test_classify_coffee_shop(self):
        """Test classification of coffee shop purchase."""
        category, confidence, carbon = self.classifier.classify("Starbucks Coffee", 6.75)
        assert category == "dining"
        assert confidence > 0
        assert carbon > 0

    def test_classify_gas_station(self):
        """Test classification of gas station purchase."""
        category, confidence, carbon = self.classifier.classify("Shell Gas Station", 45.00)
        assert category == "transportation_car"
        assert confidence > 0
        assert carbon > 0

    def test_classify_airline(self):
        """Test classification of airline purchase."""
        category, confidence, carbon = self.classifier.classify("United Airlines Flight", 350.00)
        assert category == "transportation_air"
        assert confidence > 0
        assert carbon > 0

    def test_classify_grocery_store(self):
        """Test classification of grocery store purchase."""
        category, confidence, carbon = self.classifier.classify("Whole Foods Market", 87.50)
        assert category == "food_plant"
        assert confidence > 0
        assert carbon > 0

    def test_classify_empty_description(self):
        """Test classification with empty description."""
        category, confidence, carbon = self.classifier.classify("", 10.00)
        assert category == "other"
        assert confidence == 0.0
        assert carbon == 0.0

    def test_classify_unknown_merchant(self):
        """Test classification of unknown merchant."""
        category, confidence, carbon = self.classifier.classify("Unknown Store ABC", 25.00)
        assert category == "other"
        assert confidence == 0.3
        assert carbon > 0

    def test_classify_without_amount(self):
        """Test classification without amount."""
        category, confidence, carbon = self.classifier.classify("Starbucks Coffee")
        assert category == "dining"
        assert confidence > 0
        assert carbon == 0.0

    def test_get_category_info(self):
        """Test getting category information."""
        info = self.classifier.get_category_info("food_meat")
        assert "carbon_per_dollar" in info
        assert "description" in info
        assert info["carbon_per_dollar"] > 0

    def test_get_all_categories(self):
        """Test getting all categories."""
        categories = self.classifier.get_all_categories()
        assert len(categories) > 0
        assert "food_meat" in categories
        assert "transportation_air" in categories
