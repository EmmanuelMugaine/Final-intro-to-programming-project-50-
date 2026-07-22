import csv  #For dictreader and dictwriter
from datetime import date, datetime #Converting string date values into actual dates

#--------- Opening and storing the Accounts csv file ------------
accounts_list = []
def load_accounts(filename):    #Reusable function to open any account file
    with open(filename , "r", newline= "") as accounts:
        account_reader = csv.DictReader(accounts)   #Storing file values as dictionaries
        for row in account_reader:
            accounts_list.append({
                "Account ID" : row["Account ID"],
                "Account Name" : row["Account Name"]
            })

load_accounts("accounts.csv")

budgets_list = []
#--------- Opening and storing the Budget csv file -------------
def load_budget(filename):
    with open(filename , "r", newline= "") as budget:
        budget_reader = csv.DictReader(budget)
    #Storing and Editing values to their appropriate data types
        for row in budget_reader:
            budgets_list.append({
                "Account ID" : row["Account ID"],
                "Category" : row["Category"],
                "Budget Amount" : float(row["Budget Amount"])
            })
#Loading the budgets.csv file
load_budget("budgets.csv")

transactions_list = []
#--------- Opening and storing the transactions csv file --------------
def load_transactions(filename):
    #Opening
    with open(filename , "r", newline= "") as transactions:
        transaction_reader = csv.DictReader(transactions)
    #Storing and Editing values to their appropriate data types
        for row in transaction_reader:  #Iterating the values in the reader
            transactions_list.append({ #Storing the values into the empty list created outside
                "Account ID" : row["Account ID"],
                "Date" : datetime.strptime( #Formatting date into YYYY-MM-DD
                row["Date"],
                "%Y-%m-%d"
                ).date(),
                "Company Name" : row["Company Name"],
                "Amount" : float(row["Amount"]),    #Formatting date into floats
                "Category" : row["Category"],
                "Description" : row["Description"]
            })
load_transactions("transactions.csv")

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

# Sort transactions by Date
transactions_by_date = merge_sort(transactions_list, key=lambda t: t["Date"])

# Sort transactions by Amount
transactions_by_amount = merge_sort(transactions_list, key=lambda t: t["Amount"])

# Sort budgets by Category
budgets_by_category = merge_sort(budgets_list, key=lambda b: b["Category"])

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

#Because the transaction by date is sorted earlier it is safe to search now
#Target date to find in the data set
target_date = datetime.strptime("2026-06-15", "%Y-%m-%d").date()
#Inputting target date into function
same_day_transactions = binary_search(transactions_by_date, target_date, key=lambda t: t["Date"])

if same_day_transactions:
    print(f"Found {len(same_day_transactions)} transaction(s) on {target_date}:")
    for t in same_day_transactions:
        print(f"  {t['Company Name']} - £{t['Amount']} ({t['Category']})")
else:
    print("No transactions found on that date.")

#--------- Budget Tracking Logic -----------
    #Compares actual spending against budgeted amounts, grouped by
    #Account ID, Category, and Month (YYYY-MM).
def track_budgets(transactions, budgets):    #Returns a list of dictionaries summarising each group.

    # Step 1: Group transaction totals by (Account ID, Category, Year-Month)
    spending = {}  # key: (account_id, category, "YYYY-MM") -> total spent

    for t in transactions:
        # Only track spending (negative amounts / expenses)
        # Adjust this check depending on how you store expenses vs income
        year_month = t["Date"].strftime("%Y-%m")
        group_key = (t["Account ID"], t["Category"], year_month)

        if group_key not in spending:
            spending[group_key] = 0.0
        spending[group_key] += t["Amount"]

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