import csv  #For dictreader and dictwriter
from datetime import date, datetime #Converting string date values into actual dates
import sys 
#Imports for the window and the dashboard tabs
import tkinter as tk
from tkinter import ttk

class DataLoadError(Exception):
    # Custom exception for problems loading App data files.
    pass

#-------- Loading CSV data with Error Handling -----------

def load_accounts(filename):

    #Loads accounts from a CSV file into a list of dictionaries.
    #Raises DataLoadError with a clear message if the file is missing,
    #has the wrong columns, or contains a malformed row.

    expected_columns = {"Account ID", "Account Name"}
    loaded_accounts = []    #Empty list to append later
    #Using a try block to handle problematic code
    try:
        with open(filename, "r", newline="") as accounts:   #Opening chosen file
            account_reader = csv.DictReader(accounts)
            #Formatting table
            actual_columns = set(account_reader.fieldnames or [])
            if actual_columns != expected_columns:
                missing = expected_columns - actual_columns
                unexpected = actual_columns - expected_columns
                raise DataLoadError(
                    f"'{filename}' has incorrect columns. "
                    f"Missing: {missing or 'none'}. Unexpected: {unexpected or 'none'}."
                )

            for row_number, row in enumerate(account_reader, start=2):
                try:
                    if not row["Account ID"].strip():
                        raise ValueError("Account ID cannot be empty")
                    if not row["Account Name"].strip():
                        raise ValueError("Account Name cannot be empty")

                    loaded_accounts.append({
                        "Account ID": row["Account ID"],
                        "Account Name": row["Account Name"]
                    })
                except ValueError as e:
                    raise DataLoadError(
                        f"'{filename}', row {row_number}: invalid data ({e}). "
                        f"Row contents: {row}"
                    )
#Displaying Error to user
    except FileNotFoundError:
        raise DataLoadError(f"Could not find file '{filename}'. Check the file path and try again.")

    return loaded_accounts


def load_budget(filename):

    #Loads budgets from a CSV file into a list of dictionaries.
    #Raises DataLoadError with a clear message if the file is missing,
    #has the wrong columns, or contains a malformed row.

    expected_columns = {"Account ID", "Category", "Budget Amount"}
    loaded_budgets = []

    try:
        with open(filename, "r", newline="") as budget:
            budget_reader = csv.DictReader(budget)

            actual_columns = set(budget_reader.fieldnames or [])
            if actual_columns != expected_columns:
                missing = expected_columns - actual_columns
                unexpected = actual_columns - expected_columns
                raise DataLoadError(
                    f"'{filename}' has incorrect columns. "
                    f"Missing: {missing or 'none'}. Unexpected: {unexpected or 'none'}."
                )

            for row_number, row in enumerate(budget_reader, start=2):
                try:
                    budget_amount = float(row["Budget Amount"])
                    if budget_amount < 0:
                        raise ValueError("Budget Amount cannot be negative")

                    loaded_budgets.append({
                        "Account ID": row["Account ID"],
                        "Category": row["Category"],
                        "Budget Amount": budget_amount
                    })
                except ValueError as e:
                    raise DataLoadError(
                        f"'{filename}', row {row_number}: invalid data ({e}). "
                        f"Row contents: {row}"
                    )

    except FileNotFoundError:
        raise DataLoadError(f"Could not find file '{filename}'. Check the file path and try again.")

    return loaded_budgets

