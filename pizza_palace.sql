-- Create Customers Table
CREATE TABLE IF NOT EXISTS `Customers` (
	`customerID` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(45),
	`address` VARCHAR(45),
	`phoneNumber` VARCHAR(45),
	`emailAddress` VARCHAR(45),
	PRIMARY KEY (`customerID`)
);


-- Create Drivers Table
CREATE TABLE IF NOT EXISTS `Drivers` (
	`driverID` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(45),
	`phoneNumber` VARCHAR(45),
	`carModel` VARCHAR(45),
	PRIMARY KEY (`driverID`)
);


-- Create Orders Table
CREATE TABLE IF NOT EXISTS `Orders` (
	`orderNum` INT NOT NULL AUTO_INCREMENT,
	`customerID` INT,
	`driverID` INT,
	`price` DECIMAL,
	`date` DATETIME,
	`cancelled` TINYINT NOT NULL DEFAULT 0,
	PRIMARY KEY (`orderNum`),
	FOREIGN KEY (`customerID`)
		REFERENCES `Customers` (`customerID`),
	FOREIGN KEY (`driverID`)
		REFERENCES `Drivers` (`driverID`)
);


-- Create Toppings Table
CREATE TABLE IF NOT EXISTS `mydb`.`Toppings` (
	`toppingID` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(45),
	`price` DECIMAL,
	`quantity` INT,
	PRIMARY KEY (`toppingID`)
);


-- Create Pizzas Table
CREATE TABLE IF NOT EXISTS `Pizzas` (
`pizzaID` INT NOT NULL AUTO_INCREMENT,
`name` VARCHAR(45),
`price` DECIMAL,
`description` VARCHAR(45),
`topping1` INT,
`topping2` INT,
`topping3` INT,
`topping4` INT,
`topping5` INT,
PRIMARY KEY (`pizzaID`),
FOREIGN KEY (`topping1`)
	REFERENCES `Toppings` (`toppingID`),
FOREIGN KEY (`topping2`)
	REFERENCES `Toppings` (`toppingID`),
FOREIGN KEY (`topping3`)
	REFERENCES `Toppings` (`toppingID`),
FOREIGN KEY (`topping4`)
	REFERENCES `Toppings` (`toppingID`),
FOREIGN KEY (`topping5`)
	REFERENCES `Toppings` (`toppingID`)
);


-- Create OrderItems Table
CREATE TABLE IF NOT EXISTS `OrderItems` (
`orderItemID` INT NOT NULL AUTO_INCREMENT,
`orderNum` INT NOT NULL,
`pizzaID` INT NOT NULL,
`quantity` INT,
PRIMARY KEY (`orderItemID`),
FOREIGN KEY (`orderNum`)
	REFERENCES `Orders` (`orderNum`),
FOREIGN KEY (`pizzaID`)
	REFERENCES `Pizzas` (`pizzaID`)
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
INSERT INTO `Pizzas` (`name`, `price`, `description`, `topping1`, `topping2`, `topping3`, `topping4`, `topping5`)
VALUES 
("Pepperoni Extreme", 9.99, "As much pepperoni as a pizza can hold", , , , , ),
("Mushroom Madness", 13.22, "A delicious circle of mushroom-y goodness", , , , , ),
("Meaty Mayhem", 8.45, "More meats than Arby's", , , , , );

-- Populate Orders Table
INSERT INTO `Orders` (`customerID`, `driverID`, `price`, `date`, `cancelled`)
VALUES 
(, , , , ),
(, , , , ),
(, , , , );

-- Populate OrderItems Table
INSERT INTO `OrderItems` (`orderNum`, `pizzaID`, `quantity`)
VALUES 
(, , ),
(, , ),
(, , );





