# SpendSmart — Student Expense Tracker

SpendSmart is a simple budgeting dashboard for students. It lets users record expenses, group spending by category, track a monthly budget, view a chart and download expense records.

## Features
- Add and delete expenses
- Categorise spending
- Monthly spend, remaining-budget and transaction metrics
- Budget usage indicator and warning
- Category pie chart and automatic spending insight
- CSV persistence and CSV download

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

## Technology
Python, Streamlit, Pandas, Plotly, CSV.

## Data and privacy
Expense records are stored in `expenses.csv` on the machine running the app. Do not enter sensitive financial information into a public demo.

## Hackathon notes
This is a starter prototype. Update this README with the actual changes you make in response to each Grevix AfterCode Challenge Card. Clearly disclose any AI tools used and review/test generated code before submission.
