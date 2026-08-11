"""
Smart Expense Tracking System - Database Module
==============================================

This module handles all database operations for the Smart Expense Tracking System.
It uses SQLite3 for data storage and provides functions for creating tables,
adding expenses, fetching data, and generating monthly summaries.

Author: AI Assistant
Date: 2025
"""

import sqlite3
import os
from datetime import datetime


def get_db_connection():
    """
    Create and return a database connection.

    Returns:
        sqlite3.Connection: Database connection object
    """
    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, 'expenses.db')

    # Connect to SQLite database (creates file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def create_table():
    """
    Create the expenses table if it doesn't already exist.

    The table structure includes:
    - id: Primary key (auto-incrementing)
    - title: Expense description
    - amount: Expense amount (integer in paise for precision)
    - category: Expense category
    - date: Expense date (YYYY-MM-DD format)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount INTEGER NOT NULL,  -- Stored in paise (100 paise = INR 1)
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def add_expense(title, amount, category, date):
    """
    Add a new expense to the database.

    Args:
        title (str): Description of the expense
        amount (int/float): Amount in rupees
        category (str): Category of the expense
        date (str): Date in YYYY-MM-DD format

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Convert amount to integer paise for storage
        # This prevents floating point precision issues
        amount_in_paise = int(float(amount) * 100)

        # Insert the expense record
        cursor.execute('''
            INSERT INTO expenses (title, amount, category, date)
            VALUES (?, ?, ?, ?)
        ''', (title, amount_in_paise, category, date))

        # Commit changes
        conn.commit()
        conn.close()

        return True
    except Exception as e:
        print(f"Error adding expense: {e}")
        return False


def fetch_all_expenses():
    """
    Fetch all expenses from the database, ordered by date (newest first).

    Returns:
        list: List of dictionaries containing expense data
              Each dict has: id, title, amount, category, date
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all expenses ordered by date (newest first)
    cursor.execute('''
        SELECT id, title, amount, category, date
        FROM expenses
        ORDER BY date DESC, id DESC
    ''')

    rows = cursor.fetchall()
    conn.close()

    # Convert rows to list of dictionaries
    expenses = []
    for row in rows:
        expense = {
            'id': row[0],
            'title': row[1],
            'amount': row[2] / 100,  # Convert back to rupees
            'category': row[3],
            'date': row[4]
        }
        expenses.append(expense)

    return expenses


def fetch_monthly_summary():
    """
    Fetch monthly spending summary grouped by category.

    Returns:
        list: List of dictionaries with month, category, and total amount
              Amounts are converted back to rupees from paise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Group expenses by year-month and category, sum amounts
    cursor.execute('''
        SELECT
            SUBSTR(date, 1, 7) as month,  -- YYYY-MM
            category,
            SUM(amount) as total_amount
        FROM expenses
        GROUP BY SUBSTR(date, 1, 7), category
        ORDER BY month DESC, total_amount DESC
    ''')

    rows = cursor.fetchall()
    conn.close()

    # Convert rows to list of dictionaries
    summary = []
    for row in rows:
        record = {
            'month': row[0],
            'category': row[1],
            'total_amount': row[2] / 100  # Convert back to rupees
        }
        summary.append(record)

    return summary


def fetch_monthly_totals():
    """
    Fetch total spending per month across all categories.

    Returns:
        dict: Dictionary with months as keys and total amounts as values
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get total spending per month
    cursor.execute('''
        SELECT
            SUBSTR(date, 1, 7) as month,
            SUM(amount) as total_amount
        FROM expenses
        GROUP BY SUBSTR(date, 1, 7)
        ORDER BY month DESC
    ''')

    rows = cursor.fetchall()
    conn.close()

    # Convert to dictionary
    monthly_totals = {}
    for row in rows:
        monthly_totals[row[0]] = row[1] / 100  # Convert to rupees

    return monthly_totals


def get_expense_by_id(expense_id):
    """
    Get a specific expense by its ID.

    Args:
        expense_id (int): The ID of the expense

    Returns:
        dict or None: Expense data or None if not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, title, amount, category, date
        FROM expenses
        WHERE id = ?
    ''', (expense_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'id': row[0],
            'title': row[1],
            'amount': row[2] / 100,
            'category': row[3],
            'date': row[4]
        }

    return None


def delete_expense(expense_id):
    """
    Delete an expense by its ID.

    Args:
        expense_id (int): The ID of the expense to delete

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()

        return cursor.rowcount > 0  # True if at least one row was deleted
    except Exception as e:
        print(f"Error deleting expense: {e}")
        return False


def get_total_spent():
    """
    Get the total amount spent across all expenses.

    Returns:
        float: Total amount spent in rupees
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT SUM(amount) FROM expenses')
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return result[0] / 100  # Convert to rupees
    return 0.0


def get_expense_statistics():
    """
    Get basic statistics about expenses.

    Returns:
        dict: Statistics including total count, average amount, etc.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get count, sum, average, min, max
    cursor.execute('''
        SELECT
            COUNT(*) as count,
            SUM(amount) as total,
            AVG(amount) as average,
            MIN(amount) as min_amount,
            MAX(amount) as max_amount
        FROM expenses
    ''')

    row = cursor.fetchone()
    conn.close()

    if row and row[0] > 0:  # If there are expenses
        return {
            'count': row[0],
            'total': row[1] / 100 if row[1] else 0,
            'average': row[2] / 100 if row[2] else 0,
            'min': row[3] / 100 if row[3] else 0,
            'max': row[4] / 100 if row[4] else 0
        }

    return {
        'count': 0,
        'total': 0.0,
        'average': 0.0,
        'min': 0.0,
        'max': 0.0
    }


# Initialize the database when this module is imported
if __name__ == "__main__":
    print("Initializing database...")
    create_table()
    print("Database initialized successfully!")