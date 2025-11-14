-- Best Selling Products Report
-- Joins: products + order_items
-- Shows top selling products by quantity and revenue

SELECT 
    p.product_id,
    p.name AS product_name,
    p.category,
    p.price AS unit_price,
    SUM(oi.quantity) AS total_quantity_sold,
    COUNT(DISTINCT oi.order_id) AS number_of_orders,
    SUM(oi.subtotal) AS total_revenue,
    AVG(oi.quantity) AS avg_quantity_per_order,
    p.stock AS current_stock
FROM 
    products p
INNER JOIN 
    order_items oi ON p.product_id = oi.product_id
GROUP BY 
    p.product_id, p.name, p.category, p.price, p.stock
ORDER BY 
    total_revenue DESC
LIMIT 50;

