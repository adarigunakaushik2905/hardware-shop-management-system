import streamlit as st
import pandas as pd
from database import (get_all_products, add_product, update_stock,
                      update_price, delete_product, search_products)

CATEGORIES = ["Asian Paints", "Birla Opus", "Pipes", "Electrical", "Other"]
LOW_STOCK_THRESHOLD = 10


def stock_page():
    st.markdown("""
    <div class='shop-header'>
      <h1>📦 Stock Management</h1>
      <p>Manage inventory, add products and monitor stock levels</p>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 View Stock", "➕ Add Product", "✏️ Update / Delete"])

    # ── TAB 1: View Stock ─────────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns([3, 1])
        with c1:
            search = st.text_input("🔍 Search products", placeholder="Name or category…",
                                   key="stock_search")
        with c2:
            cat_filter = st.selectbox("Filter by Category",
                                      ["All"] + CATEGORIES, key="stock_cat")

        products = search_products(search) if search else get_all_products()
        if cat_filter != "All":
            products = [p for p in products if p["category"] == cat_filter]

        if not products:
            st.info("No products found.")
        else:
            _render_stock_metrics(products)
            st.markdown("#### 📊 Inventory Table")
            _render_stock_table(products)

    # ── TAB 2: Add Product ────────────────────────────────────────────────────
    with tab2:
        st.markdown("#### ➕ Add New Product")
        with st.form("add_product_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                pname    = st.text_input("Product Name *")
                price    = st.number_input("Price per Unit (₹) *", min_value=0.01,
                                          step=0.5, format="%.2f")
            with c2:
                category = st.selectbox("Category *", CATEGORIES)
                quantity = st.number_input("Initial Stock Qty *", min_value=0, step=1)

            submitted = st.form_submit_button("✅ Add Product", use_container_width=True)
            if submitted:
                if not pname.strip():
                    st.error("Product name is required.")
                else:
                    add_product(pname.strip(), category, price, quantity)
                    st.success(f"✅ '{pname}' added successfully!")
                    st.rerun()

    # ── TAB 3: Update / Delete ────────────────────────────────────────────────
    with tab3:
        st.markdown("#### ✏️ Update Stock / Price")
        products = get_all_products()
        if not products:
            st.info("No products available.")
            return

        options = {f"{p['name']} ({p['category']})": p for p in products}
        sel = st.selectbox("Select Product", list(options.keys()), key="upd_sel")
        prod = options[sel]

        st.markdown(f"""
        <div class='section-card'>
          <b>{prod['name']}</b> &nbsp;|&nbsp; Category: {prod['category']}<br>
          Current Price: <b>₹{prod['price']:.2f}</b> &nbsp;|&nbsp;
          Current Stock: <b>{prod['quantity']} units</b>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            new_qty = st.number_input("New Stock Quantity", min_value=0,
                                     value=prod["quantity"], step=1)
            if st.button("📦 Update Stock", use_container_width=True):
                update_stock(prod["id"], new_qty)
                st.success("Stock updated!")
                st.rerun()
        with c2:
            new_price = st.number_input("New Price (₹)", min_value=0.01,
                                       value=float(prod["price"]), step=0.5,
                                       format="%.2f")
            if st.button("💰 Update Price", use_container_width=True):
                update_price(prod["id"], new_price)
                st.success("Price updated!")
                st.rerun()

        st.divider()
        st.markdown("#### 🗑️ Delete Product")
        if st.button(f"⚠️ Delete '{prod['name']}'", type="secondary"):
            st.session_state["confirm_delete"] = prod["id"]

        if st.session_state.get("confirm_delete") == prod["id"]:
            st.warning(f"Are you sure you want to delete **{prod['name']}**?")
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("✅ Yes, Delete", use_container_width=True):
                    delete_product(prod["id"])
                    st.session_state.pop("confirm_delete", None)
                    st.success("Deleted.")
                    st.rerun()
            with cc2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.pop("confirm_delete", None)
                    st.rerun()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _render_stock_metrics(products):
    total  = len(products)
    low    = sum(1 for p in products if 0 < p["quantity"] <= LOW_STOCK_THRESHOLD)
    out    = sum(1 for p in products if p["quantity"] == 0)
    value  = sum(p["price"] * p["quantity"] for p in products)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Products",  total)
    c2.metric("Low Stock Items", low,  delta=f"-{low}" if low else None,
              delta_color="inverse")
    c3.metric("Out of Stock",    out,  delta=f"-{out}" if out else None,
              delta_color="inverse")
    c4.metric("Inventory Value", f"₹{value:,.0f}")
    st.markdown("")


def _render_stock_table(products):
    rows = []
    for p in products:
        if p["quantity"] == 0:
            status = "🔴 Out of Stock"
        elif p["quantity"] <= LOW_STOCK_THRESHOLD:
            status = "🟡 Low Stock"
        else:
            status = "🟢 In Stock"

        rows.append({
            "ID":          p["id"],
            "Product":     p["name"],
            "Category":    p["category"],
            "Price (₹)":   f"{p['price']:.2f}",
            "Stock (Qty)": p["quantity"],
            "Stock Value": f"₹{p['price']*p['quantity']:,.0f}",
            "Status":      status,
        })

    df = pd.DataFrame(rows)

    def highlight_row(row):
        if "Out" in str(row["Status"]):
            return ["background-color:#ffe0e0"] * len(row)
        elif "Low" in str(row["Status"]):
            return ["background-color:#fff9e0"] * len(row)
        return [""] * len(row)

    styled = df.style.apply(highlight_row, axis=1)
    st.dataframe(styled, use_container_width=True, hide_index=True)
