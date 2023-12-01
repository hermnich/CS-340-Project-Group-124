# Citation for the following code:
# Date: 2023/11/15
# Based on:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/tree/master/bsg_people_app

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection
# Template: oops
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_walsbria"
app.config["MYSQL_PASSWORD"] = "EFsD2wR1kAsV"
app.config["MYSQL_DB"] = "cs340_walsbria"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "brian"
# app.config["MYSQL_PASSWORD"] = ""
# app.config["MYSQL_DB"] = "project_schema"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "root"
# app.config["MYSQL_DB"] = "testdb"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# have homepage route to /customers for now
@app.route("/")
def home():
    return redirect("/customers")

# route for customers page
@app.route("/customers", methods=["POST", "GET"])
def customers():

    # insert a new customer
    if request.method == "POST":
        # fire off if user clicks the 'Add Customer' button
        if request.form.get("Add_Customer"):
            # grab user form inputs
            name = request.form["name"]
            address = request.form["address"]
            phone = request.form["phone"]
            email = request.form["email"]

            # account for null email
            if email == "":
                query = "INSERT INTO Customers (name, address, phoneNumber) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, address, phone))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Customers (name, address, phoneNumber, emailAddress) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, address, phone, email))
                mysql.connection.commit()

            # redirect back to customers page
            return redirect("/customers")

    # Get all customer data to display
    if request.method == "GET":
        query = "SELECT * from Customers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render customers page
        return render_template("customers.j2", data=data)


# route for delete functionality, deleting a customer,
# customer id is passed via route parameter
@app.route("/delete_customer/<int:customerID>")
def delete_customers(customerID):
    query = "DELETE FROM Customers WHERE customerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (customerID,))
    mysql.connection.commit()

    # redirect back to customers page
    return redirect("/customers")


