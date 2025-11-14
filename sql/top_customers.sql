-- Top Customers by Order Frequency
-- Joins: customers + orders
-- Shows customers with highest order frequency and spending

SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.email,
    c.city,
    c.country,
    c.signup_date,
    COUNT(o.order_id) AS total_orders,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date,
    COUNT(CASE WHEN o.status = 'Delivered' THEN 1 END) AS delivered_orders,
    COUNT(CASE WHEN o.status = 'Cancelled' THEN 1 END) AS cancelled_orders,
    -- Calculate total spent from order_items
    COALESCE((
        SELECT SUM(oi.subtotal)
        FROM order_items oi
        INNER JOIN orders ord ON oi.order_id = ord.order_id
        WHERE ord.customer_id = c.customer_id
    ), 0) AS total_spent
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id, c.name, c.email, c.city, c.country, c.signup_date
HAVING 
    total_orders > 0
ORDER BY 
    total_orders DESC, total_spent DESC
LIMIT 100;

