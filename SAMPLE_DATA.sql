-- Sample Data for Smart Expense Tracking System
-- ============================================
-- This SQL file contains sample expense data for testing and demonstration purposes.
-- To use this data, execute these INSERT statements in your SQLite database.

-- Note: Amounts are stored in paise (100 paise = ₹1)
-- So ₹500.50 = 50050 paise

-- Sample Expenses Data
-- ====================

-- Week 1 Expenses
INSERT INTO expenses (title, amount, category, date) VALUES
('Grocery Shopping', 250000, 'Food', '2025-01-01'),      -- ₹2,500.00
('Bus Fare', 4000, 'Travel', '2025-01-01'),              -- ₹40.00
('Lunch at Restaurant', 15000, 'Food', '2025-01-02'),   -- ₹150.00
('Mobile Recharge', 30000, 'Bills', '2025-01-03'),       -- ₹300.00
('Petrol Filling', 200000, 'Travel', '2025-01-04'),      -- ₹2,000.00

-- Week 2 Expenses
INSERT INTO expenses (title, amount, category, date) VALUES
('Dinner with Friends', 22000, 'Food', '2025-01-08'),    -- ₹220.00
('Grocery Items', 180000, 'Food', '2025-01-09'),         -- ₹1,800.00
('Metro Card Recharge', 50000, 'Travel', '2025-01-10'),  -- ₹500.00
('Electricity Bill', 120000, 'Bills', '2025-01-11'),     -- ₹1,200.00
('Online Shopping', 350000, 'Shopping', '2025-01-12'),   -- ₹3,500.00

-- Week 3 Expenses
INSERT INTO expenses (title, amount, category, date) VALUES
('Breakfast', 8000, 'Food', '2025-01-15'),               -- ₹80.00
('Cab Ride', 25000, 'Travel', '2025-01-15'),             -- ₹250.00
('Grocery Store', 120000, 'Food', '2025-01-16'),         -- ₹1,200.00
('Water Bill', 80000, 'Bills', '2025-01-17'),            -- ₹800.00
('Clothes Purchase', 250000, 'Shopping', '2025-01-18'),  -- ₹2,500.00

-- Week 4 Expenses
INSERT INTO expenses (title, amount, category, date) VALUES
('Lunch Box', 6000, 'Food', '2025-01-22'),               -- ₹60.00
('Train Ticket', 15000, 'Travel', '2025-01-23'),         -- ₹150.00
('Fruits and Vegetables', 90000, 'Food', '2025-01-24'),  -- ₹900.00
('Internet Bill', 60000, 'Bills', '2025-01-25'),         -- ₹600.00
('Book Purchase', 75000, 'Shopping', '2025-01-26'),       -- ₹750.00

-- Additional Expenses for December 2024
INSERT INTO expenses (title, amount, category, date) VALUES
('Monthly Groceries', 300000, 'Food', '2024-12-01'),     -- ₹3,000.00
('Weekend Trip', 500000, 'Travel', '2024-12-05'),        -- ₹5,000.00
('Dinner Date', 25000, 'Food', '2024-12-06'),            -- ₹250.00
('Gas Bill', 150000, 'Bills', '2024-12-10'),             -- ₹1,500.00
('Electronics Accessories', 800000, 'Shopping', '2024-12-15'), -- ₹8,000.00
('Coffee with Colleagues', 3000, 'Food', '2024-12-20'),  -- ₹30.00
('Auto Rickshaw', 1500, 'Travel', '2024-12-22'),         -- ₹15.00
('Medicine Purchase', 120000, 'Other', '2024-12-25'),    -- ₹1,200.00
('New Year Party', 80000, 'Food', '2024-12-31'),         -- ₹800.00

-- Additional Expenses for February 2025
INSERT INTO expenses (title, amount, category, date) VALUES
('Weekly Groceries', 220000, 'Food', '2025-02-05'),      -- ₹2,200.00
('Bus Pass', 100000, 'Travel', '2025-02-06'),            -- ₹1,000.00
('Mobile Bill', 40000, 'Bills', '2025-02-07'),           -- ₹400.00
('Stationery Items', 35000, 'Shopping', '2025-02-08'),   -- ₹350.00
('Snacks', 2000, 'Food', '2025-02-09'),                  -- ₹20.00

