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
app.config["MYSQL_USER"] = "cs340_"
app.config["MYSQL_PASSWORD"] = "EFsD2wR1kAsV"
app.config["MYSQL_DB"] = "cs340_"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "brian"
# app.config["MYSQL_PASSWORD"] = ""
# app.config["MYSQL_DB"] = "project_schema"
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


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=42067, debug=True)
