#  CarbonFootprint Tracker


A Python-based web app that automatically estimates your carbon footprint from purchase data and offers actionable suggestions to reduce it.  
This project combines sustainability data, NLP classification, and AI-generated insights to help users visualize and improve their environmental impact.

---

##  Overview

Most people want to live sustainably but don’t know where to start.  
**CarbonFootprint Tracker** bridges that gap by analyzing receipts or bank transactions, estimating the CO₂ impact of each purchase, and providing data-driven recommendations to help users make greener choices.

---

##  Features

-  **Transaction Analysis:** Parse receipts or bank data (CSV or API input).  
-  **AI Classification:** Categorize purchases (e.g., food, transport, retail) using NLP.  
-  **Carbon Estimation:** Fetch emission data via the **Climatiq API**.  
-  **Smart Suggestions:** Generate personalized tips with the **OpenAI API**.  
-  **Visualization (optional):** Display monthly carbon usage with Streamlit or a React dashboard.

---

##  Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | **FastAPI (Python)** |
| Database | **Supabase / PostgreSQL** |
| NLP & AI | **DistilBERT / OpenAI API** |
| Carbon Data | **Climatiq API** |
| Visualization (optional) | **Streamlit / React** |
| OCR (optional) | **Tesseract / AWS Textract** |

---

## 📁 Folder Structure