def load_transactions(filename):  #Loads transactions from a CSV file into a list of dictionaries.

    #Raises DataLoadError with a clear message if the file is missing,
    #has the wrong columns, or contains a malformed row.

    expected_columns = {"Account ID", "Date", "Company Name", "Amount", "Category", "Description"}
    loaded_transactions = []

    try:
        with open(filename, "r", newline="") as transactions:
            transaction_reader = csv.DictReader(transactions)

            # Check the header row matches what we expect BEFORE reading any data
            actual_columns = set(transaction_reader.fieldnames or [])
            if actual_columns != expected_columns:
                missing = expected_columns - actual_columns
                unexpected = actual_columns - expected_columns
                raise DataLoadError(
                    f"'{filename}' has incorrect columns. "
                    f"Missing: {missing or 'none'}. Unexpected: {unexpected or 'none'}."
                )

            # enumerate starts at 2 because row 1 is the header
            for row_number, row in enumerate(transaction_reader, start=2):
                try:
                    loaded_transactions.append({
                        "Account ID": row["Account ID"],
                        "Date": datetime.strptime(row["Date"], "%Y-%m-%d").date(),
                        "Company Name": row["Company Name"],
                        "Amount": float(row["Amount"]),
                        "Category": row["Category"],
                        "Description": row["Description"]
                    })
                except ValueError as e:
                    raise DataLoadError(
                        f"'{filename}', row {row_number}: invalid data ({e}). "
                        f"Row contents: {row}"
                    )
#Displaying error and potential fix to the user
    except FileNotFoundError:
        raise DataLoadError(f"Could not find file '{filename}'. Check the file path and try again.")

    return loaded_transactions

def load_all_data(accounts_file, budgets_file, transactions_file):
    #Loads all three LedgerWise data files together.
    #If any file fails to load, prints a clear error and exits the program
    #cleanly rather than crashing with a raw traceback.
    #Returns (accounts_list, budgets_list, transactions_list) on success.
    try:
        accounts_list = load_accounts(accounts_file)
        budgets_list = load_budget(budgets_file)
        transactions_list = load_transactions(transactions_file)
    except DataLoadError as e:
        print(f"LedgerWise could not start: {e}")
        sys.exit(1)  # Exit with a non-zero code to signal failure

    return accounts_list, budgets_list, transactions_list

#  Linear Search (generic, partial text match)

def linear_search(data, search_text, key):
    # Searches ANY list (sorted or not) for items whose key value
    # contains 'search_text' as a substring (case-insensitive).

    search_text_lower = search_text.lower()
    results = []

    for item in data:  # Checks every item in turn — O(n), no sorting required
        if search_text_lower in key(item).lower():
            results.append(item)

    return results


#--------- Merge Sort (generic, sorts by any key) -----------
def merge_sort(data, key):     #'key' is a function that extracts the value to compare
    #e.g. key=lambda x: x["Amount"]

    #Sorts a list of dictionaries using merge sort.
    
    if len(data) <= 1:
        return data  # Base case: a list of 0 or 1 items is already sorted

    mid = len(data) // 2
    left_half = data[:mid]
    right_half = data[mid:]

    # Recursively split both halves
    left_sorted = merge_sort(left_half, key)
    right_sorted = merge_sort(right_half, key)

    # Merge the two sorted halves together
    return merge(left_sorted, right_sorted, key)


def merge(left, right, key):
    merged = []
    i = j = 0  # Pointers into left and right lists

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any leftover items (one side will still have items left)
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


#--------- Binary Search (generic, searches by any key) -----------
#Displays all transactions if sorted by date
def binary_search(sorted_data, target, key):
    #Searches a list that has ALREADY been sorted by 'key' for an
    #item whose key value equals the 'target'.
    
    #Returns the matching item, or None if not found.
    low = 0
    high = len(sorted_data) - 1
    found_index = None

    # Step 1: standard binary search to find ONE matching index
    while low <= high:
        mid = (low + high) // 2
        mid_value = key(sorted_data[mid])

        if mid_value == target:
            found_index = mid
            break
        elif mid_value < target:
            low = mid + 1
        else:
            high = mid - 1

    if found_index is None:
        return []  # No matches at all

    # Step 2: scan outward from found_index to collect every match
    results = [sorted_data[found_index]]

    # Scan left
    i = found_index - 1
    while i >= 0 and key(sorted_data[i]) == target:
        results.append(sorted_data[i])
        i -= 1

    # Scan right
    j = found_index + 1
    while j < len(sorted_data) and key(sorted_data[j]) == target:
        results.append(sorted_data[j])
        j += 1

    return results


