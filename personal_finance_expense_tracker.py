import json
import os
import datetime
import urllib.request

# FILE PATHS

CATEGORY_FILE = "data/categories.txt"
TRANSACTION_FILE = "data/transactions.json"
REPORT_FILE = "data/monthly_report.txt"

# SETUP FILES

def setup_files():

    if not os.path.exists("data"):
        os.mkdir("data")

    # Category File
    if not os.path.exists(CATEGORY_FILE):

        file = open(CATEGORY_FILE, "w")
        file.write("Food\n")
        file.write("Transport\n")
        file.write("Shopping\n")
        file.write("Rent\n")
        file.write("Salary\n")
        file.write("Utilities\n")
        file.write("Education\n")
        file.write("Entertainment\n")
        file.write("Others\n")
        file.close()

    # Transaction File
    if not os.path.exists(TRANSACTION_FILE):

        file = open(TRANSACTION_FILE, "w")
        json.dump([], file, indent=4)
        file.close()

# DISPLAY MENU

def display_menu():

    print("\n" + "="*55)
    print("      PERSONAL FINANCE MANAGER")
    print("="*55)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. Search Transaction")
    print("5. Update Transaction")
    print("6. Delete Transaction")
    print("7. Financial Summary")
    print("8. Category-wise Analysis")
    print("9. Monthly Report")
    print("10. Currency Converter")
    print("11. Exit")

# LOAD CATEGORIES

