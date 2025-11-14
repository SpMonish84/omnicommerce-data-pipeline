-- Monthly Revenue Report
-- Joins: customers + orders + payments
-- Shows revenue by month with customer and order details

SELECT 
    strftime('%Y-%m', o.order_date) AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    SUM(p.amount) AS total_revenue,
    AVG(p.amount) AS avg_order_value,
    COUNT(CASE WHEN p.payment_status = 'Completed' THEN 1 END) AS completed_payments,
    SUM(CASE WHEN p.payment_status = 'Completed' THEN p.amount ELSE 0 END) AS completed_revenue
FROM 
    orders o
INNER JOIN 
    payments p ON o.order_id = p.order_id
INNER JOIN 
    customers c ON o.customer_id = c.customer_id
GROUP BY 
    strftime('%Y-%m', o.order_date)
ORDER BY 
    month DESC;

