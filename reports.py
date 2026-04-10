import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import (get_sales, get_daily_summary,
                      get_monthly_summary, get_category_summary)


def reports_page():
    st.markdown("""
    <div class='shop-header'>
      <h1>📊 Sales Reports</h1>
      <p>Track daily, monthly and category-wise performance</p>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📅 Daily", "📆 Monthly", "🏷️ By Category", "🧾 All Transactions"]
    )

    # ── TAB 1: Daily ──────────────────────────────────────────────────────────
    with tab1:
        st.markdown("#### 📅 Daily Sales (Last 30 Days)")
        rows = get_daily_summary()
        if not rows:
            st.info("No sales data yet.")
        else:
            df = pd.DataFrame(rows).rename(columns={
                "day": "Date", "transactions": "Transactions", "revenue": "Revenue (₹)"
            })
            df["Revenue (₹)"] = df["Revenue (₹)"].apply(lambda x: f"₹{x:,.2f}")

            # KPIs for today
            today_str = date.today().strftime("%Y-%m-%d")
            today_rows = [r for r in rows if r["day"] == today_str]
            yesterday_rows = []  # simplification

            c1, c2, c3 = st.columns(3)
            if today_rows:
                c1.metric("Today's Revenue",      f"₹{today_rows[0]['revenue']:,.2f}")
                c2.metric("Today's Transactions",  today_rows[0]["transactions"])
            else:
                c1.metric("Today's Revenue",      "₹0.00")
                c2.metric("Today's Transactions",  0)
            c3.metric("Days Tracked", len(rows))

            st.markdown("")
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Simple bar-like visualization using st.bar_chart
            chart_df = pd.DataFrame(rows)
            chart_df["Revenue"] = chart_df["revenue"]
            chart_df = chart_df.set_index("day")[["Revenue"]]
            st.bar_chart(chart_df, use_container_width=True)

    # ── TAB 2: Monthly ────────────────────────────────────────────────────────
    with tab2:
        st.markdown("#### 📆 Monthly Sales Summary")
        rows = get_monthly_summary()
        if not rows:
            st.info("No sales data yet.")
        else:
            df = pd.DataFrame(rows).rename(columns={
                "month": "Month", "transactions": "Transactions", "revenue": "Revenue (₹)"
            })

            total_revenue = sum(r["revenue"] for r in rows)
            total_txns    = sum(r["transactions"] for r in rows)
            best_month    = max(rows, key=lambda r: r["revenue"])

            c1, c2, c3 = st.columns(3)
            c1.metric("All-Time Revenue",    f"₹{total_revenue:,.2f}")
            c2.metric("Total Transactions",   total_txns)
            c3.metric("Best Month",           f"{best_month['month']}  ₹{best_month['revenue']:,.0f}")

            df["Revenue (₹)"] = df["Revenue (₹)"].apply(lambda x: f"₹{x:,.2f}")
            st.markdown("")
            st.dataframe(df, use_container_width=True, hide_index=True)

            chart_df = pd.DataFrame(rows).set_index("month")[["revenue"]].rename(
                columns={"revenue": "Revenue"}
            )
            st.bar_chart(chart_df, use_container_width=True)

    # ── TAB 3: By Category ────────────────────────────────────────────────────
    with tab3:
        st.markdown("#### 🏷️ Revenue by Product Category")
        rows = get_category_summary()
        if not rows:
            st.info("No sales data yet.")
        else:
            total = sum(r["revenue"] for r in rows)
            cols  = st.columns(len(rows)) if len(rows) <= 4 else st.columns(4)
            for i, row in enumerate(rows):
                cols[i % len(cols)].metric(
                    row["category"],
                    f"₹{row['revenue']:,.2f}",
                    f"{row['revenue']/total*100:.1f}%"
                )

            df = pd.DataFrame(rows).rename(columns={
                "category": "Category",
                "transactions": "Transactions",
                "revenue": "Revenue (₹)"
            })
            df["Revenue (₹)"] = df["Revenue (₹)"].apply(lambda x: f"₹{x:,.2f}")
            st.markdown("")
            st.dataframe(df, use_container_width=True, hide_index=True)

            chart_df = pd.DataFrame(rows).set_index("category")[["revenue"]].rename(
                columns={"revenue": "Revenue"}
            )
            st.bar_chart(chart_df, use_container_width=True)

    # ── TAB 4: All Transactions ───────────────────────────────────────────────
    with tab4:
        st.markdown("#### 🧾 Transaction History")

        c1, c2, c3 = st.columns(3)
        with c1:
            filter_type = st.radio("Filter by", ["All", "Date", "Month"],
                                   horizontal=True, key="txn_filter")
        with c2:
            if filter_type == "Date":
                sel_date = st.date_input("Pick Date", value=date.today(), key="txn_date")
                df_filter = str(sel_date)
            elif filter_type == "Month":
                months = sorted({r["date"][:7] for r in get_sales()}, reverse=True)
                sel_month = st.selectbox("Pick Month", months if months else ["—"],
                                         key="txn_month")
                df_filter = sel_month
            else:
                df_filter = None
        with c3:
            st.markdown("")

        sales = get_sales(df_filter)
        if not sales:
            st.info("No transactions found.")
        else:
            df = pd.DataFrame(sales)[[
                "date", "customer", "product", "quantity",
                "unit_price", "subtotal", "gst", "total"
            ]].rename(columns={
                "date":       "Date & Time",
                "customer":   "Customer",
                "product":    "Product",
                "quantity":   "Qty",
                "unit_price": "Unit Price (₹)",
                "subtotal":   "Subtotal (₹)",
                "gst":        "GST (₹)",
                "total":      "Total (₹)",
            })

            # Format numeric columns
            for col in ["Unit Price (₹)", "Subtotal (₹)", "GST (₹)", "Total (₹)"]:
                df[col] = df[col].apply(lambda x: f"₹{float(x):,.2f}")

            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown(f"**{len(sales)} transaction(s) found** | "
                        f"Total: ₹{sum(float(s['total']) for s in sales):,.2f}")

            # CSV download
            csv = pd.DataFrame(sales).to_csv(index=False).encode()
            st.download_button("⬇️ Export as CSV", csv,
                               "sales_report.csv", "text/csv")
