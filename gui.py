# ------------ gui.py -----------

#The Tkinter GUI for LedgerWise. Contains only widget/display logic —
#all data loading and calculations are imported from Personal_Finance_Manager.py so
#this file stays focused on presentation.

import tkinter as tk
from tkinter import ttk
from datetime import date

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Personal_Finance_Manager import load_all_data, track_budgets, forecast_budgets


class LedgerWiseApp:
    # Main application window for LedgerWise.
    # Holds the notebook (tabbed interface) and creates each tab's frame.
    def __init__(self, root, accounts_list, budgets_list, transactions_list):
        self.root = root
        self.root.title("LedgerWise")
        self.root.geometry("900x600")

        # Store the in-memory data so any tab-building method can access it
        self.accounts_list = accounts_list
        self.budgets_list = budgets_list
        self.transactions_list = transactions_list

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.dashboard_tab = ttk.Frame(self.notebook)
        self.transactions_tab = ttk.Frame(self.notebook)
        self.budgets_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)
    #Creating the dashboards
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.transactions_tab, text="Transactions")
        self.notebook.add(self.budgets_tab, text="Budgets")
        self.notebook.add(self.reports_tab, text="Reports")

        self.build_dashboard_tab()
        self.build_transactions_tab()
        self.build_budgets_tab()
        self.build_reports_tab()

    def build_dashboard_tab(self):
        # Builds the Dashboard tab: this month's income, expenses, net
        # cashflow, and a warning list of categories at risk of going
        # over budget.
        current_month = date.today().strftime("%Y-%m")

        # --- Calculate this month's totals from transactions_list ---
        #This is done to allow for better flexibility rather than a
        #Hard coded value in the table
        income = 0.0
        expenses = 0.0
        for t in self.transactions_list:
            if t["Date"].strftime("%Y-%m") == current_month:
                if t["Amount"] > 0:
                    income += t["Amount"]
                else:
                    expenses += abs(t["Amount"])

        net_cashflow = income - expenses

        # --- Summary labels ---
        title = ttk.Label(self.dashboard_tab, text=f"Dashboard — {current_month}", font=("Arial", 16, "bold"))
        title.pack(pady=(20, 10))

        summary_frame = ttk.Frame(self.dashboard_tab)
        summary_frame.pack(pady=10)

        ttk.Label(summary_frame, text=f"Income: £{income:.2f}", font=("Arial", 12)).grid(row=0, column=0, padx=20)
        ttk.Label(summary_frame, text=f"Expenses: £{expenses:.2f}", font=("Arial", 12)).grid(row=0, column=1, padx=20)

        cashflow_colour = "green" if net_cashflow >= 0 else "red"
        ttk.Label(summary_frame, text=f"Net: £{net_cashflow:.2f}", font=("Arial", 12, "bold"),
                foreground=cashflow_colour).grid(row=0, column=2, padx=20)

        # --- Budget warnings using existing tracking/forecasting logic ---
        status = track_budgets(self.transactions_list, self.budgets_list)
        forecast = forecast_budgets(status)

        warnings_label = ttk.Label(self.dashboard_tab, text="Budget Watch", font=("Arial", 13, "bold"))
        warnings_label.pack(pady=(20, 5))

        current_month_forecasts = [
            f for f in forecast
            if f["Month"] == current_month and f["Projected Over Budget"]
        ]

        if current_month_forecasts:
            for f in current_month_forecasts:
                warning_text = (
                    f" {f['Category']}: on track to be £{f['Projected Overspend']:.2f} "
                    f"over budget by month-end"
                )
                ttk.Label(self.dashboard_tab, text=warning_text, foreground="red").pack(anchor="w", padx=40)
        else:
            ttk.Label(self.dashboard_tab, text="No categories currently at risk.", foreground="green").pack(padx=40)

    def build_transactions_tab(self):
        """Placeholder content for the Transactions tab."""
        label = ttk.Label(self.transactions_tab, text="Transactions — table will go here", font=("Arial", 14))
        label.pack(pady=20)

    def build_budgets_tab(self):
        """Placeholder content for the Budgets tab."""
        label = ttk.Label(self.budgets_tab, text="Budgets — progress bars will go here", font=("Arial", 14))
        label.pack(pady=20)

# ----------- Reports Section -------------

    def build_reports_tab(self):
        # Builds the Reports tab: a pie chart of spending by category,
        # with a dropdown to pick which month to view.

        # --- Work out which months actually have data, most recent first ---
        months_with_data = sorted(
            {t["Date"].strftime("%Y-%m") for t in self.transactions_list},
            reverse=True
        )

        if not months_with_data:
            ttk.Label(self.reports_tab, text="No transaction data available.",
                    font=("Arial", 14)).pack(pady=20)
            return

        # --- Controls row: label + dropdown ---
        controls_frame = ttk.Frame(self.reports_tab)
        controls_frame.pack(pady=(20, 10))

        ttk.Label(controls_frame, text="Month:", font=("Arial", 11)).pack(side="left", padx=(0, 8))

        self.selected_month = tk.StringVar(value=months_with_data[0])
        month_dropdown = ttk.Combobox(
            controls_frame,
            textvariable=self.selected_month,
            values=months_with_data,
            state="readonly",  # user can only pick from the list, not type freely
            width=10
        )
        month_dropdown.pack(side="left")
        # Redraw the chart whenever a new month is selected
        month_dropdown.bind("<<ComboboxSelected>>", lambda event: self.draw_spending_pie_chart())

        # --- Frame that will hold the matplotlib canvas ---
        # Kept as its own frame (rather than reports_tab directly) so we can
        # destroy and rebuild just the chart on redraw, without touching the dropdown above.
        self.chart_frame = ttk.Frame(self.reports_tab)
        self.chart_frame.pack(fill="both", expand=True)

        self.draw_spending_pie_chart()

    def draw_spending_pie_chart(self):
        # Draws (or redraws) a pie chart of spending by category for
        # whichever month is currently selected in the dropdown.
        # Clear out any previously drawn chart before drawing a new one

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        selected_month = self.selected_month.get()

        # --- Sum expenses by category for the selected month ---
        category_totals = {}
        for t in self.transactions_list:
            if t["Date"].strftime("%Y-%m") == selected_month and t["Amount"] < 0:
                category = t["Category"]
                category_totals[category] = category_totals.get(category, 0.0) + abs(t["Amount"])

        if not category_totals:
            ttk.Label(self.chart_frame, text=f"No spending recorded for {selected_month}.",
                    font=("Arial", 12)).pack(pady=20)
            return

        # --- Build the pie chart ---
        figure = Figure(figsize=(6, 5), dpi=100)
        axes = figure.add_subplot(111)

        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        axes.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
        axes.set_title(f"Spending by Category — {selected_month}")

        # Embed the matplotlib figure inside the Tkinter frame
        canvas = FigureCanvasTkAgg(figure, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def main():
    # load_all_data() prints a clear message and exits (sys.exit(1)) if
    # any CSV is missing, malformed, or has the wrong columns — no need
    # to catch anything here, the GUI simply won't open on bad data.
    accounts_list, budgets_list, transactions_list = load_all_data(
        "accounts.csv", "budgets.csv", "transactions.csv"
    )

    root = tk.Tk()
    app = LedgerWiseApp(root, accounts_list, budgets_list, transactions_list)
    root.mainloop()


if __name__ == "__main__":
    main()