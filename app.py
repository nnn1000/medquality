def get_indicators():
    conn = get_db_connection()
    indicators = conn.execute('SELECT * FROM indicators WHERE parent_code IS NULL').fetchall()
    # Filter out any child indicators for B19I
    indicators = [ind for ind in indicators if not ind['code'].startswith('B19I.')]
    conn.close()
    return indicators 