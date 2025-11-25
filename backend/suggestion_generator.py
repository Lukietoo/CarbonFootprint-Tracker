"""
AI-powered suggestion generator for carbon reduction recommendations.
"""
from typing import List, Dict
from openai import AsyncOpenAI
from backend.config import settings


class SuggestionGenerator:
    """
    Generates personalized carbon reduction suggestions using OpenAI.
    Falls back to rule-based suggestions if API is unavailable.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the suggestion generator.

        Args:
            api_key: OpenAI API key (optional, uses settings if not provided)
        """
        self.api_key = api_key or settings.openai_api_key
        self.client = None
        if self.api_key and self.api_key != "your_openai_api_key":
            self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate_suggestions(
        self,
        transactions: List[Dict],
        total_carbon: float,
        category_breakdown: Dict
    ) -> List[Dict]:
        """
        Generate personalized carbon reduction suggestions.

        Args:
            transactions: List of recent transactions
            total_carbon: Total carbon footprint in kg
            category_breakdown: Carbon emissions by category

        Returns:
            List of suggestion dictionaries
        """
        # Try using OpenAI API if available
        if self.client:
            try:
                return await self._generate_ai_suggestions(
                    transactions,
                    total_carbon,
                    category_breakdown
                )
            except Exception as e:
                print(f"OpenAI API error: {e}, falling back to rule-based suggestions")

        # Fallback to rule-based suggestions
        return self._generate_rule_based_suggestions(category_breakdown, total_carbon)

    async def _generate_ai_suggestions(
        self,
        transactions: List[Dict],
        total_carbon: float,
        category_breakdown: Dict
    ) -> List[Dict]:
        """Generate suggestions using OpenAI API."""
        # Prepare context for AI
        context = f"""
        User's carbon footprint analysis:
        - Total carbon emissions: {total_carbon:.2f} kg CO2
        - Category breakdown: {category_breakdown}
        - Recent transactions: {len(transactions)} purchases

        Top categories:
        {self._format_top_categories(category_breakdown)}
        """

        prompt = f"""
        Based on this user's carbon footprint data:
        {context}

        Generate 5 specific, actionable suggestions to reduce their carbon footprint.
        For each suggestion, provide:
        1. A clear, actionable recommendation
        2. The estimated carbon reduction in kg CO2
        3. The difficulty level (easy/medium/hard)
        4. The category it applies to

        Format as JSON array with fields: suggestion, reduction_kg, difficulty, category
        """

        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sustainability expert helping users reduce their carbon footprint. Provide specific, actionable, and personalized advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=800
        )

        # Parse AI response
        suggestions_text = response.choices[0].message.content

        # Try to extract structured data, fallback to text parsing
        try:
            import json
            suggestions = json.loads(suggestions_text)
            return suggestions
        except:
            # Parse as text and create structured suggestions
            return self._parse_text_suggestions(suggestions_text)

    def _generate_rule_based_suggestions(
        self,
        category_breakdown: Dict,
        total_carbon: float
    ) -> List[Dict]:
        """
        Generate suggestions using rule-based logic.
        Focuses on the highest-impact categories.
        """
        suggestions = []

        # Sort categories by carbon impact
        sorted_categories = sorted(
            category_breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Suggestion templates
        suggestion_templates = {
            "food_meat": {
                "suggestion": "Try 'Meatless Mondays' - replace one meat meal per week with plant-based alternatives",
                "reduction_percent": 15,
                "difficulty": "easy",
                "category": "food"
            },
            "transportation_air": {
                "suggestion": "For trips under 500 miles, consider train or bus travel instead of flying",
                "reduction_percent": 80,
                "difficulty": "medium",
                "category": "transportation"
            },
            "transportation_car": {
                "suggestion": "Combine errands into single trips and maintain proper tire pressure to improve fuel efficiency",
                "reduction_percent": 10,
                "difficulty": "easy",
                "category": "transportation"
            },
            "energy": {
                "suggestion": "Switch to LED bulbs and unplug devices when not in use to reduce energy consumption",
                "reduction_percent": 20,
                "difficulty": "easy",
                "category": "energy"
            },
            "retail_clothing": {
                "suggestion": "Buy second-hand clothing or choose sustainable brands with eco-certifications",
                "reduction_percent": 50,
                "difficulty": "easy",
                "category": "shopping"
            },
            "retail_electronics": {
                "suggestion": "Extend device lifespan by repairing instead of replacing, and recycle old electronics properly",
                "reduction_percent": 40,
                "difficulty": "medium",
                "category": "shopping"
            },
            "dining": {
                "suggestion": "Choose restaurants with local, seasonal ingredients to reduce food miles",
                "reduction_percent": 25,
                "difficulty": "easy",
                "category": "food"
            }
        }

        # Generate top 5 suggestions based on user's highest-impact categories
        for category, carbon_kg in sorted_categories[:5]:
            if category in suggestion_templates:
                template = suggestion_templates[category]
                reduction_kg = carbon_kg * (template["reduction_percent"] / 100)

                suggestions.append({
                    "suggestion": template["suggestion"],
                    "reduction_kg": round(reduction_kg, 2),
                    "difficulty": template["difficulty"],
                    "category": template["category"],
                    "current_impact_kg": round(carbon_kg, 2)
                })

        # Add general suggestions if we have less than 5
        general_suggestions = [
            {
                "suggestion": "Use reusable bags, bottles, and containers to reduce single-use plastic waste",
                "reduction_kg": round(total_carbon * 0.05, 2),
                "difficulty": "easy",
                "category": "general",
                "current_impact_kg": 0
            },
            {
                "suggestion": "Buy local and seasonal produce to reduce transportation emissions",
                "reduction_kg": round(total_carbon * 0.08, 2),
                "difficulty": "easy",
                "category": "food",
                "current_impact_kg": 0
            },
            {
                "suggestion": "Set your thermostat 2°F lower in winter and 2°F higher in summer",
                "reduction_kg": round(total_carbon * 0.10, 2),
                "difficulty": "easy",
                "category": "energy",
                "current_impact_kg": 0
            }
        ]

        while len(suggestions) < 5 and general_suggestions:
            suggestions.append(general_suggestions.pop(0))

        return suggestions[:5]

    def _format_top_categories(self, category_breakdown: Dict) -> str:
        """Format category breakdown for AI context."""
        sorted_cats = sorted(
            category_breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return "\n".join([f"- {cat}: {val:.2f} kg CO2" for cat, val in sorted_cats[:5]])

    def _parse_text_suggestions(self, text: str) -> List[Dict]:
        """Parse AI-generated text into structured suggestions."""
        # Simple text parser for fallback
        suggestions = []
        lines = text.strip().split('\n')

        current_suggestion = {}
        for line in lines:
            line = line.strip()
            if line and (line.startswith(('-', '*', '•')) or line[0].isdigit()):
                if current_suggestion:
                    suggestions.append(current_suggestion)
                current_suggestion = {
                    "suggestion": line.lstrip('-*•0123456789. '),
                    "reduction_kg": 5.0,
                    "difficulty": "medium",
                    "category": "general"
                }

        if current_suggestion:
            suggestions.append(current_suggestion)

        return suggestions[:5]

    def get_quick_wins(self, category_breakdown: Dict) -> List[str]:
        """
        Get quick, easy wins for carbon reduction.

        Args:
            category_breakdown: Carbon emissions by category

        Returns:
            List of quick action items
        """
        quick_wins = [
            "Switch to reusable shopping bags",
            "Unplug chargers when not in use",
            "Choose 'eco' mode on appliances",
            "Air dry clothes instead of using dryer",
            "Use a reusable water bottle",
            "Opt for digital receipts",
            "Combine car trips to reduce driving"
        ]

        return quick_wins[:5]
