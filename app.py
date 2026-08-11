"""
Smart Expense Tracking System - Flask Application
==============================================

This is the main Flask application for the Smart Expense Tracking System.
It provides a web interface for managing personal expenses with features like
adding expenses, viewing expense history, and generating monthly summaries.

Features:
- Add new expenses with title, amount, category, and date
- View all expenses in a paginated table
- Generate monthly spending summaries
- Bar chart visualization of monthly spending
- Clean, responsive web interface

Author: AI Assistant
Date: 2025
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import database
import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO
from datetime import datetime

# Use non-interactive backend for matplotlib to avoid GUI issues
matplotlib.use('Agg')

# Create Flask application instance
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Ensure database tables are created
database.create_table()

# Available expense categories
CATEGORIES = ['Food', 'Travel', 'Bills', 'Shopping', 'Other']


@app.route('/')
def index():
    """
    Home dashboard route.

    Displays:
    - Total amount spent
    - Recent expenses (last 5)
    - Quick statistics

    Returns:
        Rendered template with dashboard data
    """
    # Get all expenses and calculate totals
    expenses = database.fetch_all_expenses()
    total_spent = database.get_total_spent()

    # Get basic statistics
    stats = database.get_expense_statistics()

    # Get recent expenses (last 5)
    recent_expenses = expenses[:5]

    return render_template('index.html',
                         total_spent=total_spent,
                         recent_expenses=recent_expenses,
                         stats=stats,
                         categories=CATEGORIES)


@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    """
    Add expense route.

    GET: Display the add expense form
    POST: Process the form submission and add expense to database

    Returns:
        Redirect to home page on success, or form template on error
    """
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        amount = request.form.get('amount', '').strip()
        category = request.form.get('category')
        date = request.form.get('date')

        # Validate form data
        if not title:
            flash('Please enter expense title', 'error')
            return render_template('add_expense.html', categories=CATEGORIES)

        if not amount:
            flash('Please enter expense amount', 'error')
            return render_template('add_expense.html', categories=CATEGORIES)

        try:
            amount = float(amount)
            if amount <= 0:
                flash('Amount must be greater than zero', 'error')
                return render_template('add_expense.html', categories=CATEGORIES)
        except ValueError:
            flash('Please enter a valid amount', 'error')
            return render_template('add_expense.html', categories=CATEGORIES)

        if not category:
            flash('Please select a category', 'error')
            return render_template('add_expense.html', categories=CATEGORIES)

        if not date:
            flash('Please select a date', 'error')
            return render_template('add_expense.html', categories=CATEGORIES)

        # Add expense to database
        if database.add_expense(title, amount, category, date):
            flash('Expense added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error adding expense. Please try again.', 'error')

    return render_template('add_expense.html', categories=CATEGORIES)


@app.route('/expenses')
def view_expenses():
    """
    View all expenses route.

    Displays all expenses in a paginated table format.

    Query Parameters:
        page: Page number for pagination (default: 1)

    Returns:
        Rendered template with expenses data
    """
    # Get all expenses
    expenses = database.fetch_all_expenses()

    # Simple pagination (10 items per page)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = len(expenses)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_expenses = expenses[start:end]

    # Calculate pagination
    total_pages = (total + per_page - 1) // per_page  # Ceiling division

    return render_template('view_expenses.html',
                         expenses=paginated_expenses,
                         page=page,
                         total_pages=total_pages,
                         total=total)


@app.route('/summary')
def monthly_summary():
    """
    Monthly summary route.

    Displays:
    - Monthly spending breakdown by category
    - Bar chart of monthly totals
    - Downloadable chart image

    Returns:
        Rendered template with summary data and chart
    """
    # Get monthly summary data
    monthly_data = database.fetch_monthly_summary()
    monthly_totals = database.fetch_monthly_totals()

    # Prepare data for chart
    months = list(monthly_totals.keys())
    amounts = list(monthly_totals.values())

    # Create bar chart (smaller, fixed size so it renders at a sane size in the browser)
    plt.figure(figsize=(7, 4))
    plt.bar(months, amounts, color='#4CAF50', alpha=0.8)
    plt.title('Monthly Spending Summary', fontsize=14, fontweight='bold', pad=16)
    plt.xlabel('Month', fontsize=10)
    plt.ylabel('Amount (₹)', fontsize=10)
    plt.xticks(rotation=45, fontsize=9)
    plt.yticks(fontsize=9)
    plt.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, (month, amount) in enumerate(zip(months, amounts)):
        plt.text(i, amount + max(amounts) * 0.02, f'₹{amount:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=8)

    plt.tight_layout()

    # Convert plot to base64 string
    img = BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()

    return render_template('summary.html',
                         monthly_data=monthly_data,
                         monthly_totals=monthly_totals,
                         chart_url=chart_url)


@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    """
    Delete expense route.

    Args:
        expense_id (int): ID of the expense to delete

    Returns:
        Redirect to previous page
    """
    # Get referrer URL for redirect
    referrer = request.referrer or url_for('view_expenses')

    # Delete expense
    if database.delete_expense(expense_id):
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Error deleting expense.', 'error')

    return redirect(referrer)


@app.template_filter('currency')
def currency_format(value):
    """
    Jinja2 template filter to format currency.

    Args:
        value (float): Amount in rupees

    Returns:
        str: Formatted currency string with ₹ symbol
    """
    try:
        return f'₹{float(value):,.2f}'
    except (ValueError, TypeError):
        return f'₹{value}'


@app.template_filter('date_format')
def date_format_filter(date_str):
    """
    Jinja2 template filter to format date.

    Args:
        date_str (str): Date string in YYYY-MM-DD format

    Returns:
        str: Formatted date string in DD-MM-YYYY format
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d-%m-%Y')
    except (ValueError, TypeError):
        return date_str


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500


if __name__ == '__main__':
    """
    Run the Flask application.

    Debug mode is enabled for development.
    """
    print("Starting Smart Expense Tracking System...")
    print("Visit http://localhost:5000 to access the application")
    app.run(debug=True, host='0.0.0.0', port=5000)