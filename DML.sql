-- Colon : character being used to denote the variables that will have data from the backend programming language

-- Operations for Customers page

-- Create a new customer
INSERT INTO Customers (name, address, phoneNumber, emailAddress)
VALUES (:name_from_input, :address_from_input, phone_number_from_input, :email_from_input);

-- Get all customers to populate customers page
SELECT *
FROM Customers
ORDER BY name ASC;

-- Get customer IDs and names for customer dropdown
SELECT customerID, name
FROM Customers
ORDER BY name ASC;

-- Update customer info
UPDATE Customers
SET
	name = :name_from_input,
    address = :address_from_input,
    phoneNumber = :phone_number_from_input,
    email = :email_from_input
WHERE customerID = :customer_id_from_dropdown;

-- Delete a customer
DELETE
FROM Customers
WHERE customerID = :customer_id_from_dropdown;


-- Operations for the drivers page

-- Create a new driver
INSERT INTO Drivers (name, phoneNumber, carModel)
VALUES (:name_from_input, :phone_number_from_input, :car_model_from_input);

-- Get all drivers to populate drivers page
SELECT *
FROM Drivers
ORDER BY name ASC;

-- Operations for Orders page

-- Get driver IDs and names to populate dropdown
SELECT driverID, name
FROM Drivers
ORDER BY name ASC;

-- Get all pizza IDs and names to populate pizza dropdowns
SELECT pizzaID, name
FROM Pizzas
ORDER BY name ASC;

-- Create a new order
INSERT INTO Orders (customerID, driverID, date)
VALUES (:customer_id_from_dropdown, :driver_id_from_dropdown, :date_from_server);

-- Get all orders to populate orders page
SELECT orderNum, customerID, driverID, price, date, cancelled
FROM Orders
ORDER BY date DESC;

-- Get all order details to populate the orders page
SELECT orderItemID, orderNum, pizzaID, quantity
FROM OrderItems
ORDER BY orderNum;

-- Add an order item to an order
INSERT INTO OrderItems (orderNum, pizzaID, quantity)
VALUES (:order_number_from_order_form, :pizza_id_from_dropdown, :quantity_from_input);

-- Update an order price
UPDATE Orders
SET
	price = (SELECT sum(Pizzas.price) FROM OrderItems JOIN Pizzas ON OrderItems.pizzaID = Pizzas.pizzaID WHERE OrderItems.orderNum = :order_number_from_order_form) 
WHERE orderNum = :order_number_from_order_form;

-- Operations for the Pizzas and Toppings Page 

-- Create a new pizza
INSERT INTO Pizzas (name, price, description)
VALUES (:name_from_input, :price_from_input, :quantity_from_input);

-- Get all pizzas to populate the pizza page
SELECT Pizzas.pizzaID, Pizzas.name, Pizzas.price, Pizzas.description, group_concat(Toppings.name) AS 'toppings'
FROM Pizzas
JOIN PizzaToppings
	ON PizzaToppings.pizzaID = Pizzas.pizzaID
JOIN Toppings
	ON PizzaToppings.toppingID = Toppings.toppingID
GROUP BY Pizzas.pizzaID;

-- Create a new topping
INSERT INTO Toppings (name, price, quantity)
VALUES (:name_from_input, :price_from_input, :quantity_from_input);

-- Get all toppings to populate the pizza page
SELECT toppingID, name, price, quantity
FROM Toppings
ORDER BY toppingID;

-- Get all topping IDs and names to populate topping dropdowns
SELECT toppingID, name
FROM Toppings
ORDER BY name ASC;

-- Add a topping to a pizza
INSERT INTO PizzaToppings (pizzaID, toppingID, quantity)
VALUES (:pizza_id_from_pizza_form, topping_id_from_dropdown, :quantity_from_input);









