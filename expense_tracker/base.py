"""
expense_tracker base module.

This is the principal module of the expense_tracker project.
here you put your main classes and objects.
"""

import datetime
import json
import os
import uuid
DEFAULT_JSON_INDENT = 4 

class Expense:
    def __init__(self, expense_id, date, description, amount):
        """
        Initialize an Expense object.

        :param expense_id: A unique identifier for the expense (e.g., integer or string)
        :param date: The date of the expense (e.g., 'YYYY-MM-DD' as string or a datetime object)
        :param description: A brief description of the expense (e.g., 'Office supplies')
        :param amount: The monetary amount of the expense (e.g., a float or decimal)
        """
        # Validate expense_id
        if not isinstance(expense_id, str):
            raise TypeError("Expense ID must be a string.")
        try:
            uuid.UUID(expense_id)  # Validate that expense_id is a valid UUID
        except ValueError:
            raise ValueError("Expense ID must be a valid UUID.")
        self.id = expense_id

        # Validate date
        if isinstance(date, str):
            try:
                self.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Date must be in 'YYYY-MM-DD' format. Provided value: {date}")
        elif isinstance(date, datetime):
            self.date = date.date()
        else:
            raise TypeError(f"Date must be a string in 'YYYY-MM-DD' format or a datetime object. Provided type: {type(date)}")

        # Validate description
        if not isinstance(description, str):
            raise TypeError(f"Description must be a string. Provided type: {type(description)}")
        self.description = description

        # Validate amount
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Amount must be a number. Provided type: {type(amount)}")
        if amount < 0:
            raise ValueError(f"Amount must be positive. Provided value: {amount}")
        self.amount = float(amount)

    def __str__(self):
        """
        Return a string representation of the expense.
        """
        return f"Expense(ID={self.id}, Date={self.date}, Description={self.description}, Amount={self.amount})"

    def __repr__(self):
        """
        Return a technical string representation of the expense.
        """
        return f"Expense({self.id}, {self.date}, {self.description}, {self.amount})"
    
    def to_dict(self):
        return{
            "id":self.id,
            "date":self.date.isoformat(),
            "description":self.description,
            "amount":self.amount,
        }

class ExpenseTracker:

    def __init__(self, filepath="expenses.json"):
        self.filepath = filepath
        self.expenses = self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as file:
                return json.load(file)
        else:
            #create an empty JSON file if it doesn't exist
            with open(self.filepath, "w") as file:
                json.dump([], file, indent=DEFAULT_JSON_INDENT)
            return []
        
    def save_expenses(self):
        with open(self.filepath, "w") as file:
            json.dump(self.expenses,file,indent=DEFAULT_JSON_INDENT)

    def add_expense(self, date, description, amount):
        expense_id = str(uuid.uuid4()) #generate a new UUID
        expense = Expense(expense_id, date, description, amount)
        self.expenses.append(expense.to_dict())
        self.save_expenses()
        print(f"Expense added successfully (ID: {expense.id})")


    def list_expenses(self):
        if not self.expenses:
            print("No expenses recorded")
        else : 
            # Define header and row format
            header = f"{'ID':<36} | {'Date':<12} | {'Description':<20} | {'Amount':>10}"
            print(header)
            print("-" * len(header))
            # Go through the expenses list and print each one
            for expense in self.expenses:
                print(f"{expense['id']:<36} | {expense['date']:<12} | {expense['description']:<20} | {expense['amount']:>10}")

    def expenses_summary(self):
        total_expenses = 0
        if self.expenses:
           # Go through the expenses list and add to total
           for expense in self.expenses:
               total_expenses += expense['amount']
        print(f"Total Expenses: {total_expenses}")
                
    def delete_expense(self, expense_id) :
        # Go through the expenses list and print each one
        for expense in self.expenses:
            if expense['id'] == expense_id:
                self.expenses.remove(expense)
                self.save_expenses()
                print(f"Expense with ID {expense_id} successfully deleted")
                return
        print("ID Not Found")
                
        