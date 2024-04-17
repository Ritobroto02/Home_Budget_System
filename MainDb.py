import sqlite3
import pandas as pd

class Database:
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS expenseRecord(itemName TEXT, itemPrice REAL, purchaseDate DATE)")
        self.conn.commit()

    def fetchRecord(self, query, params=None):
        if params:
            self.cur.execute(query, params)
        else:
            self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insertRecord(self, itemName, itemPrice, purchaseDate):
        try:
            self.cur.execute("INSERT INTO expenseRecord VALUES(?, ?, ?)",
                             (itemName, itemPrice, purchaseDate))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error inserting record:", e)

    def removeRecord(self, rwid):
        try:
            self.cur.execute("DELETE FROM expenseRecord WHERE rowid=?", (rwid,))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error deleting record:", e)

    def updateRecord(self, itemName, itemPrice, purchaseDate, rid):
        try:
            self.cur.execute("UPDATE expenseRecord SET itemName = ?, itemPrice = ?, purchaseDate = ? WHERE rowid = ?",
                             (itemName, itemPrice, purchaseDate, rid))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error updating record:", e)

    def save_to_csv(self, filename):  # Changed method name to save_to_csv
        # Fetch all records from the database
        records = self.fetchRecord("SELECT * FROM expenseRecord")
        
        # Create a DataFrame from the fetched records
        df = pd.DataFrame(records, columns=["itemName", "itemPrice", "purchaseDate"])
        
        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False)

    def __del__(self):
        self.conn.close()