-- Display All Expenses (Optional Query)
-- SELECT * FROM expenses ORDER BY date DESC, id DESC;

-- Display Monthly Summary (Optional Query)
-- SELECT SUBSTR(date, 1, 7) as month, category, SUM(amount)/100 as total_amount
-- FROM expenses
-- GROUP BY SUBSTR(date, 1, 7), category
-- ORDER BY month DESC, total_amount DESC;

-- Display Total Spending (Optional Query)
-- SELECT SUM(amount)/100 as total_spent, AVG(amount)/100 as average_spent
-- FROM expenses;

-- Instructions for Manual Data Entry:
-- ================================
-- If you prefer to manually add these expenses through the web interface:
--
-- January 2025 Expenses:
-- 1. Grocery Shopping - ₹2500.00 - Food - 2025-01-01
-- 2. Bus Fare - ₹40.00 - Travel - 2025-01-01
-- 3. Lunch at Restaurant - ₹150.00 - Food - 2025-01-02
-- 4. Mobile Recharge - ₹300.00 - Bills - 2025-01-03
-- 5. Petrol Filling - ₹2000.00 - Travel - 2025-01-04
-- 6. Dinner with Friends - ₹220.00 - Food - 2025-01-08
-- 7. Grocery Items - ₹1800.00 - Food - 2025-01-09
-- 8. Metro Card Recharge - ₹500.00 - Travel - 2025-01-10
-- 9. Electricity Bill - ₹1200.00 - Bills - 2025-01-11
-- 10. Online Shopping - ₹3500.00 - Shopping - 2025-01-12
-- 11. Breakfast - ₹80.00 - Food - 2025-01-15
-- 12. Cab Ride - ₹250.00 - Travel - 2025-01-15
-- 13. Grocery Store - ₹1200.00 - Food - 2025-01-16
-- 14. Water Bill - ₹800.00 - Bills - 2025-01-17
-- 15. Clothes Purchase - ₹2500.00 - Shopping - 2025-01-18
-- 16. Lunch Box - ₹60.00 - Food - 2025-01-22
-- 17. Train Ticket - ₹150.00 - Travel - 2025-01-23
-- 18. Fruits and Vegetables - ₹900.00 - Food - 2025-01-24
-- 19. Internet Bill - ₹600.00 - Bills - 2025-01-25
-- 20. Book Purchase - ₹750.00 - Shopping - 2025-01-26
--
-- December 2024 Expenses:
-- 21. Monthly Groceries - ₹3000.00 - Food - 2024-12-01
-- 22. Weekend Trip - ₹5000.00 - Travel - 2024-12-05
-- 23. Dinner Date - ₹250.00 - Food - 2024-12-06
-- 24. Gas Bill - ₹1500.00 - Bills - 2024-12-10
-- 25. Electronics Accessories - ₹8000.00 - Shopping - 2024-12-15
-- 26. Coffee with Colleagues - ₹30.00 - Food - 2024-12-20
-- 27. Auto Rickshaw - ₹15.00 - Travel - 2024-12-22
-- 28. Medicine Purchase - ₹1200.00 - Other - 2024-12-25
-- 29. New Year Party - ₹800.00 - Food - 2024-12-31
--
-- February 2025 Expenses:
-- 30. Weekly Groceries - ₹2200.00 - Food - 2025-02-05
-- 31. Bus Pass - ₹1000.00 - Travel - 2025-02-06
-- 32. Mobile Bill - ₹400.00 - Bills - 2025-02-07
-- 33. Stationery Items - ₹350.00 - Shopping - 2025-02-08
-- 34. Snacks - ₹20.00 - Food - 2025-02-09

-- Total Sample Expenses: 34
-- Total Amount Spent: ₹42,520.00
--
-- Monthly Breakdown:
-- December 2024: ₹18,430.00
-- January 2025: ₹23,160.00
-- February 2025: ₹930.00 (partial month)
--
-- Category Breakdown:
-- Food: ₹9,840.00
-- Travel: ₹9,165.00
-- Bills: ₹4,400.00
-- Shopping: ₹13,100.00
-- Other: ₹1,200.00

-- Note: These sample expenses provide a good variety for testing the dashboard,
-- monthly summaries, charts, and expense categorization features of the application.