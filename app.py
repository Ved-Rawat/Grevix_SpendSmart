import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import date

st.set_page_config(page_title="SpendSmart", page_icon="💸", layout="wide")
DATA_FILE = Path("expenses.csv")
CATEGORIES = ["Food", "Travel", "Education", "Shopping", "Entertainment", "Health", "Other"]

def load_expenses():
    columns = ["ID", "Date", "Category", "Amount", "Note"]
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            for col in columns:
                if col not in df.columns:
                    df[col] = None
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
            return df[columns]
        except (pd.errors.ParserError, OSError):
            st.warning("Could not read expenses.csv. Starting with an empty expense list.")
    return pd.DataFrame(columns=columns)

def save_expenses(df):
    df.to_csv(DATA_FILE, index=False)

st.title("💸 SpendSmart")
st.write("A simple student expense tracker that helps you understand spending and stay within budget.")
st.caption("Demo project for Grevix AfterCode 2026 • Python • Streamlit • Pandas • Plotly")

with st.sidebar:
    st.header("Budget settings")
    budget = st.number_input("Monthly budget (₹)", min_value=0, value=5000, step=500)
    st.caption("Demo data is stored in a local CSV file.")

df = load_expenses()
with st.expander("➕ Add a new expense", expanded=True):
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            expense_date = st.date_input("Date", value=date.today())
            category = st.selectbox("Category", CATEGORIES)
        with col2:
            amount = st.number_input("Amount (₹)", min_value=1.0, value=100.0, step=10.0)
            note = st.text_input("Description (optional)", max_chars=120)
        submitted = st.form_submit_button("Save expense", type="primary")
    if submitted:
        next_id = int(pd.to_numeric(df["ID"], errors="coerce").max()) + 1 if not df.empty and pd.to_numeric(df["ID"], errors="coerce").notna().any() else 1
        new_row = pd.DataFrame([{
            "ID": next_id, "Date": pd.Timestamp(expense_date),
            "Category": category, "Amount": float(amount), "Note": note.strip()
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        save_expenses(df)
        st.success("Expense saved.")
        st.rerun()

today = pd.Timestamp(date.today())
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    month_df = df[(df["Date"].dt.month == today.month) & (df["Date"].dt.year == today.year)].copy()
else:
    month_df = df.copy()

total = float(month_df["Amount"].sum()) if not month_df.empty else 0.0
remaining = budget - total
c1, c2, c3 = st.columns(3)
c1.metric("Spent this month", f"₹{total:,.2f}")
c2.metric("Budget remaining", f"₹{remaining:,.2f}", delta=f"{remaining:,.2f} vs zero")
c3.metric("Transactions this month", str(len(month_df)))

if budget > 0:
    st.progress(min(total / budget, 1.0), text=f"{min(total / budget * 100, 100):.0f}% of monthly budget used")
if total > budget:
    st.error("Budget exceeded. Review your recent expenses.")
elif budget > 0 and total >= budget * 0.8:
    st.warning("You have used at least 80% of your monthly budget.")
else:
    st.success("You're within your monthly budget.")

left, right = st.columns(2)
with left:
    st.subheader("Spending by category")
    if not month_df.empty:
        grouped = month_df.groupby("Category", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
        fig = px.pie(grouped, names="Category", values="Amount", hole=0.42, title="This month's expenses")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add an expense to see your chart.")
with right:
    st.subheader("Quick insight")
    if not month_df.empty:
        by_category = month_df.groupby("Category")["Amount"].sum()
        top_category = by_category.idxmax()
        share = (by_category.max() / total * 100) if total else 0
        st.write(f"Your highest spending category is **{top_category}**.")
        st.write(f"It accounts for **{share:.1f}%** of your spending this month.")
        if budget > 0:
            st.write(f"You have **₹{remaining:,.2f}** {'left' if remaining >= 0 else 'over budget'} against your monthly budget.")
    else:
        st.write("Your spending insights will appear after you add your first expense.")
    st.caption("Insights are calculated from your recorded data; no external AI service is used.")

st.subheader("Expense history")
if not month_df.empty:
    display_df = month_df.sort_values("Date", ascending=False).copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download this month's expenses (CSV)", data=month_df.to_csv(index=False).encode("utf-8"), file_name="spendsmart-expenses.csv", mime="text/csv")
    ids = month_df["ID"].dropna().tolist()
    if ids:
        with st.form("delete_form"):
            selected_id = st.selectbox("Transaction ID to delete", options=ids, format_func=lambda x: f"Transaction #{int(x)}")
            delete = st.form_submit_button("Delete selected transaction")
        if delete:
            df = df[df["ID"] != selected_id]
            save_expenses(df)
            st.success("Expense deleted.")
            st.rerun()
else:
    st.info("No expenses recorded this month yet.")

st.caption("SpendSmart is a hackathon prototype. CSV storage is local to the machine running the app.")
