def create_tables(cur,db_type):
    if db_type == 'sqlite3':
        cur.execute('''CREATE TABLE IF NOT EXISTS person (
            id integer PRIMARY KEY,
            name varchar(10));''')

        cur.execute('''CREATE TABLE IF NOT EXISTS expensetypes (
            id integer PRIMARY KEY,
            expensetype varchar(50));''')

        cur.execute('''CREATE TABLE IF NOT EXISTS payments (
            id integer PRIMARY KEY,
            payer_id int REFERENCES person(id),
            expensetype_id int REFERENCES expensetypes(id),
            name varchar(50),
            amount double precision,
            paydate date,
            note varchar(100)
        );''')
    if db_type == 'postgres':
        cur.execute('''CREATE TABLE IF NOT EXISTS person (
            id integer PRIMARY KEY,
            name varchar(10));''')

        cur.execute('''CREATE TABLE IF NOT EXISTS expensetypes (
            id serial PRIMARY KEY,
            expensetype varchar(50));''')

        cur.execute('''CREATE TABLE IF NOT EXISTS payments (
            id serial PRIMARY KEY,
            payer_id int REFERENCES person(id),
            expensetype_id int REFERENCES expensetypes(id),
            name varchar(50),
            amount double precision,
            paydate date);''')