def load_categories():

    categories = []
    file = open(CATEGORY_FILE, "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        categories.append(line.strip())
    return categories

# LOAD TRANSACTIONS

def load_transactions():

    try:
        file = open(TRANSACTION_FILE, "r")
        transactions = json.load(file)
        file.close()
        return transactions
    except:
        return []

# SAVE TRANSACTIONS

def save_transactions(transactions):

    file = open(TRANSACTION_FILE, "w")
    json.dump(transactions, file, indent=4)
    file.close()

# AUTO TRANSACTION ID

def generate_transaction_id():

    transactions = load_transactions()

    if len(transactions) == 0:
        return 1001

    last_id = transactions[-1]["ID"]
    return last_id + 1

# VALID DATE

def get_valid_date():

    while True:
        date = input("Enter Date (YYYY-MM-DD) or press Enter for today: ")
        if date == "":
            return datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            valid = datetime.datetime.strptime(date,"%Y-%m-%d")
            return valid.strftime("%Y-%m-%d")
        except:
            print("Invalid Date!")

# VALID CATEGORY

def get_valid_category():

    categories = load_categories()
    print("\nAvailable Categories\n")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    while True:

        try:
            choice = int(input("\nChoose Category: "))
            if 1 <= choice <= len(categories):
                return categories[choice-1]
            else:
                print("Invalid Choice")
        except:
            print("Enter Number Only")

# VALID AMOUNT

def get_valid_amount():

    while True:

        try:
            amount = float(input("Enter Amount: "))
            if amount > 0:
                return amount
            else:
                print("Amount must be positive.")
        except:
            print("Invalid Number!")

# VALID DESCRIPTION

def get_description():

    description = input("Enter Description: ")
    return description

# ADD TRANSACTION

def add_transaction(transaction_type):

    transactions = load_transactions()
    transaction = {
        "ID": generate_transaction_id(),
        "Date": get_valid_date(),
        "Type": transaction_type,
        "Category": get_valid_category(),
        "Amount": get_valid_amount(),
        "Description": get_description()
    }
    transactions.append(transaction)
    save_transactions(transactions)
    print("\nTransaction Added Successfully!")

# VIEW ALL TRANSACTIONS

def view_transactions():

    transactions = load_transactions()
    if len(transactions) == 0:
        print("\nNo Transactions Found!")
        return
    
    print("\n" + "=" * 90)
    print(f"{'ID':<8}{'Date':<15}{'Type':<12}{'Category':<18}{'Amount':<12}Description")
    print("=" * 90)

    for transaction in transactions:

        print(f"{transaction['ID']:<8}"
              f"{transaction['Date']:<15}"
              f"{transaction['Type']:<12}"
              f"{transaction['Category']:<18}"
              f"{transaction['Amount']:<12.2f}"
              f"{transaction['Description']}")
    print("=" * 90)
    print(f"Total Transactions: {len(transactions)}")

# SEARCH TRANSACTION

def search_transaction():

    transactions = load_transactions()

    if len(transactions) == 0:
        print("\nNo Transactions Found!")
        return

    print("\nSearch By")
    print("1. Date")
    print("2. Category")
    print("3. Type")

    choice = input("Enter Choice: ")

    matches = []

    if choice == "1":
        keyword = input("Enter Date (YYYY-MM-DD): ").strip()
        for transaction in transactions:
            if transaction["Date"] == keyword:
                matches.append(transaction)
    elif choice == "2":
        keyword = input("Enter Category: ").strip().lower()
        for transaction in transactions:
            if transaction["Category"].lower() == keyword:
                matches.append(transaction)
    elif choice == "3":
        keyword = input("Enter Type (Income/Expense): ").strip().lower()
        for transaction in transactions:
            if transaction["Type"].lower() == keyword:
                matches.append(transaction)
    else:
        print("Invalid Choice!")
        return

    if len(matches) == 0:
        print("\nNo Matching Transactions Found!")
        return

    print("\nMatching Transactions\n")
    print("=" * 90)
    print(f"{'ID':<8}{'Date':<15}{'Type':<12}{'Category':<18}{'Amount':<12}Description")
    print("=" * 90)

    for transaction in matches:

        print(f"{transaction['ID']:<8}"
              f"{transaction['Date']:<15}"
              f"{transaction['Type']:<12}"
              f"{transaction['Category']:<18}"
              f"{transaction['Amount']:<12.2f}"
              f"{transaction['Description']}")
    print("=" * 90)
    print(f"Found {len(matches)} Record(s).")

# UPDATE TRANSACTION

def update_transaction():

    transactions = load_transactions()
    if len(transactions) == 0:
        print("\nNo Transactions Available.")
        return
    try:
        trans_id = int(input("Enter Transaction ID to Update: "))
    except:
        print("Invalid ID!")
        return
    
    found = False

    for transaction in transactions:
        if transaction["ID"] == trans_id:

            found = True
            print("\nCurrent Information")
            print("--------------------------")
            print("Category :", transaction["Category"])
            print("Amount   :", transaction["Amount"])
            print("Description :", transaction["Description"])
            print("\nLeave blank to keep old value.")

            new_category = input("New Category: ")

            if new_category != "":
                transaction["Category"] = new_category
            new_amount = input("New Amount: ")

            if new_amount != "":

                try:
                    amount = float(new_amount)
                    if amount > 0:
                        transaction["Amount"] = amount
                except:
                    print("Invalid Amount! Old value kept.")

            new_description = input("New Description: ")

            if new_description != "":
                transaction["Description"] = new_description
            break

    if found:
        save_transactions(transactions)
        print("\nTransaction Updated Successfully!")
    else:
        print("\nTransaction ID Not Found!")

# DELETE TRANSACTION

def delete_transaction():

    transactions = load_transactions()
    if len(transactions) == 0:
        print("\nNo Transactions Found!")
        return

    try:
        trans_id = int(input("Enter Transaction ID to Delete: "))
    except:
        print("Invalid ID!")
        return

    found = False
    for transaction in transactions:
        if transaction["ID"] == trans_id:
            transactions.remove(transaction)
            found = True
            break

    if found:
        save_transactions(transactions)
        print("\nTransaction Deleted Successfully!")
    else:
        print("\nTransaction ID Not Found!")

# FINANCIAL SUMMARY

def financial_summary():

    transactions = load_transactions()
    if len(transactions) == 0:
        print("\nNo Transactions Found!")
        return

    total_income = 0
    total_expense = 0

    for transaction in transactions:

        if transaction["Type"] == "Income":
            total_income += transaction["Amount"]
        elif transaction["Type"] == "Expense":
            total_expense += transaction["Amount"]

    balance = total_income - total_expense

    print("\n" + "=" * 45)
    print("        FINANCIAL SUMMARY")
    print("=" * 45)
    print(f"Total Income : {total_income:.2f} BDT")
    print(f"Total Expense: {total_expense:.2f} BDT")
    print("-" * 45)
    print(f"Current Balance: {balance:.2f} BDT")
    print("=" * 45)

    if balance > 0:
        print("✔ Great! You are saving money.")
    elif balance < 0:
        print("⚠ You are spending more than your income.")
    else:
        print("Income and Expense are equal.")

# CATEGORY-WISE ANALYSIS
# (Dictionary + Set)

def category_analysis():

    transactions = load_transactions()
    if len(transactions) == 0:
        print("\nNo Transactions Found!")
        return

    category_totals = {}      # Dictionary
    unique_categories = set() # Set

    for transaction in transactions:

        if transaction["Type"] == "Expense":
            category = transaction["Category"]
            unique_categories.add(category)
            if category in category_totals:
                category_totals[category] += transaction["Amount"]
            else:
                category_totals[category] = transaction["Amount"]

    print("\n" + "=" * 45)
    print("      CATEGORY-WISE EXPENSE")
    print("=" * 45)

    total = 0

    for category in sorted(unique_categories):
        amount = category_totals.get(category, 0)
        print(f"{category:<20} {amount:.2f} BDT")
        total += amount
    print("-" * 45)
    print(f"Total Expense : {total:.2f} BDT")

# MONTHLY REPORT
# (Tuple Used)

def generate_monthly_report():

    transactions = load_transactions()
    if len(transactions) == 0:
        print("\nNo Transactions Found!")
        return

    month = input("Enter Month (YYYY-MM): ")

    monthly_transactions = []

    monthly_income = 0
    monthly_expense = 0

    for transaction in transactions:

        if transaction["Date"].startswith(month):
            monthly_transactions.append(transaction)
            if transaction["Type"] == "Income":
                monthly_income += transaction["Amount"]
            elif transaction["Type"] == "Expense":
                monthly_expense += transaction["Amount"]
    savings = monthly_income - monthly_expense

    # Tuple (required by project)
    report_values = (
        month,
        monthly_income,
        monthly_expense,
        savings
    )

    try:

        file = open(REPORT_FILE, "w")

        file.write("=" * 55 + "\n")
        file.write("        MONTHLY FINANCIAL REPORT\n")
        file.write("=" * 55 + "\n\n")
        file.write(f"Month           : {report_values[0]}\n")
        file.write(f"Total Income    : {report_values[1]:.2f} BDT\n")
        file.write(f"Total Expense   : {report_values[2]:.2f} BDT\n")
        file.write(f"Current Savings : {report_values[3]:.2f} BDT\n")
        file.write("\n")
        file.write("-" * 55 + "\n")
        file.write("TRANSACTIONS\n")
        file.write("-" * 55 + "\n\n")

        if len(monthly_transactions) == 0:
            file.write("No Transactions Found.\n")
        else:
            for transaction in monthly_transactions:
                file.write(f"ID          : {transaction['ID']}\n")
                file.write(f"Date        : {transaction['Date']}\n")
                file.write(f"Type        : {transaction['Type']}\n")
                file.write(f"Category    : {transaction['Category']}\n")
                file.write(f"Amount      : {transaction['Amount']:.2f} BDT\n")
                file.write(f"Description : {transaction['Description']}\n")
                file.write("-" * 55 + "\n")
        file.close()

        print("\nMonthly Report Generated Successfully!")
        print(f"Saved as: {REPORT_FILE}")
    except:
        print("Error Creating Report!")

# CURRENCY CONVERTER (API)

def currency_converter():

    transactions = load_transactions()
    if len(transactions) == 0:
        print("\nNo Transactions Found!")
        return
    
    # Calculate Current Balance
    total_income = 0
    total_expense = 0

    for transaction in transactions:

        if transaction["Type"] == "Income":
            total_income += transaction["Amount"]
        elif transaction["Type"] == "Expense":
            total_expense += transaction["Amount"]

    balance = total_income - total_expense

    print("\nCurrent Balance: {:.2f} BDT".format(balance))

    print("\nFetching Latest Exchange Rates...")

    try:
        url = "https://open.er-api.com/v6/latest/BDT"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

        if data["result"] != "success":
            print("Unable to fetch exchange rates.")
            return

        rates = data["rates"]

        usd = balance * rates["USD"]
        eur = balance * rates["EUR"]
        gbp = balance * rates["GBP"]

        print("\n" + "=" * 45)
        print("     BALANCE IN OTHER CURRENCIES")
        print("=" * 45)

        print(f"BDT : {balance:.2f}")
        print(f"USD : {usd:.2f}")
        print(f"EUR : {eur:.2f}")
        print(f"GBP : {gbp:.2f}")

        print("=" * 45)

    except Exception as error:

        print("\nInternet Connection Error!")
        print(error)

# MAIN FUNCTION

def main():

    setup_files()
    print("=" * 55)
    print("     WELCOME TO PERSONAL FINANCE MANAGER")
    print("=" * 55)

    while True:
        display_menu()

        choice = input("\nEnter Your Choice (1-11): ")

        if choice == "1":
            print("\nADD INCOME")
            add_transaction("Income")

        elif choice == "2":
            print("\nADD EXPENSE")
            add_transaction("Expense")

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            search_transaction()

        elif choice == "5":
            update_transaction()

        elif choice == "6":
            delete_transaction()

        elif choice == "7":
            financial_summary()

        elif choice == "8":
            category_analysis()

        elif choice == "9":
            generate_monthly_report()

        elif choice == "10":
            currency_converter()

        elif choice == "11":
            print("\nThank you for using Personal Finance Manager!")
            print("Good Bye!")
            break
        else:
            print("\nInvalid Choice!")
            print("Please Enter a Number Between 1 and 11.")

main()