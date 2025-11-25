# Changelog

All notable changes to the Carbon Footprint Tracker project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2024-01-18

### Fixed
- Fixed potential IndexError in `suggestion_generator.py` when parsing empty lines in AI-generated text
  - Added check for non-empty lines before accessing line[0].isdigit()
  - Improves robustness when OpenAI API returns unexpected formats

### Changed
- Optimized `requirements.txt` by removing unused heavy dependencies:
  - Removed `transformers` (4.35.2) - not used in current implementation
  - Removed `torch` (2.1.1) - not used in current implementation
  - Removed `scikit-learn` (1.3.2) - not used in current implementation
  - Removed `matplotlib` (3.8.2) - using Plotly instead
  - Removed `pytesseract` and `Pillow` - OCR features planned for future
  - This reduces installation size from ~5GB to ~500MB

### Added
- Comprehensive test suite with pytest
  - Added `tests/test_classifier.py` - 9 unit tests for transaction classification
  - Added `tests/test_carbon_estimator.py` - 7 unit tests for carbon estimation
  - Added `tests/test_transaction_parser.py` - 11 unit tests for transaction parsing
  - Added `test_basic.py` - Simple test script for quick verification
- Development dependencies in `requirements-dev.txt`
  - pytest, pytest-cov, pytest-asyncio for testing
  - black, flake8, mypy, isort for code quality
- Configuration files:
  - Added `pytest.ini` for pytest configuration
  - Added `.flake8` for linting rules
  - Added `pyproject.toml` for tool configuration
- Updated README with detailed testing and development instructions

### Documentation
- Enhanced README with:
  - Detailed test running instructions
  - Code quality tool usage
  - Development workflow guidelines
- Added CHANGELOG.md for version tracking
- Updated .gitignore to exclude test coverage and cache files

## [1.0.0] - 2024-01-18

### Added
- Initial release of Carbon Footprint Tracker
- FastAPI backend with RESTful API
  - Transaction upload and management
  - Carbon estimation
  - AI-powered suggestions
  - Dashboard statistics
- Streamlit frontend
  - Interactive dashboard with visualizations
  - Transaction history and filtering
  - CSV upload functionality
  - Personalized suggestions page
- Core features:
  - NLP-based transaction classification (12 categories)
  - Carbon emission estimation (Climatiq API + local fallback)
  - AI suggestion generation (OpenAI API + rule-based fallback)
  - SQLite/PostgreSQL database support
  - Sample data for testing
- Documentation:
  - Comprehensive README
  - API documentation
  - Contributing guidelines
  - Setup scripts for easy installation
- MIT License
