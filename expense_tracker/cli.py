"""CLI interface for expense_tracker project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
import argparse
from .base import ExpenseTracker    

def main():
    # Create the main parser
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add Expense Command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("-d", "--date", required=True, help="Date of the expense (YYYY-MM-DD)")
    add_parser.add_argument("-desc", "--description", required=True, help="Description of the expense")
    add_parser.add_argument("-a", "--amount", type=float, required=True, help="Amount of the expense")

    # List Expenses Command
    list_parser = subparsers.add_parser("list", help="List all expenses")

    # Delete Expense Command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("-id", "--id", required=True, help="ID of the expense to delete")

    # Delete Expense Command
    summary_parser = subparsers.add_parser("summary", help="Sum of all expenses recorded")

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the ExpenseTracker
    tracker = ExpenseTracker(filepath="expenses.json")

    # Handle commands
    if args.command == "add":
        try:
            tracker.add_expense(args.date, args.description, args.amount)
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
    elif args.command == "list":
        tracker.list_expenses()
    elif args.command == "delete":
        tracker.delete_expense(args.id)
    elif args.command == "summary":
        tracker.expenses_summary()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
