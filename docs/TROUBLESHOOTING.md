# Troubleshooting Guide

Common issues and solutions for Carbon Footprint Tracker.

## Installation Issues

### psycopg2-binary Installation Error

**Error:**
```
Error: pg_config executable not found.
psycopg2-binary requires PostgreSQL development libraries
```

**Solution:**

The app uses **SQLite by default** and doesn't need PostgreSQL libraries. This error means you have an older version of requirements.txt.

**Option 1: Use SQLite (Recommended)**
```bash
# Make sure you have the latest requirements.txt
git pull origin claude/carbon-footprint-tracker-018TyuJjdgHw6gsJGZeofov3

# Install dependencies (SQLite only)
pip install -r requirements.txt
```

**Option 2: Use PostgreSQL**

If you specifically want to use PostgreSQL/Supabase:

**On macOS:**
```bash
brew install postgresql
pip install -r requirements-postgres.txt
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install libpq-dev
pip install -r requirements-postgres.txt
```

**On Windows:**
```bash
# Download PostgreSQL from https://www.postgresql.org/download/windows/
# Then install Python dependencies
pip install -r requirements-postgres.txt
```

### Module Not Found Errors

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Pandas/NumPy Installation Issues

**Error:**
```
Building wheel for pandas failed
```

**Solution:**

These packages require compilation. Try installing pre-built wheels:

```bash
# Upgrade pip
pip install --upgrade pip

# Install with pre-built wheels
pip install --only-binary :all: pandas numpy
```

Or use conda:
```bash
conda install pandas numpy
pip install -r requirements.txt
```

## Runtime Errors

### Port Already in Use

**Error:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**

Another process is using port 8000 or 8501.

**Find and kill the process:**
```bash
# On macOS/Linux
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Or use different ports:**
```bash
# Backend
uvicorn backend.main:app --port 8001

# Frontend
streamlit run frontend/app.py --server.port 8502
```

### Database Locked Error

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**

SQLite database is being accessed by multiple processes.

```bash
# Stop all running instances
pkill -f "uvicorn"
pkill -f "streamlit"

# Delete the database and restart
rm carbon_tracker.db

# Restart the application
./run_both.sh
```

### API Connection Error (Frontend)

**Error in Streamlit:**
```
Connection Error: Failed to connect to http://localhost:8000
```

**Solution:**

The backend isn't running.

```bash
# Terminal 1: Start backend first
./run_backend.sh

# Wait for "Application startup complete"

# Terminal 2: Then start frontend
./run_frontend.sh
```

## API Issues

### OpenAI API Error

**Error:**
```
OpenAI API error: Invalid API key
```

**Solution:**

The OpenAI API key is invalid or not set. **This is optional** - the app works without it.

**Option 1: Skip OpenAI (Recommended)**
- The app will use rule-based suggestions instead
- No changes needed

**Option 2: Add Valid API Key**
```bash
# Edit .env file
OPENAI_API_KEY=sk-your-actual-key-here
```

### Climatiq API Error

**Error:**
```
Climatiq API error: 401 Unauthorized
```

**Solution:**

Similar to OpenAI, **this is optional**. The app falls back to local estimates.

**Option 1: Use Local Estimates (Recommended)**
- No action needed
- The app works fine with local carbon calculations

**Option 2: Add Valid API Key**
```bash
# Edit .env file
CLIMATIQ_API_KEY=your-actual-key-here
```

Get a free key at: https://www.climatiq.io/

## Data Issues

### CSV Upload Error

**Error:**
```
Error processing file: CSV must contain 'description' or 'merchant' column
```

**Solution:**

Your CSV needs required columns:
- `description` (or `merchant` or `name`)
- `amount` (or `total` or `price`)

**Valid CSV format:**
```csv
date,description,amount
2024-01-15,Store Name,50.00
2024-01-16,Another Store,25.00
```

### No Transactions Showing

**Issue:** Dashboard shows "No transactions found"

**Solution:**

1. Load sample data:
   - Click "Load Sample Data" in sidebar
   - Or use API: `POST http://localhost:8000/api/sample-data`

2. Upload your own CSV:
   - Go to "Upload Data" page
   - Choose CSV file
   - Click "Process & Upload"

## Testing Issues

### Pytest Not Found

**Error:**
```
bash: pytest: command not found
```

**Solution:**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Verify pytest is installed
pytest --version
```

### Tests Failing

**Error:**
```
ImportError: No module named 'backend'
```

**Solution:**
```bash
# Run tests from project root
cd /path/to/CarbonFootprint-Tracker

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run tests
pytest
```

## Performance Issues

### Slow Streamlit Loading

**Issue:** Frontend takes long to load

**Solutions:**

1. **Disable developer mode:**
   ```bash
   streamlit run frontend/app.py --server.runOnSave false
   ```

2. **Clear cache:**
   ```bash
   rm -rf ~/.streamlit/cache
   ```

3. **Reduce data:**
   - Limit transactions displayed
   - Use pagination

### High Memory Usage

**Issue:** App using too much RAM

**Solutions:**

1. **Limit database queries:**
   - Use smaller `limit` parameter
   - Filter by date range

2. **Restart periodically:**
   ```bash
   # Stop services
   pkill -f "uvicorn"
   pkill -f "streamlit"

   # Restart
   ./run_both.sh
   ```

## Development Issues

### Import Errors During Development

**Error:**
```
ModuleNotFoundError: No module named 'backend.config'
```

**Solution:**

Ensure you're running from the project root:
```bash
# Always run from project root
cd /path/to/CarbonFootprint-Tracker

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run backend
python -m uvicorn backend.main:app
```

### Code Changes Not Reflecting

**Issue:** Changes to code don't appear in running app

**Solution:**

**Backend:**
- Restart with `--reload` flag:
  ```bash
  uvicorn backend.main:app --reload
  ```

**Frontend:**
- Streamlit auto-reloads, but you can force with:
  - Click "Rerun" in top-right
  - Or press `R`

## Getting Help

If you're still having issues:

1. **Check logs:**
   ```bash
   # Backend logs
   tail -f backend.log

   # Streamlit logs
   tail -f ~/.streamlit/logs/*.log
   ```

2. **Verify installation:**
   ```bash
   # Check Python version (3.8+ required)
   python --version

   # Check installed packages
   pip list | grep -E "fastapi|streamlit|sqlalchemy"
   ```

3. **Test basic functionality:**
   ```bash
   # Run simple tests
   python test_basic.py
   ```

4. **Check the Issues page:**
   - GitHub Issues: [Report a bug](https://github.com/yourusername/CarbonFootprint-Tracker/issues)

5. **Clean reinstall:**
   ```bash
   # Remove virtual environment
   rm -rf venv

   # Start fresh
   ./setup.sh
   ```

## Quick Diagnostic

Run this to check your environment:

```bash
#!/bin/bash
echo "=== System Check ==="
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo ""
echo "=== Installed Packages ==="
pip list | grep -E "fastapi|streamlit|sqlalchemy|pandas" || echo "Missing packages!"
echo ""
echo "=== Ports ==="
echo "Port 8000 (backend):"
lsof -ti:8000 || echo "  Available"
echo "Port 8501 (frontend):"
lsof -ti:8501 || echo "  Available"
echo ""
echo "=== Database ==="
ls -lh carbon_tracker.db 2>/dev/null || echo "No database file (will be created on first run)"
```

Save as `check_system.sh`, make executable, and run:
```bash
chmod +x check_system.sh
./check_system.sh
```

---

**Still stuck?** Open an issue with:
- Error message (full stack trace)
- Operating system and version
- Python version
- Output of `pip list`
- Steps to reproduce
