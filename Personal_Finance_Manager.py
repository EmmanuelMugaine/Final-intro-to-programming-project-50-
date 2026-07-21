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
#Currently only displays one transaction per day if searched
def binary_search(sorted_data, target, key):
    #Searches a list that has ALREADY been sorted by 'key' for an
    #item whose key value equals the 'target'.
    
    #Returns the matching item, or None if not found.
    low = 0
    high = len(sorted_data) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_value = key(sorted_data[mid])

        if mid_value == target:
            return sorted_data[mid]  # Found it
        elif mid_value < target:
            low = mid + 1  # Target is in the right half
        else:
            high = mid - 1  # Target is in the left half

    return None  # Not found