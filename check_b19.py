import sqlite3

def check_b19():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # Query all indicators for debugging
    cursor.execute('SELECT code, name, frequency, target_value, definition FROM indicators ORDER BY code')
    results = cursor.fetchall()
    
    print("All indicators in database:")
    for result in results:
        code, name, frequency, target_value, definition = result
        print(f"\nCode: {code}")
        print(f"Name: {name}")
        print(f"Frequency: {frequency}")
        print(f"Target Value: {target_value}")
        print(f"Definition: {definition}")
    
    conn.close()

if __name__ == "__main__":
    check_b19()

 