# route for edit functionality, updating a customer
# customer id is passed via route parameter
@app.route("/edit_customer/<int:customerID>", methods=["POST", "GET"])
def edit_customer(customerID):
    if request.method == "GET":
        # Get the info of the customer with our passed id
        query = "SELECT * FROM Customers WHERE customerID = %s" % (customerID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_customers page
        return render_template("edit_customers.j2", data=data)

    # Update the customer
    if request.method == "POST":
        # fire off if user clicks the 'Edit Customer' button
        if request.form.get("Edit_Customer"):
            # grab user form inputs
            name = request.form["name"]
            address = request.form["address"]
            phone = request.form["phone"]
            email = request.form["email"]

            # account for null email
            if (email == ""):
                query = "UPDATE Customers SET name = %s, address = %s, phoneNumber = %s, emailAddress = NULL WHERE customerID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, address, phone, customerID))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Customers SET name = %s, address = %s, phoneNumber = %s, emailAddress = %s WHERE customerID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, address, phone, email, customerID))
                mysql.connection.commit()

            # redirect back to customers page
            return redirect("/customers")


# route for drivers page
@app.route("/drivers", methods=["POST", "GET"])
def drivers():

    # insert a new driver
    if request.method == "POST":
        # fire off if user clicks the 'Add Driver' button
        if request.form.get("Add_Driver"):
            # grab user form inputs
            name = request.form["name"]
            phone = request.form["phone"]
            car = request.form["car"]

            # no null inputs
            query = "INSERT INTO Drivers (name, phoneNumber, carModel) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, phone, car))
            mysql.connection.commit()

            # redirect back to drivers page
            return redirect("/drivers")

    # Get all driver data to display
    if request.method == "GET":
        query = "SELECT * from Drivers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render drivers page
        return render_template("drivers.j2", data=data)


# route for delete functionality, deleting a driver,
# driver id is passed via route parameter
@app.route("/delete_driver/<int:driverID>")
def delete_driver(driverID):
    query = "DELETE FROM Drivers WHERE driverID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (driverID,))
    mysql.connection.commit()

    # redirect back to drivers page
    return redirect("/drivers")


# route for edit functionality, updating a driver
# driver id is passed via route parameter
@app.route("/edit_driver/<int:driverID>", methods=["POST", "GET"])
def edit_driver(driverID):
    if request.method == "GET":
        # Get the info of the driver with our passed id
        query = "SELECT * FROM Drivers WHERE driverID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (driverID,))
        data = cur.fetchall()

        # render edit_drivers page
        return render_template("edit_drivers.j2", data=data)

    # Update the driver
    if request.method == "POST":
        # fire off if user clicks the 'Edit Driver' button
        if request.form.get("Edit_Driver"):
            # grab user form inputs
            name = request.form["name"]
            phone = request.form["phone"]
            car = request.form["car"]

            # no null inputs
            query = "UPDATE Drivers SET name = %s, phoneNumber = %s, carModel = %s WHERE driverID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, phone, car, driverID))
            mysql.connection.commit()

            # redirect back to drivers page
            return redirect("/drivers")
        
        
# route for pizzas page
@app.route("/pizzas", methods=["GET"])
def pizzas():
    # Get all pizza data to display
    if request.method == "GET":
        query = ("SELECT Pizzas.pizzaID, Pizzas.name, Pizzas.price, Pizzas.description, group_concat(Toppings.name) AS 'toppings' "
                "FROM Pizzas "
                "LEFT JOIN PizzaToppings "
                    "ON PizzaToppings.pizzaID = Pizzas.pizzaID "
                "LEFT JOIN Toppings "
                    "ON PizzaToppings.toppingID = Toppings.toppingID "
                "GROUP BY Pizzas.pizzaID;")
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render pizzas page
        return render_template("pizzas.j2", data=data)
    
# route for add functionality, creating a new pizza
@app.route("/add_pizza", methods=["GET", "POST"])
def add_pizza():

    # insert a new pizza
    if request.method == "POST":
        # fire off if user clicks the 'Add Pizza' button
        if request.form.get("Add_Pizza"):
            # grab user form inputs
            values = json.loads(request.form["values"].replace("'", "\""))
            name = request.form["name"]
            price = request.form["price"]
            desc = request.form["desc"]

            cur = mysql.connection.cursor()

            # Account for null description
            if desc == "":
                query = "INSERT INTO Pizzas (name, price, description) VALUES (%s, %s, %s)"
                cur.execute(query, (name, price, desc))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Pizzas (name, price, description) VALUES (%s, %s, %s)"
                cur.execute(query, (name, price, desc))
                mysql.connection.commit()
            
            cur.execute("SELECT LAST_INSERT_ID() as pizzaID")
            pizzaID = cur.fetchall()
            pizzaID = pizzaID[0]["pizzaID"]

            for topping in values["toppings"]:
                query = "INSERT INTO PizzaToppings (pizzaID, toppingID, quantity) VALUE (%s, %s, %s)"
                cur.execute(query, (pizzaID, topping["toppingID"], topping["quantity"]))
                mysql.connection.commit()

            # redirect back to pizzas page
            return redirect("/pizzas")
        
        # fire off if user clicks the 'Save' button on one of the toppings
        if request.form.get("Edit_Pizza_Topping"):
            # grab user form inputs
            values = json.loads(request.form["values"].replace("'", "\""))
            toppingID = request.form["toppingID"]
            qty = request.form["qty"]
            index = request.form["index"]

            values["toppings"][int(index)] = {"toppingID": toppingID, "quantity": qty}

            # Get list of all topping names and id
            query = "SELECT * FROM Toppings"
            cur = mysql.connection.cursor()
            cur.execute(query)
            topping_list = cur.fetchall()

            # redirect back to pizzas page
            return render_template("add_pizza.j2", values=values, topping_list=topping_list)
        
        # fire off if user clicks the 'Add Topping' button
        if request.form.get("Add_Pizza_Topping"):
            # grab user form inputs
            values = json.loads(request.form["values"].replace("'", "\""))
            toppingID = request.form["toppingID"]
            qty = request.form["qty"]
            values["toppings"].append({"toppingID": toppingID, "quantity": qty})

            # Get list of all topping names and id
            query = "SELECT * FROM Toppings"
            cur = mysql.connection.cursor()
            cur.execute(query)
            topping_list = cur.fetchall()

            # redirect back to pizzas page
            return render_template("add_pizza.j2", values=values, topping_list=topping_list)
        
        # fire off if user clicks the 'Delete' button on one of the toppings
        if request.form.get("Delete_Pizza_Topping"):
            # grab user form inputs
            values = json.loads(request.form["values"].replace("'", "\""))
            index = request.form["index"]
            toppingID = request.form["toppingID"]
            qty = request.form["qty"]

            del values["toppings"][int(index)]

            # Get list of all topping names and id
            query = "SELECT * FROM Toppings"
            cur = mysql.connection.cursor()
            cur.execute(query)
            topping_list = cur.fetchall()

            # redirect back to pizzas page
            return render_template("add_pizza.j2", values=values, topping_list=topping_list)
        
    
    # Get all pizza data to display
    if request.method == "GET":

        # Get list of all topping names and id
        query = "SELECT * FROM Toppings"
        cur = mysql.connection.cursor()
        cur.execute(query)
        topping_list = cur.fetchall()

        values = {
            "pizza":
                {
                    "name": "",
                    "price": "",
                    "description": ""
                },
            "toppings": []
        }

        # render pizzas page
        return render_template("add_pizza.j2", values=values, topping_list=topping_list)


# route for delete functionality, deleting a pizza,
# pizza id is passed via route parameter
@app.route("/delete_pizza/<int:pizzaID>")
def delete_pizza(pizzaID):
    query = "DELETE FROM Pizzas WHERE pizzaID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (pizzaID,))
    mysql.connection.commit()

    # redirect back to pizzas page
    return redirect("/pizzas")


# route for edit functionality, updating a pizza
# pizza id is passed via route parameter
@app.route("/edit_pizza/<int:pizzaID>", methods=["POST", "GET"])
def edit_pizza(pizzaID):
    if request.method == "GET":
        # Get the info of the pizza with our passed id
        query = ("SELECT Pizzas.pizzaID, Pizzas.name, Pizzas.price, Pizzas.description, group_concat(Toppings.name) AS 'toppings' "
                "FROM Pizzas "
                "LEFT JOIN PizzaToppings "
                    "ON PizzaToppings.pizzaID = Pizzas.pizzaID "
                "LEFT JOIN Toppings "
                    "ON PizzaToppings.toppingID = Toppings.toppingID "
                "WHERE Pizzas.pizzaID = '%s'"
                "GROUP BY Pizzas.pizzaID;")
        cur = mysql.connection.cursor()
        cur.execute(query, (pizzaID,))
        pizza_data = cur.fetchall()

        # Get the info of the pizza toppings with our passed id
        query = ("SELECT PizzaToppings.pizzaToppingID, PizzaToppings.toppingID, Toppings.name, PizzaToppings.quantity "
                 "FROM PizzaToppings "
                 "JOIN Toppings "
                    "ON PizzaToppings.toppingID = Toppings.toppingID "
                 "WHERE pizzaID = '%s';")
        cur = mysql.connection.cursor()
        cur.execute(query, (pizzaID,))
        topping_data = cur.fetchall()

        # Get list of all topping names and id
        query = "SELECT * FROM Toppings"
        cur = mysql.connection.cursor()
        cur.execute(query)
        topping_list = cur.fetchall()

        # render edit_pizzas page
        return render_template("edit_pizzas.j2", pizza_data=pizza_data, topping_data=topping_data, topping_list=topping_list)

    # Update the pizza
    if request.method == "POST":
        # fire off if user clicks the 'Edit Pizza' button
        if request.form.get("Edit_Pizza"):
            # grab user form inputs
            name = request.form["name"]
            price = request.form["price"]
            desc = request.form["desc"]

            # Account for null description
            if desc == "":
                query = "UPDATE Pizzas SET name = %s, price = %s, description = %s WHERE pizzaID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, price, desc, pizzaID))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Pizzas SET name = %s, price = %s, description = %s WHERE pizzaID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, price, desc, pizzaID))
                mysql.connection.commit()

            # redirect back to pizzas page
            return redirect("/pizzas")
        
# route for delete functionality, deleting a pizza topping,
# pizza id is passed via route parameter
@app.route("/edit_pizza/<int:pizzaID>/delete_pizza_topping/<int:pizzaToppingID>")
def delete_pizza_topping(pizzaID, pizzaToppingID):
    query = "DELETE FROM PizzaToppings WHERE pizzaToppingID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (pizzaToppingID,))
    mysql.connection.commit()

    # redirect back to edit pizzas page
    return redirect("/edit_pizza/%d" % pizzaID)

# route for edit functionality, updating a pizza topping
# pizza id is passed via route parameter
@app.route("/edit_pizza/<int:pizzaID>/edit_pizza_topping/<int:pizzaToppingID>", methods=["POST"])
def edit_pizza_topping(pizzaID, pizzaToppingID):
    # Update the pizza topping
    # fire off if user clicks the 'Edit Pizza' button
    if request.form.get("Edit_Pizza_Topping"):
        # grab user form inputs
        toppingID = request.form["toppingID"]
        qty = request.form["qty"]

        # no null inputs
        query = "UPDATE PizzaToppings SET toppingID = %s, quantity = %s WHERE pizzaToppingID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (toppingID, qty, pizzaToppingID))
        mysql.connection.commit()

        # redirect back to pizzas page
        return redirect("/edit_pizza/%d" % pizzaID)
    
# route for add functionality, inserting a pizza topping
@app.route("/edit_pizza/<int:pizzaID>/add_pizza_topping", methods=["POST"])
def add_pizza_topping(pizzaID):
    # Update the pizza topping
    # fire off if user clicks the 'Edit Pizza' button
    if request.form.get("Add_Pizza_Topping"):
        # grab user form inputs
        toppingID = request.form["toppingID"]
        qty = request.form["qty"]

        # no null inputs
        query = "INSERT INTO PizzaToppings (pizzaID, toppingID, quantity) VALUES (%s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (pizzaID, toppingID, qty))
        mysql.connection.commit()

        # redirect back to pizzas page
        return redirect("/edit_pizza/%d" % pizzaID)
    
# route for toppings page
@app.route("/toppings", methods=["POST", "GET"])
def toppings():

    # insert a new topping
    if request.method == "POST":
        # fire off if user clicks the 'Add Topping' button
        if request.form.get("Add_Topping"):
            # grab user form inputs
            name = request.form["name"]
            price = request.form["price"]
            qty = request.form["qty"]

            # no null inputs
            query = "INSERT INTO Toppings (name, price, quantity) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, price, qty))
            mysql.connection.commit()

            # redirect back to drivers page
            return redirect("/toppings")

    # Get all topping data to display
    if request.method == "GET":
        query = "SELECT * from Toppings"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render drivers page
        return render_template("toppings.j2", data=data)


# route for delete functionality, deleting a topping,
# topping id is passed via route parameter
@app.route("/delete_topping/<int:toppingID>")
def delete_topping(toppingID):
    query = "DELETE FROM Toppings WHERE toppingID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (toppingID,))
    mysql.connection.commit()

    # redirect back to drivers page
    return redirect("/toppings")


# route for edit functionality, updating a topping
# topping id is passed via route parameter
@app.route("/edit_topping/<int:toppingID>", methods=["POST", "GET"])
def edit_topping(toppingID):
    if request.method == "GET":
        # Get the info of the topping with our passed id
        query = "SELECT * FROM Toppings WHERE toppingID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (toppingID,))
        data = cur.fetchall()

        # render edit_toppings page
        return render_template("edit_toppings.j2", data=data)

    # Update the topping
    if request.method == "POST":
        # fire off if user clicks the 'Edit Topping' button
        if request.form.get("Edit_Topping"):
            # grab user form inputs
            name = request.form["name"]
            price = request.form["price"]
            qty = request.form["qty"]

            # no null inputs
            query = "UPDATE Toppings SET name = %s, price = %s, quantity = %s WHERE toppingID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, price, qty, toppingID))
            mysql.connection.commit()

            # redirect back to toppings page
            return redirect("/toppings")

# route for orders page
@app.route("/orders", methods=["POST", "GET"])
def orders():
        
    # create a new order
    if request.method == "POST":
        # fire off if user clicks the 'Add Topping' button
        if request.form.get("Submit_Order"):
            # grab user form inputs
            pizza1 = request.form["pizza_1"]
            qty1 = request.form["pizza_1_qty"]
            price = 10
            pizza2 = request.form["pizza_2"]
            qty2 = request.form["pizza_2_qty"]
            pizza3 = request.form["pizza_3"]
            qty3 = request.form["pizza_3_qty"]
            cust_id = request.form["customerID"]
            driver_id = request.form["driverID"]

            # first enter customer and driver and price in to orders, then get order ID and fill out orderitems
            query = "INSERT INTO Orders (customerID, driverID, price) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (cust_id, driver_id, price))
            mysql.connection.commit()

            # get the most recent order number. figure out how to do by date
            query = "SELECT MAX(orderNum) from Orders"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
            order_number = data[0]
            order_number = int(order_number['MAX(orderNum)'])

            # write order data to orderItems
            query = "INSERT INTO OrderItems (orderNum, pizzaID, quantity) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            # print(query, (order_number, pizza1, qty1))
            cur.execute(query, (order_number, pizza1, qty1))
            mysql.connection.commit()

            if pizza2 != "":
                query = "INSERT INTO OrderItems (orderNum, pizzaID, quantity) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (order_number, pizza2, qty2))
                mysql.connection.commit()

            if pizza3 != "":
                query = "INSERT INTO OrderItems (orderNum, pizzaID, quantity) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (order_number, pizza3, qty3))
                mysql.connection.commit()

            return redirect("/orders")


    # Get all orders to display
    if request.method == "GET":
        query = "SELECT * from Orders"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render orders page
        return render_template("orders.j2", data=data)


# route for order details page
@app.route("/orderdetails", methods=["POST", "GET"])
def orderdetails():
    # Get all orders to display
    if request.method == "GET":
        query = "SELECT * from OrderItems"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render orders page
        return render_template("orderdetails.j2", data=data)

# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=42067, debug=True)
