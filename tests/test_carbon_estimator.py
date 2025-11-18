"""Tests for the carbon estimator."""
import pytest
from backend.carbon_estimator import CarbonEstimator


class TestCarbonEstimator:
    """Test cases for CarbonEstimator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.estimator = CarbonEstimator()

    def test_estimate_locally_food_meat(self):
        """Test local estimation for meat products."""
        result = self.estimator._estimate_locally("food_meat", 100.0)
        assert result["carbon_kg"] > 0
        assert result["source"] == "local_estimate"
        assert result["confidence"] == "medium"
        assert "emission_factor" in result

    def test_estimate_locally_food_plant(self):
        """Test local estimation for plant-based food."""
        result = self.estimator._estimate_locally("food_plant", 100.0)
        assert result["carbon_kg"] > 0
        # Plant-based should have lower emissions than meat
        meat_result = self.estimator._estimate_locally("food_meat", 100.0)
        assert result["carbon_kg"] < meat_result["carbon_kg"]

    def test_estimate_locally_transportation_air(self):
        """Test local estimation for air travel."""
        result = self.estimator._estimate_locally("transportation_air", 100.0)
        assert result["carbon_kg"] > 0
        # Air travel should have high emissions
        assert result["carbon_kg"] > self.estimator._estimate_locally("food_plant", 100.0)["carbon_kg"]

    def test_estimate_locally_unknown_category(self):
        """Test local estimation with unknown category."""
        result = self.estimator._estimate_locally("unknown_category", 100.0)
        assert result["carbon_kg"] > 0
        assert result["emission_factor"] == 0.3  # Default factor

    def test_compare_alternatives_food_meat(self):
        """Test alternative comparison for meat products."""
        comparison = self.estimator.compare_alternatives("food_meat", 50.0)
        assert "alternative" in comparison
        assert "potential_reduction_kg" in comparison
        assert comparison["reduction_percent"] > 0
        assert comparison["potential_reduction_kg"] > 0

    def test_compare_alternatives_no_alternative(self):
        """Test comparison for category with no alternatives."""
        comparison = self.estimator.compare_alternatives("other", 50.0)
        assert comparison["alternative"] is None
        assert comparison["potential_reduction_kg"] == 0

    def test_compare_alternatives_transportation_air(self):
        """Test alternative comparison for air travel."""
        comparison = self.estimator.compare_alternatives("transportation_air", 200.0)
        assert comparison["alternative"] is not None
        assert comparison["reduction_percent"] >= 80
        assert comparison["potential_reduction_kg"] > 0
