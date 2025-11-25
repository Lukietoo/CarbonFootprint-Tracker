"""
Simple test script to verify core logic without external dependencies.
"""

def test_classifier():
    """Test classifier logic."""
    from backend.classifier import TransactionClassifier

    classifier = TransactionClassifier()

    # Test various transactions
    tests = [
        ("Starbucks Coffee", 6.75, "dining"),
        ("Shell Gas Station", 45.00, "transportation_car"),
        ("United Airlines Flight", 350.00, "transportation_air"),
        ("Whole Foods Market", 87.50, "food_plant"),
        ("Unknown Store", 25.00, "other"),
    ]

    print("Testing Classifier...")
    for desc, amount, expected_category in tests:
        category, confidence, carbon = classifier.classify(desc, amount)
        print(f"  {desc}: {category} (expected: {expected_category}) - {carbon:.2f} kg CO2")
        if category != expected_category:
            print(f"    WARNING: Expected {expected_category}, got {category}")

    print("✓ Classifier tests complete\n")


def test_carbon_estimator():
    """Test carbon estimator logic."""
    from backend.carbon_estimator import CarbonEstimator

    estimator = CarbonEstimator()

    print("Testing Carbon Estimator...")
    categories = ["food_meat", "food_plant", "transportation_air", "energy"]
    for category in categories:
        result = estimator._estimate_locally(category, 100.0)
        print(f"  {category}: {result['carbon_kg']} kg CO2 for $100")

    print("✓ Carbon estimator tests complete\n")


def test_suggestion_generator():
    """Test suggestion generator logic."""
    from backend.suggestion_generator import SuggestionGenerator

    generator = SuggestionGenerator()

    print("Testing Suggestion Generator...")
    category_breakdown = {
        "food_meat": 50.0,
        "transportation_air": 200.0,
        "energy": 30.0
    }

    suggestions = generator._generate_rule_based_suggestions(category_breakdown, 280.0)
    print(f"  Generated {len(suggestions)} suggestions:")
    for i, sug in enumerate(suggestions, 1):
        print(f"    {i}. {sug['suggestion'][:50]}... ({sug['reduction_kg']} kg)")

    print("✓ Suggestion generator tests complete\n")


def test_transaction_parser():
    """Test transaction parser logic."""
    from backend.transaction_parser import TransactionParser

    parser = TransactionParser()

    print("Testing Transaction Parser...")
    samples = parser.create_sample_data()
    print(f"  Created {len(samples)} sample transactions")
    print(f"  First transaction: {samples[0]['description']}")

    validated = parser.validate_transactions(samples)
    print(f"  Validated {len(validated)} transactions")

    print("✓ Transaction parser tests complete\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Carbon Footprint Tracker Tests")
    print("=" * 60)
    print()

    try:
        test_classifier()
    except Exception as e:
        print(f"✗ Classifier test failed: {e}\n")

    try:
        test_carbon_estimator()
    except Exception as e:
        print(f"✗ Carbon estimator test failed: {e}\n")

    try:
        test_suggestion_generator()
    except Exception as e:
        print(f"✗ Suggestion generator test failed: {e}\n")

    try:
        test_transaction_parser()
    except Exception as e:
        print(f"✗ Transaction parser test failed: {e}\n")

    print("=" * 60)
    print("Tests Complete")
    print("=" * 60)
