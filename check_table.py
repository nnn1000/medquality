import sqlite3

def check_table_structure():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute("PRAGMA table_info(indicators)")
    columns = cursor.fetchall()
    
    print("Table structure:")
    for col in columns:
        print(f"Column: {col}")
    
    conn.close()

if __name__ == "__main__":
    check_table_structure() 