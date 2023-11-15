# Sample Flask application for a BSG database, snapshot of BSG_people

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection
# Template:
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

mysql = MySQL(app)

# Routes
# have homepage route to /people by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return redirect("/customers")


# route for customers page
@app.route("/customers", methods=["POST", "GET"])
def customers():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Customer"):
            # grab user form inputs
            name = request.form["name"]
            address = request.form["address"]
            phone = request.form["phone"]
            email = request.form["email"]

            # account for null age AND homeworld
            # if age == "" and homeworld == "0":
            #     # mySQL query to insert a new person into bsg_people with our form inputs
            #     query = "INSERT INTO bsg_people (fname, lname) VALUES (%s, %s)"
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (fname, lname))
            #     mysql.connection.commit()

            # account for null homeworld
            # elif homeworld == "0":
            #    query = "INSERT INTO bsg_people (fname, lname, age) VALUES (%s, %s,%s)"
            #    cur = mysql.connection.cursor()
            #    cur.execute(query, (fname, lname, age))
            #    mysql.connection.commit()

            # account for null age
            # elif age == "":
            #    query = "INSERT INTO bsg_people (fname, lname, homeworld) VALUES (%s, %s,%s)"
            #    cur = mysql.connection.cursor()
            #    cur.execute(query, (fname, lname, homeworld))
            #    mysql.connection.commit()

            # no null inputs
            # else:
            query = "INSERT INTO Customers (name, address, phoneNumber, emailAddress) VALUES (%s, %s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, address, phone, email))
            mysql.connection.commit()

            # redirect back to customers page
            return redirect("/customers")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT * from Customers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        # query2 = "SELECT id, name FROM bsg_planets"
        # cur = mysql.connection.cursor()
        # cur.execute(query2)
        # homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("customers.j2", data=data)


# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_customer/<int:customerID>")
def delete_customers(customerID):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Customers WHERE customerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (customerID,))
    mysql.connection.commit()

    # redirect back to customers page
    return redirect("/customers")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_customer/<int:customerID>", methods=["POST", "GET"])
def edit_customer(customerID):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Customers WHERE customerID = %s" % (customerID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        # query2 = "SELECT id, name FROM bsg_planets"
        # cur = mysql.connection.cursor()
        # cur.execute(query2)
        # homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_customers.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Customer' button
        if request.form.get("Edit_Customer"):
            # grab user form inputs
            # id = request.form["personID"]
            name = request.form["name"]
            address = request.form["address"]
            phone = request.form["phone"]
            email = request.form["email"]

            # # account for null age AND homeworld
            # if (age == "" or age == "None") and homeworld == "0":
            #     # mySQL query to update the attributes of person with our passed id value
            #     query = "UPDATE customers SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = NULL WHERE bsg_people.id = %s"
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (fname, lname, id))
            #     mysql.connection.commit()

            # # account for null homeworld
            # elif homeworld == "0":
            #     query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = %s WHERE bsg_people.id = %s"
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (fname, lname, age, id))
            #     mysql.connection.commit()

            # # account for null age
            # elif age == "" or age == "None":
            #     query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = NULL WHERE bsg_people.id = %s"
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (fname, lname, homeworld, id))
            #     mysql.connection.commit()

            # no null inputs
            # else:
            query = "UPDATE customers SET customers.name = %s, customers.address = %s, customers.phoneNumber = %s, customers.emailAddress = %s WHERE customers.customerID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, address, phone, email, customerID))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/customers")


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=42067, debug=True)
