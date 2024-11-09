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
