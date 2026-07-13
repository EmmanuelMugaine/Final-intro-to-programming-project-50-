# Final-intro-to-programming-project

## Project Description ##
A personal finance tracking and budgeting application. The user maintains multiple accounts (e.g. checking, savings, credit) and records transactions against them, each tagged with a category and optional notes. Transactions can be entered manually through the interface or imported in bulk from a CSV file. The program sorts and searches transaction records using a custom-built sorting algorithm and binary search, allowing the user to quickly view spending within a given date range or filter by category. Budgets can be set per category, and the application uses a simple rule-based method to forecast whether the user is on track to stay within budget based on their recent spending pattern. The application includes a graphical interface with a dashboard of data visualisations, such as spending by category and spending trends over time, and all account, transaction, and budget data is saved to and loaded from CSV files so a user's data persists between sessions.

## Introduction
I intend to create a Personal Finance Manager programme using python. The programme will read data from a CSV file and place the values into different categories such as income and expenses. From this, various charts and graphs will be displayed showing the trend of expendature of the user along wth predicting whether the user will be above or below their allocated budget category

I am making the assumption that the programm is being used by an admin and as such they have access to all the user details and can view individual user accounts

## Features to be implemented

### Data Visualisation
Using matplotlib in tkinter to visualise spending over time (line graph), Spending per category (pie/bar charts) and budget vs actual amount (pie chart)

### GUI
Using tkinter to create a login page, dashboard and tabs to cycle through

### File I/O
Importing user transaction files as a CSV file

### Searching and Sorting
Implementing a searching and sorting algorithm to sort the user transactions read from the CSV in terms of date/name/balance
I will also implement a way for the user to choose which field to sort by

### Error Handling
I will include data verification and input sanitation to prevent erroneous user input values
FileNotFound errors will be addressed
CSV parsing errors will be addressed
