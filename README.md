# 🏪 RR ENTERPRISE — Hardware Shop Management Software

A professional, full-featured shop management system built with **Python + Streamlit**.

---

## ✅ Features

| Module | What it does |
|--------|-------------|
| **Billing** | Select products, add to cart, auto-calculate GST (18%), generate & download PDF invoices |
| **Stock** | Add/edit/delete products, update stock & prices, view colour-coded inventory table |
| **Reports** | Daily & monthly sales, category revenue, full transaction history with CSV export |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The browser will open automatically at **http://localhost:8501**

---

## 📁 Project Structure

```
rr_enterprise/
├── app.py          # Main entry point + global CSS
├── billing.py      # Billing / cart / invoice preview
├── stock.py        # Stock management
├── reports.py      # Sales reports & analytics
├── database.py     # SQLite setup, all DB helpers
├── pdf_utils.py    # ReportLab PDF invoice generator
├── requirements.txt
└── README.md
```

The SQLite database (`rr_enterprise.db`) is auto-created on first run with **20 pre-loaded products** across four categories:
- Asian Paints (5 products)
- Birla Opus (3 products)
- Pipes (5 products)
- Electrical (7 products)

---

## 🖥️ Screenshots (UI Overview)

| Section | Description |
|---------|-------------|
| **Sidebar** | Dark navy gradient nav with RR Enterprise branding |
| **Billing** | Split-layout — add items left, live invoice preview right |
| **Stock** | Tabbed view: inventory table, add product form, update/delete |
| **Reports** | Tabbed: daily bar chart, monthly summary, category breakdown, full log |

---

## ⚙️ Configuration

Edit `database.py` → `_seed_products()` to change default products.

Change `LOW_STOCK_THRESHOLD` in `stock.py` (default: **10 units**).

GST rate is set in `billing.py` → `GST_RATE = 0.18`.
