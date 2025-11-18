# Contributing to Carbon Footprint Tracker

Thank you for your interest in contributing to Carbon Footprint Tracker! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and inclusive. We're all here to build something that helps the planet.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has been suggested
2. Create an issue describing:
   - The problem it solves
   - Proposed solution
   - Any alternatives considered
   - Additional context

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/CarbonFootprint-Tracker.git
   cd CarbonFootprint-Tracker
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation
   - Add comments for complex logic

4. **Test your changes**
   ```bash
   # Run tests
   pytest tests/

   # Test both backend and frontend
   ./run_both.sh
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

   Use conventional commits:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation
   - `Refactor:` for code refactoring

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Include screenshots if UI changes

## Development Setup

1. **Install dependencies**
   ```bash
   ./setup.sh
   ```

2. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Run in development mode**
   ```bash
   ./run_both.sh
   ```

## Code Style

### Python

- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 100 characters
- Use docstrings for functions and classes

```python
def calculate_carbon(amount: float, category: str) -> float:
    """
    Calculate carbon emissions for a transaction.

    Args:
        amount: Transaction amount in USD
        category: Purchase category

    Returns:
        Carbon emissions in kg CO₂
    """
    pass
```

### Project Structure

- Backend code in `backend/`
- Frontend code in `frontend/`
- Tests in `tests/`
- Documentation in `docs/`

## Testing

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_classifier.py

# With coverage
pytest --cov=backend tests/
```

### Writing Tests

```python
def test_classify_transaction():
    classifier = TransactionClassifier()
    category, confidence, carbon = classifier.classify(
        "Starbucks Coffee",
        6.75
    )
    assert category == "dining"
    assert confidence > 0.5
    assert carbon > 0
```

## Documentation

- Update README.md for major changes
- Update API.md for API changes
- Add docstrings to new functions
- Include examples in documentation

## Areas for Contribution

### High Priority
- [ ] Unit tests for all modules
- [ ] OCR implementation for receipt scanning
- [ ] Bank API integrations (Plaid)
- [ ] Docker containerization
- [ ] Performance optimization

### Medium Priority
- [ ] Enhanced ML models (DistilBERT)
- [ ] More carbon categories
- [ ] Multi-currency support
- [ ] Export functionality (PDF, CSV)
- [ ] User authentication

### Low Priority
- [ ] Mobile app
- [ ] Social features
- [ ] Gamification
- [ ] Internationalization (i18n)

## Questions?

Feel free to:
- Open an issue
- Start a discussion
- Reach out to maintainers

Thank you for contributing to a more sustainable future! 🌱
