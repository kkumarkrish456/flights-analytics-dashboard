from dbhelper import DB

db = DB()

city_airport_map = {
        'Delhi':     ('Indira Gandhi International Airport', 'DEL'),
        'Mumbai':    ('Chhatrapati Shivaji Maharaj International Airport', 'BOM'),
        'Bangalore': ('Kempegowda International Airport', 'BLR'),
        'Kolkata':   ('Netaji Subhas Chandra Bose International Airport', 'CCU'),
        'Hyderabad': ('Rajiv Gandhi International Airport', 'HYD'),
        'Chennai':   ('Chennai International Airport', 'MAA')
    }

# Adding col airport,airport_code

db.cursor.execute("""
    ALTER TABLE airlines_flights_data
    ADD COLUMN IF NOT EXISTS airport VARCHAR(100),
    ADD COLUMN IF NOT EXISTS airport_code VARCHAR(10);
""")

airport_case = " ".join("WHEN source_city = %s THEN %s" for _ in city_airport_map)
code_case = " ".join("WHEN source_city = %s THEN %s" for _ in city_airport_map)

airport_values = [v for city, (name, code) in city_airport_map.items() for v in (city, name)]
code_values = [v for city, (name, code) in city_airport_map.items() for v in (city, code)]

update_query = f"""
    UPDATE airlines_flights_data
    SET airport = CASE {airport_case} ELSE NULL END,
    airport_code = CASE {code_case} ELSE NULL END;
    """
db.cursor.execute(update_query, airport_values + code_values)
db.conn.commit()