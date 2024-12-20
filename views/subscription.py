import sqlite3
import json
from models import Subscription

def get_all_subscriptions():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
            
        FROM Subscriptions s
        """)

        Subscriptions = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            Subscriptions.append(subscription.__dict__) # see the notes below for an explanation on this line of code.

    return Subscriptions

def get_single_subscription(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
            
        FROM Subscriptions s
  
        WHERE s.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        subscription = Subscription(data['id'], data['follower_id'], data['author_id'],
                            data['created_on'])

        return subscription.__dict__

def create_subscription(new_subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
            
        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( id, follower_id, author_id, created_on )
        VALUES
            ( ?, ?, ?, ? )
        """, (new_subscription['id'], new_subscription['follower_id'],
              new_subscription['author_id'], new_subscription['created_on'],  ))
            
        id = db_cursor.lastrowid
            
        new_subscription['id'] = id
        
    return new_subscription

def update_subscription(id, new_subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Subscriptions
            SET
                id = ?,
                follower_id = ?,
                author_id = ?,
                created_on = ?
                
        WHERE id = ?
        """, (new_subscription['id'], new_subscription['follower_id'],
              new_subscription['author_id'], new_subscription['created_on'],  id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True

    
def delete_subscription(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Subscriptions
        WHERE id = ?
        """, (id, ))

