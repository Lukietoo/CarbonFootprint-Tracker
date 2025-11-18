"""
Carbon emission estimator using Climatiq API.
"""
import httpx
from typing import Dict, Optional
from backend.config import settings


class CarbonEstimator:
    """
    Estimates carbon emissions using the Climatiq API.
    Falls back to local estimates if API is unavailable.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the carbon estimator.

        Args:
            api_key: Climatiq API key (optional, uses settings if not provided)
        """
        self.api_key = api_key or settings.climatiq_api_key
        self.base_url = settings.climatiq_base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def estimate_from_category(
        self,
        category: str,
        amount: float,
        unit: str = "usd"
    ) -> Dict:
        """
        Estimate carbon emissions for a purchase.

        Args:
            category: Purchase category
            amount: Purchase amount
            unit: Currency unit (default: USD)

        Returns:
            Dictionary with carbon estimate and metadata
        """
        # Mapping of our categories to Climatiq activity IDs
        category_mapping = {
            "food_meat": "consumer_goods-type_meat_products_beef",
            "food_plant": "consumer_goods-type_vegetables",
            "transportation_air": "passenger_flight-route_type_domestic-aircraft_type_jet",
            "transportation_car": "fuel_type_motor_gasoline",
            "transportation_public": "passenger_train-route_type_local",
            "energy": "electricity-energy_source_grid_mix",
            "retail_clothing": "consumer_goods-type_clothing",
            "retail_electronics": "consumer_goods-type_electrical_equipment",
            "retail_general": "consumer_goods-type_other",
            "services": "services-type_other",
            "dining": "consumer_goods-type_food_products",
        }

        # Try using Climatiq API if key is available
        if self.api_key and self.api_key != "your_climatiq_api_key":
            try:
                result = await self._estimate_via_api(category, amount, category_mapping)
                if result:
                    return result
            except Exception as e:
                print(f"Climatiq API error: {e}, falling back to local estimates")

        # Fallback to local estimates
        return self._estimate_locally(category, amount)

    async def _estimate_via_api(
        self,
        category: str,
        amount: float,
        category_mapping: Dict
    ) -> Optional[Dict]:
        """Estimate using Climatiq API."""
        activity_id = category_mapping.get(category)
        if not activity_id:
            return None

        payload = {
            "emission_factor": {
                "activity_id": activity_id,
                "data_version": "^1"
            },
            "parameters": {
                "money": amount,
                "money_unit": "usd"
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/estimate",
                headers=self.headers,
                json=payload,
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "carbon_kg": data.get("co2e", 0),
                    "source": "climatiq_api",
                    "confidence": "high",
                    "details": data
                }

        return None

    def _estimate_locally(self, category: str, amount: float) -> Dict:
        """
        Local carbon estimation using average emission factors.
        Based on research data and EPA estimates.
        """
        # Carbon intensity factors (kg CO2 per USD)
        emission_factors = {
            "food_meat": 0.8,  # Beef has high emissions
            "food_plant": 0.2,  # Plant-based much lower
            "transportation_air": 2.5,  # Air travel very high
            "transportation_car": 1.2,  # Gasoline/diesel
            "transportation_public": 0.3,  # Public transit lower
            "energy": 0.9,  # Grid electricity
            "retail_clothing": 0.6,  # Fast fashion
            "retail_electronics": 0.7,  # Manufacturing impact
            "retail_general": 0.4,  # General goods
            "services": 0.1,  # Digital services low
            "dining": 0.5,  # Restaurant meals
            "other": 0.3  # Default estimate
        }

        carbon_per_dollar = emission_factors.get(category, 0.3)
        carbon_kg = amount * carbon_per_dollar

        return {
            "carbon_kg": round(carbon_kg, 2),
            "source": "local_estimate",
            "confidence": "medium",
            "emission_factor": carbon_per_dollar,
            "details": {
                "category": category,
                "amount_usd": amount,
                "methodology": "average_emission_factor"
            }
        }

    def compare_alternatives(self, category: str, amount: float) -> Dict:
        """
        Compare carbon impact with alternative choices.

        Args:
            category: Purchase category
            amount: Purchase amount

        Returns:
            Dictionary with comparison data
        """
        alternatives = {
            "food_meat": {
                "current": "Meat-based meal",
                "alternative": "Plant-based meal",
                "reduction_percent": 75,
                "tip": "Switching to plant-based alternatives can reduce food emissions by up to 75%"
            },
            "transportation_air": {
                "current": "Air travel",
                "alternative": "Train or bus",
                "reduction_percent": 80,
                "tip": "Consider train travel for shorter distances to reduce emissions by 80%"
            },
            "transportation_car": {
                "current": "Gasoline vehicle",
                "alternative": "Electric vehicle or public transit",
                "reduction_percent": 60,
                "tip": "EVs or public transit can cut transportation emissions by 60%+"
            },
            "retail_clothing": {
                "current": "New clothing",
                "alternative": "Second-hand or sustainable brands",
                "reduction_percent": 50,
                "tip": "Buying second-hand or sustainable fashion reduces emissions by ~50%"
            },
            "energy": {
                "current": "Grid electricity",
                "alternative": "Renewable energy plan",
                "reduction_percent": 70,
                "tip": "Switching to renewable energy can reduce home emissions by 70%"
            }
        }

        estimate = self._estimate_locally(category, amount)
        carbon_kg = estimate["carbon_kg"]

        if category in alternatives:
            alt = alternatives[category]
            reduction = carbon_kg * (alt["reduction_percent"] / 100)

            return {
                "current_carbon_kg": carbon_kg,
                "alternative": alt["alternative"],
                "potential_reduction_kg": round(reduction, 2),
                "reduction_percent": alt["reduction_percent"],
                "tip": alt["tip"]
            }

        return {
            "current_carbon_kg": carbon_kg,
            "alternative": None,
            "potential_reduction_kg": 0,
            "reduction_percent": 0,
            "tip": "Keep tracking your purchases to find more opportunities to reduce emissions"
        }
