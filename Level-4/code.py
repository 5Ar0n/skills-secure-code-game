import sqlite3
import os
from flask import Flask, request

class Connect(object):

    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection
    
class Create(object):
    
    def __init__(self):
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()
            
            table_fetch = cur.execute(
                '''
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'AND name='stocks';
                ''').fetchall()
 
            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')
                
                cur.execute(
                    "INSERT INTO stocks VALUES ('2022-01-06', 'MSFT', 300.00)")
                db_con.commit()
            
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
            
        finally:
            db_con.close()

class DB_CRUD_ops(object):
    

    def get_stock_info(self, stock_symbol):

        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor() 
            
            res = "[METHOD EXECUTED] get_stock_info\n"
            query = "SELECT * FROM stocks WHERE symbol = ?"
            cur.execute(query, (stock_symbol,))
            res += "[QUERY] " + query + "\n"
            
            restricted_chars = ";%&^!#-"
            has_restricted_char = any([char in query for char in restricted_chars])
            correct_number_of_single_quotes = query.count("'") == 2
            
            if has_restricted_char or not correct_number_of_single_quotes:

                res += "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
            else:
                cur.execute(query)
                
                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result)
            return res
        
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
            
        finally:
            db_con.close()
            

    def get_stock_price(self, stock_symbol):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()
            
            res = "[METHOD EXECUTED] get_stock_price\n"
            query = "SELECT price FROM stocks WHERE symbol = ?"
            cur.execute(query, (stock_symbol,))
            res += "[QUERY] " + query + "\n"
            if ';' in query:
                res += "[SCRIPT EXECUTION]\n"
                cur.executescript(query)
            else:
                cur.execute(query)
                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result) + "\n"
            return res
                
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
            
        finally:
            db_con.close()

    def update_stock_price(self, stock_symbol, price):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()
            
            if not isinstance(price, float):
                raise Exception("ERROR: stock price provided is not a float")
            
            res = "[METHOD EXECUTED] update_stock_price\n"
            query = "UPDATE stocks SET price = ? WHERE symbol = ?"
            cur.execute(query, (price, stock_symbol))
            res += "[QUERY] " + query + "\n"
            
            cur.execute(query)
            db_con.commit()
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + result
            return res
            
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
            
        finally:
            db_con.close()


    def exec_multi_query(self, query):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()
            
            res = "[METHOD EXECUTED] exec_multi_query\n"
            for query in filter(None, query.split(';')):
                res += "[QUERY]" + query + "\n"
                query = query.strip()
                cur.execute(query)
                db_con.commit()
                
                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result) + " "
            return res
            
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
            
        finally:
            db_con.close()  

 
    def exec_user_script(self, query):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()
            
            res = "[METHOD EXECUTED] exec_user_script\n"
            res += "[QUERY] " + query + "\n"
            if ';' in query:
                res += "[SCRIPT EXECUTION]"

            else:
                cur.execute(query)
                db_con.commit()
                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result)
            return res    
            
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
            
        finally:
            db_con.close()