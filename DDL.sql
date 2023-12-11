SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- Create Customers Table
DROP TABLE IF EXISTS `Customers`;
CREATE TABLE `Customers` (
	`customerID` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(45) NOT NULL,
	`address` VARCHAR(45),
	`phoneNumber` VARCHAR(45),
	`emailAddress` VARCHAR(45),
	PRIMARY KEY (`customerID`)
);

-- Create Drivers Table
DROP TABLE IF EXISTS `Drivers`;
CREATE TABLE `Drivers` (
	`driverID` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(45) NOT NULL,
	`phoneNumber` VARCHAR(45) NOT NULL,
	`carModel` VARCHAR(45) NOT NULL,
	PRIMARY KEY (`driverID`)
);

-- Create Orders Table
DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders` (
	`orderNum` INT NOT NULL AUTO_INCREMENT,
	`customerID` INT NOT NULL,
	`driverID` INT,
	`price` DECIMAL(5,2) NOT NULL,
	`date` DATETIME NOT NULL,
	PRIMARY KEY (`orderNum`),
	FOREIGN KEY (`customerID`)
		REFERENCES `Customers` (`customerID`)
        ON DELETE CASCADE,
	FOREIGN KEY (`driverID`)
		REFERENCES `Drivers` (`driverID`)
        ON DELETE SET NULL
);

-- Create Toppings Table
DROP TABLE IF EXISTS `Toppings`;
CREATE TABLE `Toppings` (
	`toppingID` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(45) NOT NULL,
	`price` DECIMAL(5,2) NOT NULL,
	`quantity` INT NOT NULL,
	PRIMARY KEY (`toppingID`)
);

-- Create Pizzas Table
DROP TABLE IF EXISTS `Pizzas`;
CREATE TABLE `Pizzas` (
	`pizzaID` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(45) NOT NULL,
	`price` DECIMAL(5,2) NOT NULL,
	`description` VARCHAR(255),
	PRIMARY KEY (`pizzaID`)
);

-- Create OrderItems Table
DROP TABLE IF EXISTS `OrderItems`;
CREATE TABLE `OrderItems` (
	`orderItemID` INT NOT NULL AUTO_INCREMENT,
	`orderNum` INT NOT NULL,
	`pizzaID` INT NOT NULL,
	`quantity` INT NOT NULL,
	PRIMARY KEY (`orderItemID`),
	FOREIGN KEY (`orderNum`)
		REFERENCES `Orders` (`orderNum`)
        ON DELETE CASCADE,
	FOREIGN KEY (`pizzaID`)
		REFERENCES `Pizzas` (`pizzaID`)
        ON DELETE RESTRICT
);

-- Create PizzaToppings Table
DROP TABLE IF EXISTS `PizzaToppings`;
CREATE TABLE `PizzaToppings` (
	`pizzaToppingID` INT NOT NULL AUTO_INCREMENT,
    `pizzaID` INT NOT NULL,
    `toppingID` INT NOT NULL,
    `quantity` INT NOT NULL,
    PRIMARY KEY (`pizzaToppingID`),
    FOREIGN KEY (`pizzaID`)
		REFERENCES `Pizzas` (`pizzaID`)
        ON DELETE CASCADE,
	FOREIGN KEY (`toppingID`)
		REFERENCES `Toppings` (`toppingID`)
        ON DELETE CASCADE
);

-- Populate Customers Table
INSERT INTO `Customers` (`name`, `address`, `phoneNumber`, `emailAddress`)
VALUES 
("Jeff", "123 Street Ave.", "111-2222-3333", "name@email.com"),
("Anthony", "8874 Circle Dr.", "444-5555-6666", "example@host.net"),
("Penelope", "1337 Avenue Blvd.", "777-8888-9999", "myemail@thisisatest.com");

-- Populate Drivers Table
INSERT INTO `Drivers` (`name`, `phoneNumber`, `carModel`)
VALUES 
("Phil", "333-2222-1111", "Acura"),
("Amelia", "666-5555-4444", "Ram"),
("Ed", "999-8888-7777", "Ranger");

-- Populate Toppings Table
INSERT INTO `Toppings` (`name`, `price`, `quantity`)
VALUES 
("Pepperoni", 0.50, 9),
("Mushroom", 1.14, 4),
("Sausage", 0.37, 6);

-- Populate Pizzas Table
INSERT INTO `Pizzas` (`name`, `price`, `description`)
VALUES 
("Pepperoni Extreme", 9.99, "As much pepperoni as a pizza can hold"),
("Mushroom Madness", 13.22, "A delicious circle of mushroom-y goodness"),
("Meaty Mayhem", 8.45, "More meats than Arby's");

-- Populate PizzaToppings Table
INSERT INTO `PizzaToppings` (`pizzaID`, `toppingID`, `quantity`)
VALUES
((SELECT `pizzaID` FROM `Pizzas` WHERE `name` = "Pepperoni Extreme"), (SELECT `toppingID` FROM `Toppings` WHERE `name` = "Pepperoni"), 3),
((SELECT `pizzaID` FROM `Pizzas` WHERE `name` = "Mushroom Madness"), (SELECT `toppingID` FROM `Toppings` WHERE `name` = "Mushroom"), 2),
((SELECT `pizzaID` FROM `Pizzas` WHERE `name` = "Meaty Mayhem"), (SELECT `toppingID` FROM `Toppings` WHERE `name` = "Pepperoni"), 1),
((SELECT `pizzaID` FROM `Pizzas` WHERE `name` = "Meaty Mayhem"), (SELECT `toppingID` FROM `Toppings` WHERE `name` = "Sausage"), 1);


-- Populate Orders Table
INSERT INTO `Orders` (`customerID`, `driverID`, `price`, `date`)
VALUES 
((SELECT `customerID` FROM `Customers` WHERE `name` = "Anthony"), (SELECT `driverID` FROM `Drivers` WHERE `name` = "Phil"), 10.23, '2023-04-26'),
((SELECT `customerID` FROM `Customers` WHERE `name` = "Anthony"), (SELECT `driverID` FROM `Drivers` WHERE `name` = "Ed"), 36.83, '2021-08-13'),
((SELECT `customerID` FROM `Customers` WHERE `name` = "Jeff"), (SELECT `driverID` FROM `Drivers` WHERE `name` = "Phil"), 26.99, '2022-11-08');


-- Populate OrderItems Table
INSERT INTO `OrderItems` (`orderNum`, `pizzaID`, `quantity`)
VALUES 
(1, (SELECT `pizzaID` FROM `Pizzas` WHERE `name` = "Pepperoni Extreme"), 1),
(2, (SELECT `pizzaID` FROM `Pizzas` WHERE `name` = "Pepperoni Extreme"), 3),
(3, (SELECT `pizzaID` FROM `Pizzas` WHERE `name` = "Mushroom Madness"), 1),
(3, (SELECT `pizzaID` FROM `Pizzas` WHERE `name` = "Meaty Mayhem"), 1);


SET FOREIGN_KEY_CHECKS=1;
COMMIT;


