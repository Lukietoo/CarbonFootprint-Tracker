# How to See the Forest Theme

If you don't see the forest background after updating, try these steps:

## Option 1: Hard Refresh Browser
**Mac:**
- Chrome/Edge: `Cmd + Shift + R`
- Safari: `Cmd + Option + E`, then `Cmd + R`
- Firefox: `Cmd + Shift + R`

**Windows:**
- Chrome/Edge/Firefox: `Ctrl + Shift + R`

## Option 2: Clear Streamlit Cache
```bash
# Stop streamlit (Ctrl+C)
# Delete cache
rm -rf ~/.streamlit/cache

# Restart streamlit
streamlit run frontend/app.py
```

## Option 3: Force Stop and Restart
```bash
# Kill all instances
pkill -f streamlit
pkill -f uvicorn

# Restart fresh
cd /Users/toehaus/CarbonFootprint-Tracker

# Terminal 1 - Backend
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
streamlit run frontend/app.py
```

## What You Should See:
- ✅ Beautiful forest/trees background image
- ✅ Green gradient sidebar
- ✅ Semi-transparent white content boxes
- ✅ Rounded corners on all cards
- ✅ Hover animations on buttons and cards
- ✅ Dark green text that's easy to read

If you still don't see it, the background image might be blocked. The CSS is definitely applied!
