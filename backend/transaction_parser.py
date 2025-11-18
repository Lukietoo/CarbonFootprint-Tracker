"""
Transaction parser for CSV files and receipt data.
"""
import pandas as pd
from typing import List, Dict
from datetime import datetime
import io


class TransactionParser:
    """
    Parses transaction data from various formats.
    Supports CSV files, JSON, and structured text.
    """

    def __init__(self):
        """Initialize the parser."""
        self.required_fields = ["description", "amount"]

    def parse_csv(self, file_content: bytes) -> List[Dict]:
        """
        Parse transactions from CSV file.

        Expected columns:
        - date (optional): Transaction date
        - description: Purchase description
        - amount: Transaction amount
        - category (optional): Category if pre-labeled

        Args:
            file_content: CSV file content as bytes

        Returns:
            List of transaction dictionaries
        """
        try:
            # Read CSV
            df = pd.read_csv(io.BytesIO(file_content))

            # Normalize column names
            df.columns = df.columns.str.lower().str.strip()

            # Check for required fields
            if "description" not in df.columns:
                # Try common alternatives
                if "merchant" in df.columns:
                    df["description"] = df["merchant"]
                elif "name" in df.columns:
                    df["description"] = df["name"]
                else:
                    raise ValueError("CSV must contain 'description' or 'merchant' column")

            if "amount" not in df.columns:
                # Try common alternatives
                if "total" in df.columns:
                    df["amount"] = df["total"]
                elif "price" in df.columns:
                    df["amount"] = df["price"]
                else:
                    raise ValueError("CSV must contain 'amount' or 'total' column")

            # Parse dates if present
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
            else:
                df["date"] = datetime.utcnow()

            # Convert to list of dictionaries
            transactions = []
            for _, row in df.iterrows():
                transaction = {
                    "description": str(row["description"]),
                    "amount": float(row["amount"]),
                    "date": row.get("date", datetime.utcnow()),
                    "category": row.get("category", None),
                    "raw_data": row.to_dict()
                }
                transactions.append(transaction)

            return transactions

        except Exception as e:
            raise ValueError(f"Error parsing CSV: {str(e)}")

    def parse_json(self, data: List[Dict]) -> List[Dict]:
        """
        Parse transactions from JSON data.

        Args:
            data: List of transaction dictionaries

        Returns:
            List of normalized transaction dictionaries
        """
        transactions = []

        for item in data:
            # Normalize field names
            description = (
                item.get("description") or
                item.get("merchant") or
                item.get("name") or
                "Unknown"
            )

            amount = (
                item.get("amount") or
                item.get("total") or
                item.get("price") or
                0.0
            )

            date = item.get("date")
            if date:
                try:
                    date = pd.to_datetime(date)
                except:
                    date = datetime.utcnow()
            else:
                date = datetime.utcnow()

            transaction = {
                "description": str(description),
                "amount": float(amount),
                "date": date,
                "category": item.get("category"),
                "raw_data": item
            }
            transactions.append(transaction)

        return transactions

    def parse_text_receipt(self, text: str) -> Dict:
        """
        Parse a text receipt using simple pattern matching.
        This is a basic implementation - can be enhanced with OCR.

        Args:
            text: Receipt text content

        Returns:
            Transaction dictionary
        """
        import re

        lines = text.strip().split('\n')

        # Extract merchant name (usually first non-empty line)
        merchant = "Unknown Merchant"
        for line in lines:
            if line.strip():
                merchant = line.strip()
                break

        # Extract total amount
        amount = 0.0
        total_patterns = [
            r'total[\s:$]*(\d+\.?\d*)',
            r'amount[\s:$]*(\d+\.?\d*)',
            r'\$\s*(\d+\.?\d*)',
        ]

        for line in lines:
            line_lower = line.lower()
            for pattern in total_patterns:
                match = re.search(pattern, line_lower)
                if match:
                    try:
                        amount = float(match.group(1))
                        break
                    except:
                        continue
            if amount > 0:
                break

        # Extract date
        date = datetime.utcnow()
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})',
        ]

        for line in lines:
            for pattern in date_patterns:
                match = re.search(pattern, line)
                if match:
                    try:
                        date = pd.to_datetime(match.group(1))
                        break
                    except:
                        continue

        return {
            "description": merchant,
            "amount": amount,
            "date": date,
            "category": None,
            "raw_data": {"text": text}
        }

    def validate_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """
        Validate and clean transaction data.

        Args:
            transactions: List of transaction dictionaries

        Returns:
            List of validated transactions
        """
        validated = []

        for trans in transactions:
            # Skip invalid transactions
            if not trans.get("description") or trans.get("amount", 0) <= 0:
                continue

            # Ensure required fields
            validated_trans = {
                "description": str(trans["description"]).strip(),
                "amount": abs(float(trans["amount"])),
                "date": trans.get("date", datetime.utcnow()),
                "category": trans.get("category"),
                "raw_data": trans.get("raw_data", {})
            }

            validated.append(validated_trans)

        return validated

    def create_sample_data(self) -> List[Dict]:
        """
        Create sample transaction data for demo purposes.

        Returns:
            List of sample transactions
        """
        from datetime import timedelta

        base_date = datetime.utcnow()

        samples = [
            {
                "description": "Whole Foods Market - Organic Groceries",
                "amount": 87.50,
                "date": base_date - timedelta(days=2)
            },
            {
                "description": "Shell Gas Station - Fuel",
                "amount": 45.00,
                "date": base_date - timedelta(days=3)
            },
            {
                "description": "United Airlines - Flight to NYC",
                "amount": 350.00,
                "date": base_date - timedelta(days=7)
            },
            {
                "description": "Starbucks Coffee",
                "amount": 6.75,
                "date": base_date - timedelta(days=1)
            },
            {
                "description": "Amazon - Electronics",
                "amount": 129.99,
                "date": base_date - timedelta(days=5)
            },
            {
                "description": "Local Steakhouse - Dinner",
                "amount": 95.00,
                "date": base_date - timedelta(days=4)
            },
            {
                "description": "Uber Ride",
                "amount": 18.50,
                "date": base_date - timedelta(days=1)
            },
            {
                "description": "Electric Company - Monthly Bill",
                "amount": 120.00,
                "date": base_date - timedelta(days=10)
            },
            {
                "description": "H&M - Clothing",
                "amount": 65.00,
                "date": base_date - timedelta(days=6)
            },
            {
                "description": "Chipotle - Lunch",
                "amount": 12.50,
                "date": base_date - timedelta(days=2)
            }
        ]

        return samples
