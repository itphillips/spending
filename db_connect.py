import sqlite3


# retuns a dictionary with the curson and the connection
def db_connect(db_type, db_path):
    out = {}
    if db_type == "sqlite3":

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        conn = sqlite3.connect(db_path, isolation_level=None)
        out['norm_conn'] = conn
        out['norm_cur'] = conn.cursor()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        out['conn'] = conn
        out['cur'] = cur
        return out
    elif db_type == 'postgres':
        import psycopg2
        from psycopg2 import extras        
        conn = psycopg2.connect(db_path)
        conn.set_session(autocommit=True)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        out['conn'] = conn
        out['cur'] = cur
        return out
    else:
        return False

        # cur.execute("select title from book")
        # for key in cur:
        #     print(key)
