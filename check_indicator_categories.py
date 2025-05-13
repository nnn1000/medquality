import sqlite3

def check_indicator_categories():
    conn = sqlite3.connect('instance/medquality.db')
    cursor = conn.cursor()
    
    # Get indicator categories
    cursor.execute("SELECT * FROM indicator_categories")
    categories = cursor.fetchall()
    
    print("Indicator Categories:")
    for category in categories:
        print(f"Category: {category}")
    
    conn.close()

if __name__ == "__main__":
    check_indicator_categories() 