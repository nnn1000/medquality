import sqlite3

def remove_b19i_children():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # Delete all B19I child indicators
    cursor.execute('DELETE FROM indicators WHERE code LIKE "B19I.%"')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("B19I child indicators have been removed.")

if __name__ == "__main__":
    remove_b19i_children() 