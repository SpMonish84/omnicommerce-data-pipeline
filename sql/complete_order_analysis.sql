-- Complete Order Analysis Query
-- Joins all 5 tables: customers, orders, order_items, products, payments
-- Shows comprehensive order details with total order value

SELECT
    c.name AS customer_name,
    c.email AS customer_email,
    o.order_id,
    o.order_date,
    p.name AS product_name,
    p.category,
    oi.quantity,
    oi.subtotal,
    SUM(oi.subtotal) OVER (PARTITION BY o.order_id) AS total_order_value,
    pay.payment_method,
    pay.payment_status,
    o.status AS order_status
FROM 
    orders o
INNER JOIN 
    customers c ON o.customer_id = c.customer_id
INNER JOIN 
    order_items oi ON o.order_id = oi.order_id
INNER JOIN 
    products p ON oi.product_id = p.product_id
LEFT JOIN 
    payments pay ON pay.order_id = o.order_id
ORDER BY 
    o.order_date DESC;

