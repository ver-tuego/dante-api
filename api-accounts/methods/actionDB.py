import sqlite3 as sql
import secrets

con = sql.connect('data/users.db', check_same_thread=False)

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS accounts ( id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT, password TEXT, "
            "token TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS games ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price INT)")
cur.execute("CREATE TABLE IF NOT EXISTS accounts_games (id_account INT, id_game INT)")
cur.execute("CREATE TABLE IF NOT EXISTS finance (id_account INT, balance INT, cards TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS photos (id_account INT, photo TEXT)")

con.commit()
cur.close()


def create_user(login, password):
    token = secrets.token_hex(16)

    cur = con.cursor()
    cur.execute("SELECT seq FROM sqlite_sequence WHERE name = ?", ("accounts",))

    n = cur.fetchall()
    if not n:
        n = 1
    else:
        n = n[0][0] + 1

    cur.execute('INSERT INTO finance (id_account, balance, cards) VALUES (?, ?, ?)', (n, 0, "",))
    cur.execute('INSERT INTO photos (id_account, photo) VALUES (?, ?)', (n, "",))
    cur.execute('INSERT INTO accounts (login, password, token) VALUES (?, ?, ?)', (login, password, token,))

    con.commit()
    cur.close()
    return [n, token]


def get_account(login='', id='', token='', password='', get_user=False):
    cur = con.cursor()
    if get_user:
        cur.execute('SELECT * FROM accounts WHERE login = ? AND password = ?', (login, password,))
    else:
        cur.execute('SELECT * FROM accounts WHERE (login = ?) or (id = ?) or (token = ?)', (login, id, token,))
    result = cur.fetchone()
    con.commit()
    cur.close()

    return result

def get_finances(account_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM finance WHERE id_account = ?", (account_id, ))
    result = cur.fetchone()
    con.commit()
    cur.close()

    return result

def get_games(account_id):
    cur = con.cursor()
    cur.execute('SELECT * FROM account_games WHERE id_account = ?', (account_id))


def save_photo(account_id, file_name):
    cur = con.cursor()
    cur.execute("UPDATE photos SET photo = ? WHERE id_account = ?", (file_name, account_id,))
    con.commit()
    cur.close()


def get_photos():
    cur = con.cursor()
    cur.execute("SELECT * FROM photos")
    result = cur.fetchall()

    con.commit()
    cur.close()
    return result