#--------- Budget Tracking Logic -----------
    #Compares actual spending against budgeted amounts, grouped by
    #Account ID, Category, and Month (YYYY-MM).
def track_budgets(transactions, budgets):    #Returns a list of dictionaries summarising each group.

    # Step 1: Group transaction totals by (Account ID, Category, Year-Month)
    spending = {}  # key: (account_id, category, "YYYY-MM") -> total spent

    for t in transactions:
        # Only track spending (negative amounts / expenses)
        if t["Amount"] < 0:
            year_month = t["Date"].strftime("%Y-%m")
            group_key = (t["Account ID"], t["Category"], year_month)

            if group_key not in spending:
                spending[group_key] = 0.0
            spending[group_key] += abs(t["Amount"])

    # Step 2: Compare each budget entry against the grouped spending
    budget_status = []

    for b in budgets:
        account_id = b["Account ID"]
        category = b["Category"]
        budget_amount = b["Budget Amount"]

        # Find every month that has spending for this account/category
        matching_months = [
            key[2] for key in spending
            if key[0] == account_id and key[1] == category
        ]

        for month in matching_months:
            spent = spending[(account_id, category, month)]
            remaining = budget_amount - spent
            percent_used = (spent / budget_amount * 100) if budget_amount > 0 else 0

            budget_status.append({
                "Account ID": account_id,
                "Category": category,
                "Month": month,
                "Budgeted": budget_amount,
                "Spent": round(spent, 2),
                "Remaining": round(remaining, 2),
                "Percent Used": round(percent_used, 1),
                "Over Budget": spent > budget_amount
            })

    return budget_status

from calendar import monthrange

#--------- Rule-based Forecasting -----------
def forecast_budgets(budget_status, today=None):
    #Takes the output of track_budgets() and adds a linear projection
    #for the CURRENT month only (past months already have real totals).

    if today is None:
        today = date.today()

    current_month_str = today.strftime("%Y-%m")
    days_elapsed = today.day  # e.g. if today is the 15th, 15 days have elapsed

    forecast_results = []

    for entry in budget_status:
        # Copy the existing entry so we don't mutate the original
        forecast_entry = dict(entry)

        if entry["Month"] == current_month_str:
            year, month = map(int, entry["Month"].split("-"))
            days_in_month = monthrange(year, month)[1]

            spent_so_far = entry["Spent"]
            daily_rate = spent_so_far / days_elapsed if days_elapsed > 0 else 0
            projected_total = daily_rate * days_in_month

            forecast_entry["Projected Total"] = round(projected_total, 2)
            forecast_entry["Projected Over Budget"] = projected_total > entry["Budgeted"]
            forecast_entry["Projected Overspend"] = round(
                max(0, projected_total - entry["Budgeted"]), 2
            )
        else:
            # Past months: no projection needed, actuals are final
            forecast_entry["Projected Total"] = entry["Spent"]
            forecast_entry["Projected Over Budget"] = entry["Over Budget"]
            forecast_entry["Projected Overspend"] = round(
                max(0, entry["Spent"] - entry["Budgeted"]), 2
            )

        forecast_results.append(forecast_entry)

    return forecast_results

class DataLoadError(Exception):
    #Custom exception for problems loading LedgerWise data files.
    pass


