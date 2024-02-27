import sqlite3 as sql

con = sql.connect('data/games-stats.db', check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS queue ( id_game INTEGER PRIMARY KEY AUTOINCREMENT, port INT, "
            "player1 TEXT, player2 TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS pingpong (id_account INT, loses INT, wins INT)")
cur.execute("CREATE TABLE IF NOT EXISTS clicker (id_account INT, click INT, increment INT)")
cur.execute("CREATE TABLE IF NOT EXISTS dinosaur (id_account INT, click INT, increment INT)")
con.commit()
cur.close()


def update_queue(player_id, port, player_num):
    cur = con.cursor()
    if player_num == 1:
        cur.execute("UPDATE queue SET player1 = ? WHERE port = ?", (player_id, port))
    else:
        cur.execute("UPDATE queue SET player2 = ? WHERE port = ?", (player_id, port))
    con.commit()
    cur.close()


def add_queue(port):
    cur = con.cursor()
    cur.execute('INSERT INTO queue (port, player1, player2) VALUES (?, ?, ?)', (port, "", "",))
    con.commit()
    cur.close()
    #


def get_queue():
    cur = con.cursor()
    cur.execute("SELECT * FROM queue WHERE player1 = ? OR player2 = ?", ("", ""))
    result = cur.fetchone()
    con.commit()
    cur.close()

    return result
    # cur.execute('INSERT INTO accounts (login, password, token) VALUES (?, ?, ?)', (login, password, token,))

def add_stat_pingpong(id, pos): #1 - победил # 2 - луз
    cur = con.cursor()
    pl = cur.execute("SELECT * FROM stats_pingpong WHERE id_account = ?", (id, )).fetchone()
    if pos == 1:
        if not pl:
            cur.execute('INSERT INTO stats_pingpong (id_account, loses, wins) VALUES (?, ?, ?)', (id, 0, 1,))
        else:
            cur.execute("UPDATE stats_pingpong SET wins = ? WHERE id_account = ?", (pl[2] + 1, id))
    else:
        if not pl:
            cur.execute('INSERT INTO stats_pingpong (id_account, loses, wins) VALUES (?, ?, ?)', (id, 1, 0,))
        else:
            cur.execute("UPDATE stats_pingpong SET loses = ? WHERE id_account = ?", (pl[1] + 1, id))
    con.commit()
    cur.close()

def add_stat_clicker(id, click, increment):
    cur = con.cursor()
    pl = cur.execute("SELECT * FROM clicker WHERE id_account = ?", (id,)).fetchone()
    if not pl:
        cur.execute('INSERT INTO clicker (id_account, click, increment) VALUES (?, ?, ?)', (id,click, increment,))
    else:
        cur.execute("UPDATE clicker SET click = ? SET increment =? WHERE id_account = ?", (click, increment, id))
    con.commit()
    cur.close()