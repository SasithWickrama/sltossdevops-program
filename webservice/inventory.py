import sqlite3
from tabulate import tabulate


def main():
    choiseList = ["[1] Add Item", "[2] Search Item", "[3] Invoice", "[4] Inventory", "[5] Exit"]
    for lst in choiseList:
        print(lst)

    n = int(input("Enter number of the Operation : "))
    while n != 5:
        if n == 1:
            add()
        if n == 2:
            search()
        if n == 3:
            invoice()
        if n == 4:
            inventory()

    print("Exit")


def add():
    addItem = input("Enter make model unit price (type quit for main menu):")
    val = tuple(addItem.split())
    print(val[0])
    if val[0].lower() != "quit":
        with sqlite3.connect("db.sqlite3") as conn:
            command = "insert into motor_cycle values (?,?,?,?)"
            conn.execute(command, val)
            conn.commit()
    else:
        main()


def search():
    addItem = input("Enter make model (type quit for main menu):")
    val = tuple(addItem.split())
    if val[0] != "quit":
        with sqlite3.connect("db.sqlite3") as conn:
            command = "select *  from motor_cycle where make = ? and model = ?"
            cursor = conn.execute(command, (val[0], val[1]))
            for row in cursor:
                print(row)
    else:
        main()


def invoice():
    addItem = input("Enter make model quantity (type quit for main menu):")
    val = tuple(addItem.split())
    if val[0] != "quit":
        with sqlite3.connect("db.sqlite3") as conn:
            command = "select make,model,price from motor_cycle where make = ? and model = ?"
            cursor = conn.execute(command, (val[0], val[1]))
            for row in cursor:
                make, model, price = row

                data = [[make, model, val[2], str(price), str(price * int(val[2]))]]

                print(list(row))
                print(tabulate(data, headers=["Make", "Model", "Units", "Unit Price", "Total Amount"]))

    else:
        main()


def inventory():
    addItem = input("Do you Want to Display the Inventory (type quit for main menu):")
    val = tuple(addItem.split())
    print(val[0])
    if val[0].lower() != "no":
        with sqlite3.connect("db.sqlite3") as conn:
            command = "select *  from motor_cycle "
            cursor = conn.execute(command)
            for row in cursor:
                print(row)

    else:
        main()


main()
