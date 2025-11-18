"""Tests for the transaction parser."""
import pytest
from datetime import datetime
from backend.transaction_parser import TransactionParser


class TestTransactionParser:
    """Test cases for TransactionParser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = TransactionParser()

    def test_create_sample_data(self):
        """Test creation of sample data."""
        samples = self.parser.create_sample_data()
        assert len(samples) > 0
        assert "description" in samples[0]
        assert "amount" in samples[0]
        assert "date" in samples[0]

    def test_validate_transactions_valid(self):
        """Test validation of valid transactions."""
        transactions = [
            {"description": "Test Store", "amount": 50.0, "date": datetime.now()},
            {"description": "Another Store", "amount": 25.0, "date": datetime.now()}
        ]
        validated = self.parser.validate_transactions(transactions)
        assert len(validated) == 2

    def test_validate_transactions_invalid_amount(self):
        """Test validation removes transactions with invalid amounts."""
        transactions = [
            {"description": "Valid Store", "amount": 50.0, "date": datetime.now()},
            {"description": "Invalid Store", "amount": 0, "date": datetime.now()},
            {"description": "Negative Store", "amount": -10.0, "date": datetime.now()}
        ]
        validated = self.parser.validate_transactions(transactions)
        # Negative amount should be converted to positive by abs()
        assert len(validated) == 2

    def test_validate_transactions_missing_description(self):
        """Test validation removes transactions without description."""
        transactions = [
            {"description": "Valid Store", "amount": 50.0, "date": datetime.now()},
            {"description": "", "amount": 25.0, "date": datetime.now()},
            {"amount": 30.0, "date": datetime.now()}
        ]
        validated = self.parser.validate_transactions(transactions)
        assert len(validated) == 1

    def test_parse_json_basic(self):
        """Test parsing JSON data."""
        data = [
            {"description": "Store A", "amount": 50.0},
            {"description": "Store B", "amount": 75.0}
        ]
        transactions = self.parser.parse_json(data)
        assert len(transactions) == 2
        assert transactions[0]["description"] == "Store A"

    def test_parse_json_alternative_fields(self):
        """Test parsing JSON with alternative field names."""
        data = [
            {"merchant": "Store A", "total": 50.0},
            {"name": "Store B", "price": 75.0}
        ]
        transactions = self.parser.parse_json(data)
        assert len(transactions) == 2
        assert transactions[0]["description"] == "Store A"
        assert transactions[1]["description"] == "Store B"

    def test_parse_text_receipt_basic(self):
        """Test parsing text receipt."""
        receipt_text = """
        Starbucks Coffee
        123 Main Street
        Total: $6.75
        01/15/2024
        """
        transaction = self.parser.parse_text_receipt(receipt_text)
        assert transaction["description"] == "Starbucks Coffee"
        assert transaction["amount"] > 0

    def test_parse_text_receipt_no_total(self):
        """Test parsing receipt without clear total."""
        receipt_text = """
        Unknown Store
        Some items here
        """
        transaction = self.parser.parse_text_receipt(receipt_text)
        assert transaction["description"] == "Unknown Store"
        assert transaction["amount"] == 0.0

    def test_parse_csv_valid_data(self):
        """Test parsing valid CSV data."""
        csv_content = b"""date,description,amount
2024-01-15,Store A,50.00
2024-01-16,Store B,75.00
"""
        transactions = self.parser.parse_csv(csv_content)
        assert len(transactions) == 2
        assert transactions[0]["description"] == "Store A"
        assert transactions[0]["amount"] == 50.0

    def test_parse_csv_alternative_columns(self):
        """Test parsing CSV with alternative column names."""
        csv_content = b"""date,merchant,total
2024-01-15,Store A,50.00
"""
        transactions = self.parser.parse_csv(csv_content)
        assert len(transactions) == 1
        assert transactions[0]["description"] == "Store A"

    def test_parse_csv_missing_required_columns(self):
        """Test parsing CSV with missing required columns."""
        csv_content = b"""date,unknown_column
2024-01-15,Value
"""
        with pytest.raises(ValueError):
            self.parser.parse_csv(csv_content)
