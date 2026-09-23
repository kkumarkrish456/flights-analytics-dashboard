import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DB:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )
            self.cursor = self.conn.cursor()
        except Exception as Error:
            print(f"Error connecting to the database : {Error}")

    def fetch_city_names(self):
        city = []
        if self.cursor:
            try:
                self.cursor.execute("""
                SELECT "source_city" FROM airlines_flights_data 
                UNION
                SELECT "destination_city" FROM airlines_flights_data;
                """)
                cities = self.cursor.fetchall()

                for item in cities:
                    city.append(item[0])
                return city
            except Exception as error:
                print(f"Error while fetching cities : {error}")
            
    def fetch_flights(self, source=None, destination=None, airline=None,airport=None):
        if self.cursor:
            try:
                conditions = []
                params = []

                if source:
                    conditions.append('source_city = %s')
                    params.append(source)
                if destination:
                    conditions.append('destination_city = %s')
                    params.append(destination)
                if airline:
                    conditions.append('airline = %s')
                    params.append(airline)
                if airport:
                    conditions.append('airport = %s')
                    params.append(airport)

                query = 'SELECT "airline","flight","departure_time","duration","price" FROM airlines_flights_data'
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                query += ";"

                self.cursor.execute(query, tuple(params))
                flights = self.cursor.fetchall()
                print(type(flights))
                return flights
            except Exception as Error:
                print(f"Error : while fetching flights {Error}")
        
    def fetch_airlines(self):
        query = "SELECT DISTINCT airline FROM airlines_flights_data"
        df = pd.read_sql(query,self.conn)
        return df["airline"].to_list()

    def fetch_airline_frequency(self):
        if self.cursor:
            
            try:
                airline = []
                frequency = []
                self.cursor.execute("""
                        SELECT airline,COUNT(*) FROM airlines_flights_data
                        GROUP BY airline ORDER BY COUNT(*) DESC;    
                """)

                data = self.cursor.fetchall()

                for item in data:
                    airline.append(item[0])
                    frequency.append(item[1])

                return airline,frequency
            except Exception as Error:
                print(f"Error while fetching freq. count of each airline : {Error}")
            
    def fetch_airport(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT DISTINCT airport, airport_code
                    FROM airlines_flights_data
                    WHERE airport IS NOT NULL
                    AND airport_code IS NOT NULL
                    ORDER BY airport;
                """)

                data = self.cursor.fetchall()

                airports = []
                airport_codes = []

                for item in data:
                    airports.append(item[0])
                    airport_codes.append(item[1])

                return airports, airport_codes

            except Exception as Error:
                print(f"Error while fetching airports : {Error}")
    def fetch_airport_flight_frequency(self):
        if self.cursor:
            try:
                airport_code = []
                frequency = []

                self.cursor.execute("""
                    SELECT airport_code, COUNT(*)
                    FROM airlines_flights_data
                    GROUP BY airport_code
                    ORDER BY COUNT(*) DESC;
                """)

                data = self.cursor.fetchall()

                for item in data:
                    airport_code.append(item[0])
                    frequency.append(item[1])
                return airport_code, frequency
            except Exception as Error:
                print(f"Error while fetching flight frequency of airports : {Error}")

    def fetch_avg_price_by_class(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT class, AVG(price)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY class
                    ORDER BY AVG(price) DESC;
                """, (source, destination))

                data = self.cursor.fetchall()

                classes = []
                avg_price = []

                for item in data:
                    classes.append(item[0])
                    avg_price.append(item[1])

                return classes, avg_price

            except Exception as Error:
                print(f"Error while fetching average price by class : {Error}")
    def fetch_avg_price_by_airline(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airline, AVG(price)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY airline
                    ORDER BY AVG(price) DESC;
                """, (source, destination))

                data = self.cursor.fetchall()

                airlines = []
                avg_price = []

                for item in data:
                    airlines.append(item[0])
                    avg_price.append(item[1])

                return airlines, avg_price

            except Exception as Error:
                print(f"Error while fetching average price by airline : {Error}")

    def fetch_avg_price_by_route(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT source_city, destination_city, AVG(price)
                    FROM airlines_flights_data
                    GROUP BY source_city, destination_city
                    ORDER BY AVG(price) DESC;
                """)

                data = self.cursor.fetchall()

                routes = []
                avg_price = []

                for item in data:
                    routes.append(f"{item[0]} → {item[1]}")
                    avg_price.append(item[2])

                return routes, avg_price

            except Exception as Error:
                print(f"Error while fetching average price by route : {Error}")
    def fetch_dashboard_kpis(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT
                        COUNT(*) AS total_flights,
                        COUNT(DISTINCT airline) AS total_airlines,
                        COUNT(DISTINCT source_city || '-' || destination_city) AS total_routes,
                        AVG(price) AS avg_price,
                        MAX(price) AS max_price,
                        AVG(duration) AS avg_duration
                    FROM airlines_flights_data;
                """)

                return self.cursor.fetchone()

            except Exception as Error:
                print(f"Error while fetching dashboard KPIs : {Error}")
    def fetch_flights_by_source_city(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT source_city, COUNT(*)
                    FROM airlines_flights_data
                    GROUP BY source_city
                    ORDER BY COUNT(*) DESC;
                """)

                data = self.cursor.fetchall()

                cities = []
                frequency = []

                for item in data:
                    cities.append(item[0])
                    frequency.append(item[1])

                return cities, frequency

            except Exception as Error:
                print(f"Error while fetching flights by source city : {Error}")
    def fetch_departure_time_frequency(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT departure_time, COUNT(*)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY departure_time;
                """, (source, destination))

                data = self.cursor.fetchall()

                departure_time = []
                frequency = []

                for item in data:
                    departure_time.append(item[0])
                    frequency.append(item[1])

                return departure_time, frequency

            except Exception as Error:
                print(f"Error while fetching departure time frequency : {Error}")
    def fetch_avg_price_by_departure_time(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT departure_time, AVG(price)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY departure_time;
                """, (source, destination))

                data = self.cursor.fetchall()

                departure_time = []
                avg_price = []

                for item in data:
                    departure_time.append(item[0])
                    avg_price.append(item[1])

                return departure_time, avg_price

            except Exception as Error:
                print(f"Error while fetching average price by departure time : {Error}")
    def fetch_stop_frequency(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT stops, COUNT(*)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY stops
                    ORDER BY COUNT(*) DESC;
                """, (source, destination))

                data = self.cursor.fetchall()

                stops = []
                frequency = []

                for item in data:
                    stops.append(item[0])
                    frequency.append(item[1])

                return stops, frequency

            except Exception as Error:
                print(f"Error while fetching stop frequency : {Error}")
    def fetch_avg_price_by_stops(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT stops, AVG(price)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY stops
                    ORDER BY AVG(price) DESC;
                """, (source, destination))

                data = self.cursor.fetchall()

                stops = []
                avg_price = []

                for item in data:
                    stops.append(item[0])
                    avg_price.append(item[1])

                return stops, avg_price

            except Exception as Error:
                print(f"Error while fetching average price by stops : {Error}")
    def fetch_avg_duration_by_airline(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airline, AVG(duration)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY airline
                    ORDER BY AVG(duration);
                """, (source, destination))

                data = self.cursor.fetchall()

                airlines = []
                avg_duration = []

                for item in data:
                    airlines.append(item[0])
                    avg_duration.append(item[1])

                return airlines, avg_duration

            except Exception as Error:
                print(f"Error while fetching average duration by airline : {Error}")
    def fetch_class_frequency(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT class, COUNT(*)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY class
                    ORDER BY COUNT(*) DESC;
                """, (source, destination))

                data = self.cursor.fetchall()

                classes = []
                frequency = []

                for item in data:
                    classes.append(item[0])
                    frequency.append(item[1])

                return classes, frequency

            except Exception as Error:
                print(f"Error while fetching class frequency : {Error}")
    def fetch_avg_price_by_airline_all(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airline, AVG(price)
                    FROM airlines_flights_data
                    GROUP BY airline
                    ORDER BY AVG(price) DESC;
                """)

                data = self.cursor.fetchall()

                airlines = []
                avg_price = []

                for item in data:
                    airlines.append(item[0])
                    avg_price.append(item[1])

                return airlines, avg_price

            except Exception as Error:
                print(f"Error while fetching average price by airline : {Error}")
    def fetch_avg_duration_by_airline_all(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airline, AVG(duration)
                    FROM airlines_flights_data
                    GROUP BY airline
                    ORDER BY AVG(duration);
                """)

                data = self.cursor.fetchall()

                airlines = []
                avg_duration = []

                for item in data:
                    airlines.append(item[0])
                    avg_duration.append(item[1])

                return airlines, avg_duration

            except Exception as Error:
                print(f"Error while fetching average duration by airline : {Error}")
    def fetch_airline_stop_frequency(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airline, stops, COUNT(*)
                    FROM airlines_flights_data
                    GROUP BY airline, stops
                    ORDER BY airline, stops;
                """)

                return self.cursor.fetchall()

            except Exception as Error:
                print(f"Error while fetching airline stop frequency : {Error}")
    def fetch_airline_route_coverage(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT
                        airline,
                        COUNT(DISTINCT source_city || '-' || destination_city)
                    FROM airlines_flights_data
                    GROUP BY airline
                    ORDER BY COUNT(DISTINCT source_city || '-' || destination_city) DESC;
                """)

                data = self.cursor.fetchall()

                airlines = []
                routes = []

                for item in data:
                    airlines.append(item[0])
                    routes.append(item[1])

                return airlines, routes

            except Exception as Error:
                print(f"Error while fetching airline route coverage : {Error}")
    def fetch_airline_class_avg_price(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airline, class, AVG(price)
                    FROM airlines_flights_data
                    GROUP BY airline, class
                    ORDER BY airline, class;
                """)

                return self.cursor.fetchall()

            except Exception as Error:
                print(f"Error while fetching airline class average price : {Error}")
    def fetch_airport_destinations(self, airport):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT destination_city, COUNT(*)
                    FROM airlines_flights_data
                    WHERE airport = %s
                    GROUP BY destination_city
                    ORDER BY COUNT(*) DESC;
                """, (airport,))

                data = self.cursor.fetchall()

                destinations = []
                frequency = []

                for item in data:
                    destinations.append(item[0])
                    frequency.append(item[1])

                return destinations, frequency

            except Exception as Error:
                print(f"Error while fetching airport destinations : {Error}")
    def fetch_avg_price_by_airport(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airport_code, AVG(price)
                    FROM airlines_flights_data
                    GROUP BY airport_code
                    ORDER BY AVG(price) DESC;
                """)

                data = self.cursor.fetchall()

                airport_codes = []
                avg_price = []

                for item in data:
                    airport_codes.append(item[0])
                    avg_price.append(item[1])

                return airport_codes, avg_price

            except Exception as Error:
                print(f"Error while fetching average price by airport : {Error}")
    def fetch_airport_connectivity(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT
                        airport_code,
                        COUNT(DISTINCT destination_city)
                    FROM airlines_flights_data
                    GROUP BY airport_code
                    ORDER BY COUNT(DISTINCT destination_city) DESC;
                """)

                data = self.cursor.fetchall()

                airport_codes = []
                destinations = []

                for item in data:
                    airport_codes.append(item[0])
                    destinations.append(item[1])

                return airport_codes, destinations

            except Exception as Error:
                print(f"Error while fetching airport connectivity : {Error}")
    def fetch_route_prices(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT price
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s;
                """, (source, destination))

                data = self.cursor.fetchall()

                prices = []

                for item in data:
                    prices.append(item[0])

                return prices

            except Exception as Error:
                print(f"Error while fetching route prices : {Error}")     
    def fetch_avg_price_by_days_left(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT days_left, AVG(price)
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s
                    GROUP BY days_left
                    ORDER BY days_left;
                """, (source, destination))

                data = self.cursor.fetchall()

                days_left = []
                avg_price = []

                for item in data:
                    days_left.append(item[0])
                    avg_price.append(item[1])

                return days_left, avg_price

            except Exception as Error:
                print(f"Error while fetching price by days left : {Error}")
    def fetch_price_duration(self, source, destination):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT duration, price
                    FROM airlines_flights_data
                    WHERE source_city = %s
                    AND destination_city = %s;
                """, (source, destination))

                return self.cursor.fetchall()

            except Exception as Error:
                print(f"Error while fetching price duration data : {Error}")
    def fetch_avg_price_by_route(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT
                        source_city,
                        destination_city,
                        AVG(price)
                    FROM airlines_flights_data
                    GROUP BY source_city, destination_city
                    ORDER BY AVG(price) DESC;
                """)

                data = self.cursor.fetchall()

                routes = []
                avg_price = []

                for item in data:
                    routes.append(f"{item[0]} → {item[1]}")
                    avg_price.append(item[2])

                return routes, avg_price

            except Exception as Error:
                print(f"Error while fetching average price by route : {Error}")
    def fetch_airline_frequency(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airline, COUNT(*)
                    FROM airlines_flights_data
                    GROUP BY airline
                    ORDER BY COUNT(*) DESC;
                """)

                data = self.cursor.fetchall()

                airlines = []
                frequency = []

                for item in data:
                    airlines.append(item[0])
                    frequency.append(item[1])

                return airlines, frequency

            except Exception as Error:
                print(f"Error while fetching airline frequency : {Error}")
    def fetch_highest_avg_fare_airline(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT airline, AVG(price)
                    FROM airlines_flights_data
                    GROUP BY airline
                    ORDER BY AVG(price) DESC
                    LIMIT 1;
                """)
                return self.cursor.fetchone()

            except Exception as Error:
                print(f"Error while fetching highest average fare airline : {Error}")
    def fetch_busiest_source_city(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT source_city, COUNT(*)
                    FROM airlines_flights_data
                    GROUP BY source_city
                    ORDER BY COUNT(*) DESC
                    LIMIT 1;
                """)
                return self.cursor.fetchone()

            except Exception as Error:
                print(f"Error while fetching busiest source city : {Error}")
    def fetch_most_expensive_route(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT
                        source_city,
                        destination_city,
                        AVG(price)
                    FROM airlines_flights_data
                    GROUP BY source_city, destination_city
                    ORDER BY AVG(price) DESC
                    LIMIT 1;
                """)
                return self.cursor.fetchone()

            except Exception as Error:
                print(f"Error while fetching most expensive route : {Error}")
    def fetch_airline_most_routes(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT
                        airline,
                        COUNT(DISTINCT source_city || '-' || destination_city)
                    FROM airlines_flights_data
                    GROUP BY airline
                    ORDER BY COUNT(DISTINCT source_city || '-' || destination_city) DESC
                    LIMIT 1;
                """)
                return self.cursor.fetchone()

            except Exception as Error:
                print(f"Error while fetching airline route coverage : {Error}")
    def fetch_class_avg_fare(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT class, AVG(price)
                    FROM airlines_flights_data
                    GROUP BY class
                    ORDER BY AVG(price) DESC;
                """)
                return self.cursor.fetchall()

            except Exception as Error:
                print(f"Error while fetching class average fare : {Error}")
    def fetch_stops_avg_fare(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT stops, AVG(price)
                    FROM airlines_flights_data
                    GROUP BY stops
                    ORDER BY stops;
                """)
                return self.cursor.fetchall()

            except Exception as Error:
                print(f"Error while fetching stops average fare : {Error}")
    def fetch_booking_lead_fare(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT days_left, AVG(price)
                    FROM airlines_flights_data
                    GROUP BY days_left
                    ORDER BY days_left;
                """)
                return self.cursor.fetchall()

            except Exception as Error:
                print(f"Error while fetching booking lead fare : {Error}")
