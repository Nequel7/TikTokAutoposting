import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()

    def add_category(self, category):
        with self.connection:
            self.cur.execute("INSERT INTO categories (category) VALUES (?)", (category,))

    def category_exists(self, category):
        with self.connection:
            self.cur.execute('SELECT * FROM categories WHERE category = ?', (category,))
            return bool(len(self.cur.fetchall()))

    def del_category(self, category):
        with self.connection:
            self.cur.execute("DELETE FROM categories WHERE category = ?", (category,))

    def get_accounts(self):
        res = {}
        with self.connection:
            ctgrs = self.cur.execute("SELECT category FROM categories").fetchall()
            # print(ctgrs)
            for i in ctgrs:
                # print(i)
                res[i[0]] = [a for a in
                             self.cur.execute("SELECT account FROM accounts WHERE category = ?", (i[0],))]

        return res

    def add_account_in_category(self, account, category):
        with self.connection:
            if bool(len(self.cur.execute("SELECT * FROM accounts WHERE account = ?", (account,)).fetchall())):
                self.cur.execute("UPDATE accounts SET category = ? WHERE account = ?", (category, account))
            else:
                self.cur.execute("INSERT INTO accounts (account,category) VALUES (?,?)", (account, category))

    def del_account(self, account):
        with self.connection:
            self.cur.execute("DELETE FROM accounts WHERE account = ?", (account,))

    def get_accounts_in_category(self, category):
        with self.connection:
            self.cur.execute("SELECT account FROM accounts WHERE category = ?", (category,))
        return [f'{i[0]}_cookies' for i in self.cur.fetchall()]
