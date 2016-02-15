# script to interact with expenses db
# create a file called "spendingconfig.py" to include "mydb = PATH TO YOUR LOCAL DATABASE"--add this file to .gitignore
# run lines "cur.execute("CREATE TABLE...")" only the first time you run this script--comment them out afterwards

import psycopg2
from psycopg2 import extras
from spendingconfig import mydb

try:
	conn = psycopg2.connect(mydb)
	# print "Connected to sharedexpenses!"
except:
	print "Not connecting to sharedexpenses db"

conn.set_session(autocommit=True)
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# cur.execute("CREATE TABLE person (id serial PRIMARY KEY, name varchar(10));")
# cur.execute("CREATE TABLE expensetypes (id serial PRIMARY KEY, expensetype varchar(50));")
# cur.execute("CREATE TABLE payments (id serial PRIMARY KEY, payer_id int REFERENCES person(id), expensetype_id int REFERENCES expensetypes(id), name varchar(50), amount numeric(4,2), paydate date);")


def enter_name():
	name = str.capitalize(raw_input("What name do you want to enter? "))
	try:
		dict_cur.execute("INSERT INTO person(name) VALUES (%s)", (name,))
	except:
		print "I can't enter that name!"

def show_all_names():
	try:
		dict_cur.execute("SELECT personname FROM person ORDER BY personname")
		ournames = dict_cur.fetchall()
		print "These are all the names:"
		for name in ournames:
			print name[0]
	except:
		print "Can't retrieve names!"

def show_all_payments():
	try:
		dict_cur.execute("SELECT * FROM payments INNER JOIN person ON person.id = payments.payer_id ORDER BY person.personname, payments.paydate DESC")
		allpayments = dict_cur.fetchall()
		print "These are all the payments:"
		for payment in allpayments:
			print "%s paid %s $%s on %s for %s" % (payment['personname'], payment['paymentname'], payment['amount'], payment['paydate'], payment['paymentnote'])
	except:
		print "Can't retrieve payments!"

def enter_payment():
	user = str.capitalize(raw_input("Who paid? "))
	dict_cur.execute("SELECT * FROM person WHERE personname = %s", (user,))
	user_record = dict_cur.fetchone()
	user_id = int(user_record['id'])
	# print type(user_id)

	paymentname = raw_input("Who did %s pay? " % user)
	paymentamount = float(input("Amount: "))
	paymentdate = raw_input("Date of payment: ")

	print "Expense types: "
	existingexpensetypes = dict_cur.execute("SELECT expensetype FROM expensetypes ORDER BY expensetype")
	expensetypelist = dict_cur.fetchall()
	for item in expensetypelist:
		print item[0]
	expensetype = raw_input("Pick an expense type: ")
	dict_cur.execute("SELECT * FROM expensetypes WHERE expensetype = %s", (expensetype,))
	expensetype_record = dict_cur.fetchone()
	expensetype_id = int(expensetype_record['id'])
	# print type(expensetype_id)

	paymentnote = raw_input("Describe what the payment is for: ")

	print "%s paid %s $%.2f on %s for %s: %s" % (user, paymentname, paymentamount, 
		paymentdate, expensetype, paymentnote)
	correct = raw_input("Is this correct (y/n): ")
	if correct == "y":
		try:
			dict_cur.execute("INSERT INTO payments(paymentname, amount, paydate, payer_id, expensetype_id, paymentnote) VALUES (%s, %s, %s, %s, %s, %s)", (paymentname, paymentamount, paymentdate, user_id, expensetype_id, paymentnote))
			print "Added your payment to the db!"
		except:
			print "I can't enter your payment in the db!"
	else:
		print "start over!"

def enter_expense_type():
	print "These are the current expense types: "
	existingepensetypes = dict_cur.execute("SELECT expensetype FROM expensetypes ORDER BY expensetype")
	expensetypelist = dict_cur.fetchall()
	for i in expensetypelist:
		print i[0]

	expense_type = raw_input("What kind of expense type do you want to add to the db? (type 'q' to go back): ")
	if expense_type == "":
		print "Try again."
		enter_expense_type()
	elif expense_type == "q":
		main()
	else:
		try:
			dict_cur.execute("INSERT INTO expensetypes(expensetype) VALUES (%s)", (expense_type,))
			print "Added %s to expensetypes db!" % (expense_type)
		except:
			print "I can't add that expense type to the db!"
		
def see_totals():
	user = str.capitalize(raw_input("Who do you want to see totals for? "))
	dict_cur.execute("SELECT * FROM person WHERE personname = %s", (user,))
	user_record = dict_cur.fetchone()
	user_id = int(user_record['id'])

	try:
		paymentsbyuser = dict_cur.execute("SELECT SUM(payments.amount) FROM payments INNER JOIN person ON payments.payer_id = person.id WHERE person.id = %s", (user_id,))
		userpayment = dict_cur.fetchone()
		print "%s has paid $%s" % (user, userpayment[0])
	except:
		print "Can't calculate totals for %s!" % (user)


def main():
	task = raw_input("What do you want to do? Pick a number. \n(1) enter payment \n(2) enter name \n(3) see names \n(4) see payments \n(5) enter expense types \n(6) see total payments for user \n: ")

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
		see_totals()
	else:
		print "Pick one of these!"

quit=1
while quit != "Q":
	main()
	quit = str.upper(raw_input("Type 'Q' to quit or any key to continue. "))
else:
	print "Bye bye!"


