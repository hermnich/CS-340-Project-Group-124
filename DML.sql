-- Colon : character being used to denote the variables that will have data from the backend programming language

--------------------------------
-- Operations for Customers
--------------------------------

-- Create a new customer
INSERT INTO Customers (name, address, phoneNumber, emailAddress)
VALUES (:name_from_input, :address_from_input, phone_number_from_input, :email_from_input);

-- Get all customers to populate customers page
SELECT *
FROM Customers;

-- Get a specific customer for editing
SELECT * 
FROM Customers 
WHERE customerID = :customer_id_from_customer_table;

-- Get all customerID and names to populate Customers dropdowns
SELECT customerID, name 
FROM Customers;

-- Update customer info
UPDATE Customers
SET
	name = :name_from_input,
    address = :address_from_input,
    phoneNumber = :phone_number_from_input,
    email = :email_from_input
WHERE customerID = :customer_id_from_customer_form;

-- Delete a customer
DELETE
FROM Customers
WHERE customerID = :customer_id_from_customer_table;

--------------------------------
-- Operations for Drivers
--------------------------------

-- Create a new driver
INSERT INTO Drivers (name, phoneNumber, carModel)
VALUES (:name_from_input, :phone_number_from_input, :car_model_from_input);

-- Get all drivers to populate drivers page
SELECT *
FROM Drivers;

-- Get a specific driver for editing
SELECT * 
FROM Drivers 
WHERE driverID = :driver_id_from_driver_table;

-- Get driver IDs and names to populate dropdown
-- Null option will be available as well from the UI
SELECT driverID, name
FROM Drivers;

-- Update driver info
UPDATE Drivers 
SET 
    name = name_from_input, 
    phoneNumber = phone_number_from_input, 
    carModel = car_model_from_input 
WHERE driverID = driver_id_from_driver_form;

-- Delete a driver
DELETE 
FROM Drivers 
WHERE driverID = :driver_id_from_driver_table;

--------------------------------
-- Operations for Orders
--------------------------------

-- Create a new order
INSERT INTO Orders (customerID, driverID, price, date)
VALUES (:customer_id_from_dropdown, :driver_id_from_dropdown, :price_from_server, :date_from_server);
-- Get the ID of the new order to insert order details
SELECT MAX(orderNum)
FROM Orders;

-- Get all orders to populate orders page
SELECT *
FROM Orders;

-- Get order IDs to populate dropdown
SELECT orderID
FROM Orders;

-- Update an order
UPDATE Orders
SET
	price = (SELECT sum(Pizzas.price) FROM OrderItems JOIN Pizzas ON OrderItems.pizzaID = Pizzas.pizzaID WHERE OrderItems.orderNum = :order_number_from_order_form) 
    driverID = :driver_id_from_dropdown
WHERE orderNum = :order_number_from_order_form;

-- Delete an order
DELETE 
FROM Orders 
WHERE orderNum = :Order_number_from_order_table;


--------------------------------
-- Operations for OrderItems
--------------------------------

-- Get all order details to populate the orders page
SELECT *
FROM OrderItems;

-- Get order details for a specific order
SELECT * 
FROM OrderItems 
WHERE orderNum = :order_number_from_order_form;

-- Add an order item to an order
INSERT INTO OrderItems (orderNum, pizzaID, quantity)
VALUES (:order_number_from_order_form, :pizza_id_from_dropdown, :quantity_from_input);

--------------------------------
-- Operations for Pizzas
--------------------------------

-- Create a new pizza
INSERT INTO Pizzas (name, price, description)
VALUES (:name_from_input, :price_from_input, :description_from_input);
-- Get the ID of the new pizza to insert toppings
SELECT LAST_INSERT_ID() as pizzaID;

-- Get all pizzas to populate the pizza page
SELECT Pizzas.pizzaID, Pizzas.name, Pizzas.price, Pizzas.description, group_concat(Toppings.name) AS 'toppings'
FROM Pizzas
JOIN PizzaToppings
	ON PizzaToppings.pizzaID = Pizzas.pizzaID
JOIN Toppings
	ON PizzaToppings.toppingID = Toppings.toppingID
GROUP BY Pizzas.pizzaID;

-- Get specific pizza for editing
SELECT Pizzas.pizzaID, Pizzas.name, Pizzas.price, Pizzas.description, group_concat(Toppings.name) AS 'toppings'
FROM Pizzas
LEFT JOIN PizzaToppings
    ON PizzaToppings.pizzaID = Pizzas.pizzaID
LEFT JOIN Toppings
    ON PizzaToppings.toppingID = Toppings.toppingID
WHERE Pizzas.pizzaID = :pizza_id_from_input
GROUP BY Pizzas.pizzaID;

-- Get the price of a selected pizza
SELECT price 
FROM Pizzas 
WHERE pizzaID = :pizza_id_from_input;

-- Get all pizza IDs and names to populate pizza dropdowns
SELECT pizzaID, name
FROM Pizzas
ORDER BY name ASC;

-- Update a pizza
UPDATE Pizzas 
SET 
    name = :name_from_input, 
    price = :price_from_input, 
    description = :description_from_input 
WHERE pizzaID = :pizza_id_from_input;

-- Delete a pizza
DELETE
FROM Pizzas
WHERE pizzaID = :pizza_id_from_input;

--------------------------------
-- Operations for PizzaToppings
--------------------------------

-- Add a pizza topping
INSERT INTO PizzaToppings (pizzaID, toppingID, quantity)
VALUES (:pizza_id_from_input, topping_id_from_dropdown, :quantity_from_input);

-- Get all pizza toppings for a specific pizza
SELECT PizzaToppings.pizzaToppingID, PizzaToppings.toppingID, Toppings.name, PizzaToppings.quantity
FROM PizzaToppings
JOIN Toppings
    ON PizzaToppings.toppingID = Toppings.toppingID
WHERE pizzaID = :pizza_id_from_input;

-- Update a pizza topping
UPDATE PizzaToppings 
SET 
    toppingID = :topping_id_from_dropdown, 
    quantity = :quantity_from_input 
WHERE pizzaToppingID = :pizza_topping_id_from_input;

-- Delete a pizza topping
DELETE 
FROM PizzaToppings 
WHERE pizzaToppingID = :pizza_topping_id_from_input;

--------------------------------
-- Operations for Toppings
--------------------------------

-- Create a new topping
INSERT INTO Toppings (name, price, quantity)
VALUES (:name_from_input, :price_from_input, :quantity_from_input);

-- Get all toppings to populate the toppings page
SELECT *
FROM Toppings;

-- Get a specific topping for editing
SELECT * 
FROM Toppings 
WHERE toppingID = :topping_id_from_input;

-- Get all topping IDs and names to populate topping dropdowns
SELECT toppingID, name
FROM Toppings;

-- Update a topping
UPDATE Toppings 
SET 
    name = :name_from_input, 
    price = :price_from_input, 
    quantity = :quantity_from_input 
WHERE toppingID = :topping_id_from_input

-- Delete a topping
DELETE 
FROM Toppings 
WHERE toppingID = :topping_id_from_input;








