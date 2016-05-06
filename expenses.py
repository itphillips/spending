# script to interact with expenses db
# Fill in db_type and db_path in config.py

import datetime
import calendar
import config
from db_connect import db_connect
import sql_expressions

db = db_connect(config.db_type, config.db_path)

# these return dicts
cur = db['cur']
conn = db['conn']

# these return tuples
norm_conn = db['norm_conn']
norm_cur = db['norm_cur']

sql_expressions.create_tables(cur, config.db_type)


def enter_name():
    name = str.capitalize(raw_input("What name do you want to enter? "))
    cur.execute("INSERT INTO person(name) VALUES (?)", (name, ))


def show_all_names():
    ournames = cur.execute("SELECT name FROM person ORDER BY name")
    print("These are all the names:")
    for row in ournames:
        print(row['name'])


def show_all_payments():
    norm_cur.execute('''
            SELECT person.name, payments.name,
            payments.amount, payments.paydate, payments.note
            FROM payments, person
            WHERE person.id=payments.payer_id;
    ''')
    allpayments = norm_cur.fetchall()
    print("These are all the payments:")
    for payment in allpayments:
        print("%s paid %s $%s on %s for %s" % (payment))


def enter_payment():
    user = str.capitalize(raw_input("Who paid? "))
    cur.execute("SELECT * FROM person WHERE name=?", (user, ))
    user_record = cur.fetchone()
    user_id = int(user_record['id'])
    # print type(user_id)

    paymentname = raw_input("Who did %s pay? " % user)
    amount = float(input("Amount: "))
    paymentdate = raw_input("Date of payment: ")

    print("Expense types: ")
    existingexpensetypes = cur.execute(
        "SELECT expensetype FROM expensetypes ORDER BY expensetype")
    expensetypelist = cur.fetchall()
    for row in expensetypelist:
        print(row['expensetype'])
    expensetype = raw_input("Pick an expense type: ")
    cur.execute("SELECT * FROM expensetypes WHERE expensetype=?",
                (expensetype, ))
    expensetype_record = cur.fetchone()
    expensetype_id = int(expensetype_record['id'])
    # print type(expensetype_id)

    paymentnote = raw_input("Describe what the payment is for: ")

    print("%s paid %s $%.2f on %s for %s: %s" % (
        user, paymentname, amount, paymentdate, expensetype, paymentnote))
    correct = raw_input("Is this correct (y/n): ")
    if correct == "y":
        cur.execute('''INSERT INTO payments(
        name, amount, paydate, payer_id,
        expensetype_id, note)
        VALUES (?, ?, ?, ?, ?, ?)''', (paymentname,
                                       amount,
                                       paymentdate,
                                       user_id,
                                       expensetype_id,
                                       paymentnote, ))
        print("Added your payment to the db!")
    else:
        print("not saved to db! enter this payment again!")


def enter_expense_type():
    print "These are the current expense types: "
    existingepensetypes = cur.execute(
        "SELECT expensetype FROM expensetypes ORDER BY expensetype")
    expensetypelist = cur.fetchall()
    for row in expensetypelist:
        print(row['expensetype'])

    expense_type = raw_input(
        "What kind of expense type do you want to add to the db? (type 'q' to go back): ")
    if expense_type == "":
        print "Try again."
        enter_expense_type()
    elif expense_type == "q":
        main()
    else:
        cur.execute("INSERT INTO expensetypes(expensetype) VALUES (?)",
                    (expense_type, ))
        print "Added %s to expensetypes db!" % (expense_type)


def month_totals():
    user = str.capitalize(raw_input("Who do you want to see totals for? "))
    month = str.capitalize(raw_input(
        "What month do you want to see totals for? "))
    year = input("What year? ")
    monthdict = {'January': 1,
                 'February': 2,
                 'March': 3,
                 'April': 4,
                 'May': 5,
                 'June': 6,
                 'July': 7,
                 'August': 8,
                 'September': 9,
                 'October': 10,
                 'November': 11,
                 'December': 12}
    monthnum = monthdict[month]
    firstday = 1
    lastday = calendar.monthrange(year, monthnum)[1]
    cur.execute("SELECT * FROM person WHERE name=?", (user, ))
    user_record = cur.fetchone()
    user_id = int(user_record['id'])

    paymentsbyuser = norm_cur.execute(
        "SELECT SUM(payments.amount) FROM payments INNER JOIN person ON payments.payer_id = person.id WHERE person.id=? AND payments.paydate BETWEEN ? and ?;",
        (user_id,
         datetime.date(year, monthnum, firstday),
         datetime.date(year, monthnum, lastday), ))
    userpayment = norm_cur.fetchone()
    if userpayment[0] == None:
        print('No payments for this period')
    else:
        print("%s paid $%s in %s %s" % (user, userpayment[0], month, year))


def main():
    task = raw_input(
        "What do you want to do? Pick a number. \n(1) enter payment \n(2) enter name \n(3) see names \n(4) see payments \n(5) enter expense types \n(6) see payments by month for user \n: ")

    if task == "1":
        enter_payment()
    elif task == "2":
        enter_name()
    elif task == "3":
        show_all_names()
    elif task == "4":
        show_all_payments()
    elif task == "5":
        enter_expense_type()
    elif task == "6":
        month_totals()
    else:
        print "Pick one of these!"


quit = 1
while quit != "Q":
    main()
    quit = str.upper(raw_input("Type 'Q' to quit or any key to continue. "))
else:
    print "Bye bye!"
