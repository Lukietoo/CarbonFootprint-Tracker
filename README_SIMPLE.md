# 🌱 Carbon Footprint Tracker - SIMPLE VERSION

**Easy-to-understand version for learning & presentations!**

## What This App Does

Track the carbon footprint of your purchases with a simple calculator and beautiful charts.

### Features:
- ✅ **Simple Calculator** - Add purchases manually, see CO₂ instantly
- ✅ **Track Over Time** - See your history in a database
- ✅ **Pretty Charts** - Pie charts, bar charts, metrics
- ✅ **Get Tips** - Simple suggestions to reduce your footprint
- ✅ **No APIs Needed** - Everything works offline!

---

## 📁 Project Structure (Simple!)

```
CarbonFootprint-Tracker/
├── backend/
│   └── main_simple.py          # Backend (200 lines with comments!)
├── frontend/
│   └── app_simple.py            # Frontend (300 lines with comments!)
├── backend/
│   ├── database.py              # Database setup (reused from before)
│   └── models.py                # Data models (reused from before)
└── start_simple.sh              # One command to start everything!
```

---

## 🚀 How to Run

### Method 1: One Command (Easiest!)

```bash
cd ~/CarbonFootprint-Tracker
./start_simple.sh
```

### Method 2: Manual (If you want to understand)

**Terminal 1 - Start Backend:**
```bash
cd ~/CarbonFootprint-Tracker
python3 -m uvicorn backend.main_simple:app --reload
```

**Terminal 2 - Start Frontend:**
```bash
cd ~/CarbonFootprint-Tracker
streamlit run frontend/app_simple.py
```

**Then open:** http://localhost:8501

---

## 📚 How It Works (For Learning!)

### 1. **Add a Purchase** (Frontend → Backend)

```
User fills form:
  "Starbucks Coffee"
  $5.50
  Category: "food_plant"
        ↓
Frontend sends to: POST /api/transactions
        ↓
Backend calculates: $5.50 × 0.2 = 1.1 kg CO₂
        ↓
Backend saves to database
        ↓
Returns: "Added! 1.1 kg CO₂"
```

### 2. **View Dashboard** (Backend → Frontend)

```
Frontend asks: GET /api/dashboard
        ↓
Backend queries database
        ↓
Calculates totals, breakdown by category
        ↓
Returns: {total: 50.5 kg, monthly: 10.2 kg, ...}
        ↓
Frontend creates charts with Plotly
```

### 3. **Get Suggestions** (Smart Logic!)

```
Backend looks at your top 3 categories
        ↓
Picks relevant tips from hardcoded list
        ↓
Returns: ["Try Meatless Mondays", "Use public transport", ...]
```

---

## 💻 Understanding the Code

### Backend (`backend/main_simple.py`)

**Line 30-40**: Simple CO₂ calculation
```python
CARBON_ESTIMATES = {
    "food_meat": 0.8,    # kg CO2 per $1 spent
    "food_plant": 0.2,
    "transportation": 0.5,
}

def calculate_carbon(category, amount):
    return amount * CARBON_ESTIMATES[category]
```

**Line 90-120**: Add transaction endpoint
```python
@app.post("/api/transactions")
async def add_transaction(transaction, db):
    # Calculate CO2
    carbon_kg = calculate_carbon(transaction.category, transaction.amount)

    # Save to database
    db.add(new_transaction)
    db.commit()

    return new_transaction
```

### Frontend (`frontend/app_simple.py`)

**Line 80-100**: Talk to backend
```python
def call_api(endpoint, method="GET", data=None):
    url = f"http://localhost:8000{endpoint}"
    response = requests.get(url)  # or .post()
    return response.json()
```

**Line 150-200**: Create charts
```python
fig = px.pie(names=categories, values=co2_amounts)
st.plotly_chart(fig)
```

---

## 🎯 What You Learn

### Technologies:
1. **FastAPI** - How to create REST APIs
2. **Streamlit** - How to build web UIs in Python
3. **SQLite** - How to store data
4. **Plotly** - How to make charts
5. **HTTP** - How frontend/backend communicate (GET, POST, DELETE)

### Concepts:
1. **Frontend vs Backend** - Separation of concerns
2. **REST APIs** - Endpoints, requests, responses
3. **Database CRUD** - Create, Read, Update, Delete
4. **Data Visualization** - Charts and graphs
5. **User Interface** - Forms, buttons, navigation

---

## 🧪 Testing It Out

1. **Load Sample Data** (sidebar button)
2. **View Dashboard** - See charts appear
3. **Add Purchase** - Add "Coffee $5" in food_plant category
4. **Check Dashboard** - See your new purchase in charts
5. **View Suggestions** - Get tips based on your data

---

## 🔧 Customizing

### Change CO₂ Estimates

Edit `backend/main_simple.py` line 30:
```python
CARBON_ESTIMATES = {
    "food_meat": 1.0,  # Change this number!
    # ...
}
```

### Add New Category

1. Add to `CARBON_ESTIMATES` dict
2. Add to dropdown in `frontend/app_simple.py` line 180

### Change Colors

Edit `frontend/app_simple.py` line 30-60 (CSS section)

---

## 🆘 Troubleshooting

**Problem**: "Can't connect to backend"
**Solution**: Make sure backend is running (see Terminal 1)

**Problem**: "No module named X"
**Solution**: `pip3 install -r requirements.txt`

**Problem**: "Port already in use"
**Solution**: Kill existing process: `pkill -f streamlit` or `pkill -f uvicorn`

---

## 📊 For Your Presentation

### Good Talking Points:
1. "This app tracks carbon footprint in real-time"
2. "I built it with Python - both frontend and backend"
3. "It uses a database to track purchases over time"
4. "The charts update automatically when you add data"
5. "It gives personalized tips based on your spending"

### Demo Flow:
1. Show empty dashboard
2. Load sample data
3. Show charts appearing
4. Add a new purchase manually
5. Show it in the dashboard
6. Go to suggestions page

---

## 🌟 Next Steps (If You Want to Add More)

- [ ] Add date range filter to dashboard
- [ ] Export data to CSV
- [ ] Compare with friends
- [ ] Set carbon reduction goals
- [ ] Add more categories
- [ ] Mobile-friendly design

---

**Made for learning! Every line of code has comments explaining what it does.**

Questions? Check the code comments or create an issue!
