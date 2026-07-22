# LedgerWise

**Personal Finance Tracker, Budgeter & Forecaster**

## Identifying Information

| | |
|---|---|
| **Name** | Emmanuel Mugaine |
| **P-Number** | P509970 |
| **Student ID Number** | 303065252 |
| **Course Code** | IY499 — Introduction to Programming |
| **Assessment** | Practical Programming Assignment |

## Declaration of Own Work

**I confirm that this assignment is my own work.**
**Where I have referred to online sources, I have provided comments detailing the reference and included a link to the source.**

## Description

LedgerWise is a desktop personal finance application built in Python with a Tkinter graphical interface. It tracks income and expenses from a single checking account, compares actual spending against a per-category monthly budget, and provides a simple rule-based forecast of whether the user is on track to stay within budget by the end of the current month.

The application loads account, budget, and transaction data from three CSV files at startup, and presents everything through four tabs: a Dashboard summarising income, expenses, net cashflow, and at-risk budget categories for a selectable month; a Transactions tab with a sortable, searchable table of every transaction; a Budgets tab showing spend-vs-budget progress bars per category; and a Reports tab with a pie chart of spending by category, again filterable by month.

Under the hood, LedgerWise uses a custom-written merge sort to order transactions by date or amount, a binary search to find all transactions on an exact date, and a linear search to find transactions by partial company name or description text. Budget comparisons and the month-end forecast are calculated on demand from the loaded transaction data, rather than stored separately, to avoid the figures ever falling out of sync with the underlying transactions.

A short splash screen introduces the application before the main window opens. All data loading is validated on startup — missing files, incorrect columns, and malformed rows are caught and reported clearly rather than allowed to silently corrupt calculations or crash with a raw Python traceback.

## Packages / Libraries Used

- **matplotlib** — renders the spending-by-category pie chart, embedded in the Tkinter window via `matplotlib.backends.backend_tkagg`
- **tkinter** (Python standard library) — the graphical user interface
- **csv** (Python standard library) — reading the accounts, budgets, and transactions CSV files
- **datetime / calendar** (Python standard library) — date parsing, comparison, and days-in-month calculations for forecasting

*A full pinned list of dependencies is provided in `requirements.txt`.*

## Installation Instructions

1. Ensure Python 3.10 or later is installed. It is available via the university Software Centre, or free from [python.org](https://www.python.org) for personal machines.

2. Download or clone the repository:
   ```
   git clone https://github.com/EmmanuelMugaine/IY499-Final-intro-to-programming-project.git
   ```

3. Install the required package:
   ```
   pip install -r requirements.txt
   ```

## Instructions on How to Run the Program

1. Make sure `accounts.csv`, `budgets.csv`, and `transactions.csv` are present in the same folder as `gui.py`.

2. Run the application from the project folder:
   ```
   python gui.py
   ```

3. Click **"Continue"** on the welcome screen to open the main application.

4. Use the tabs across the top (**Dashboard**, **Transactions**, **Budgets**, **Reports**) to navigate. Most tabs include a month dropdown to change which period is displayed.

*Note: `ledgerwise.py` can also be run directly (`python ledgerwise.py`) to execute the core logic from the command line without the GUI — useful for testing the sorting, searching, and budget logic in isolation.*

## Repository Link

*https://github.com/EmmanuelMugaine/IY499-Final-intro-to-programming-project.git*

## Refrences
Matthes, E. (2015) Python crash course: a hands-on, project-based introduction to programming [PDF]. San Francisco: No Starch Press. Available at: https://indiachinainstitute.org/wp-content/uploads/2018/05/Python-Crash-Course.pdf (Accessed: 22 July 2026).