def load_transactions(filename):  # Loads transactions from a CSV file into a list of dictionaries.
    # Raises DataLoadError with a clear message if the file is missing,
    # has the wrong columns, or contains a malformed row.

    expected_columns = {"Account ID", "Date", "Company Name", "Amount", "Category", "Description"}
    loaded_transactions = []

    try:
        with open(filename, "r", newline="") as transactions:
            transaction_reader = csv.DictReader(transactions)

            # Check the header row matches what we expect BEFORE reading any data
            actual_columns = set(transaction_reader.fieldnames or [])
            if actual_columns != expected_columns:
                missing = expected_columns - actual_columns
                unexpected = actual_columns - expected_columns
                raise DataLoadError(
                    f"'{filename}' has incorrect columns. "
                    f"Missing: {missing or 'none'}. Unexpected: {unexpected or 'none'}."
                )

            # enumerate starts at 2 because row 1 is the header
            for row_number, row in enumerate(transaction_reader, start=2):
                try:
                    loaded_transactions.append({
                        "Account ID": row["Account ID"],
                        "Date": datetime.strptime(row["Date"], "%Y-%m-%d").date(),
                        "Company Name": row["Company Name"],
                        "Amount": float(row["Amount"]),
                        "Category": row["Category"],
                        "Description": row["Description"]
                    })
                except ValueError as e:
                    raise DataLoadError(
                        f"'{filename}', row {row_number}: invalid data ({e}). "
                        f"Row contents: {row}"
                    )

    except FileNotFoundError:
        raise DataLoadError(f"Could not find file '{filename}'. Check the file path and try again.")

    return loaded_transactions

def load_accounts(filename):  # Loads accounts from a CSV file into a list of dictionaries.
    # Raises DataLoadError with a clear message if the file is missing,
    # has the wrong columns, or contains a malformed row.

    expected_columns = {"Account ID", "Account Name"}
    loaded_accounts = []

    try:
        with open(filename, "r", newline="") as accounts:
            account_reader = csv.DictReader(accounts)

            actual_columns = set(account_reader.fieldnames or [])
            if actual_columns != expected_columns:
                missing = expected_columns - actual_columns
                unexpected = actual_columns - expected_columns
                raise DataLoadError(
                    f"'{filename}' has incorrect columns. "
                    f"Missing: {missing or 'none'}. Unexpected: {unexpected or 'none'}."
                )

            for row_number, row in enumerate(account_reader, start=2):
                try:
                    if not row["Account ID"].strip():
                        raise ValueError("Account ID cannot be empty")
                    if not row["Account Name"].strip():
                        raise ValueError("Account Name cannot be empty")

                    loaded_accounts.append({
                        "Account ID": row["Account ID"],
                        "Account Name": row["Account Name"]
                    })
                except ValueError as e:
                    raise DataLoadError(
                        f"'{filename}', row {row_number}: invalid data ({e}). "
                        f"Row contents: {row}"
                    )

    except FileNotFoundError:
        raise DataLoadError(f"Could not find file '{filename}'. Check the file path and try again.")

    return loaded_accounts


def load_budget(filename): # Loads budgets from a CSV file into a list of dictionaries.
    # Raises DataLoadError with a clear message if the file is missing,
    # has the wrong columns, or contains a malformed row.
    expected_columns = {"Account ID", "Category", "Budget Amount"}
    loaded_budgets = []

    try:
        with open(filename, "r", newline="") as budget:
            budget_reader = csv.DictReader(budget)

            actual_columns = set(budget_reader.fieldnames or [])
            if actual_columns != expected_columns:
                missing = expected_columns - actual_columns
                unexpected = actual_columns - expected_columns
                raise DataLoadError(
                    f"'{filename}' has incorrect columns. "
                    f"Missing: {missing or 'none'}. Unexpected: {unexpected or 'none'}."
                )

            for row_number, row in enumerate(budget_reader, start=2):
                try:
                    budget_amount = float(row["Budget Amount"])
                    if budget_amount < 0:
                        raise ValueError("Budget Amount cannot be negative")

                    loaded_budgets.append({
                        "Account ID": row["Account ID"],
                        "Category": row["Category"],
                        "Budget Amount": budget_amount
                    })
                except ValueError as e:
                    raise DataLoadError(
                        f"'{filename}', row {row_number}: invalid data ({e}). "
                        f"Row contents: {row}"
                    )

    except FileNotFoundError:
        raise DataLoadError(f"Could not find file '{filename}'. Check the file path and try again.")

    return loaded_budgets


#  Command-line entry point (only runs when this file is executed directly
def main():
    accounts_list, budgets_list, transactions_list = load_all_data(
        "accounts.csv", "budgets.csv", "transactions.csv"
    )

if __name__ == "__main__":
    main()