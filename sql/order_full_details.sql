-- Full Order Details Report
-- Joins: All tables (customers, products, orders, order_items, payments)
-- Comprehensive view of complete order information

SELECT 
    o.order_id,
    o.order_date,
    o.status AS order_status,
    
    -- Customer Information
    c.customer_id,
    c.name AS customer_name,
    c.email AS customer_email,
    c.city AS customer_city,
    c.country AS customer_country,
    
    -- Product and Order Item Information
    oi.order_item_id,
    p.product_id,
    p.name AS product_name,
    p.category AS product_category,
    oi.quantity,
    oi.subtotal AS item_subtotal,
    p.price AS unit_price,
    
    -- Payment Information
    pay.payment_id,
    pay.amount AS payment_amount,
    pay.payment_method,
    pay.payment_status,
    
    -- Calculated Fields
    (
        SELECT SUM(oi2.subtotal)
        FROM order_items oi2
        WHERE oi2.order_id = o.order_id
    ) AS order_total,
    
    (
        SELECT COUNT(*)
        FROM order_items oi3
        WHERE oi3.order_id = o.order_id
    ) AS total_items_in_order

FROM 
    orders o
INNER JOIN 
    customers c ON o.customer_id = c.customer_id
INNER JOIN 
    order_items oi ON o.order_id = oi.order_id
INNER JOIN 
    products p ON oi.product_id = p.product_id
LEFT JOIN 
    payments pay ON o.order_id = pay.order_id
ORDER BY 
    o.order_date DESC, o.order_id, oi.order_item_id;

