import pandas as pd
import streamlit as st
import plotly.express as px
from dbhelper import DB

db = DB()

st.set_page_config(page_title="Flights Analytics Dashboard", page_icon="✈️", layout="wide")

st.sidebar.title("Flights Analytics Dashboard")

user_option = st.sidebar.selectbox(
    'Menu', 
        ['Project Overview',
        'Dashboard Overview', 
        'Key Insights',
        'Flights Data', 
        'Airlines Data',  
        'Airport Data',
        'Flight Routes And Price Data']
)

if user_option == 'Project Overview':
    st.title("Welcome to the Flights Analytics Dashboard!")
    st.subheader(" Use the sidebar to navigate through different sections and explore the data.")
    st.caption("An end-to-end analytics dashboard on Indian domestic flight bookings")

    st.markdown("""
    # ✈️ Flights Analytics Dashboard

    This dashboard analyzes Indian domestic flight data using **Python, PostgreSQL, Pandas, Streamlit, and Plotly**.

    The dataset contains approximately **300,000 flight records** covering major Indian cities and airlines. The dashboard allows users to explore flight operations, airline performance, airport traffic, routes, and ticket pricing patterns.

    ### 📊 Dataset Coverage

    * **6 Major Indian Cities:** Delhi, Mumbai, Bangalore, Kolkata, Hyderabad, Chennai
    * **6 Airlines:** SpiceJet, AirAsia, Vistara, GO_FIRST, Indigo, Air India
    * Approximately **300,000 flight records**
    * Flight information including:

    * Airline
    * Flight number
    * Source and destination
    * Departure and arrival information
    * Number of stops
    * Travel class
    * Flight duration
    * Days left before departure
    * Ticket price

    ### 🔎 Dashboard Analysis

    **✈️ Flights Data**

    * Flight availability by route
    * Departure-time distribution
    * Average fare by departure time
    * Flights by number of stops
    * Average fare by stops
    * Class distribution

    **🏢 Airlines Data**

    * Airline flight distribution
    * Average fare by airline
    * Average flight duration
    * Airline route coverage
    * Airline vs stops analysis
    * Airline and class fare comparison

    **🛫 Airport Data**

    * Airport traffic
    * Destinations from each airport
    * Average fare by airport
    * Airport connectivity
    * Airport code reference

    **💰 Routes & Price Data**

    * Average fare by route
    * Average fare by class
    * Average fare by airline
    * Fare distribution
    * Fare vs days left
    * Fare vs flight duration

    ### 🛠️ Technologies Used

    * Python
    * PostgreSQL
    * Pandas
    * Streamlit
    * Plotly
    * SQL

    ### 📌 Project Links

    * **GitHub:** [Add GitHub Repository Link]
    * **LinkedIn:** [Add LinkedIn Profile]
    * **Portfolio:** [Add Portfolio Link]
    * **Live Dashboard:** [Add Deployment Link]

    ### 📬 Contact

    **Krish Kumar**

    * **Email:** kkumarkrish.456@gmail.com
    * **LinkedIn:** https://www.linkedin.com/in/krish-kumar-132a55432/
    * **GitHub:** 

    ---

    *This project was created to demonstrate practical skills in SQL, data analysis, data visualization, dashboard development, and extracting insights from real-world flight data.*

    """)
elif user_option == 'Dashboard Overview':
    st.subheader("Dashboard Overview")

    total_flights, total_airlines, total_routes, avg_price, max_price, avg_duration = db.fetch_dashboard_kpis()

    col1, col2, col3 = st.columns(3)

    # Dashboard KPI's
    with col1:
        st.metric("✈️ Total Flights", f"{total_flights:,}")

    with col2:
        st.metric("🏢 Total Airlines", total_airlines)

    with col3:
        st.metric("🗺️ Total Routes", total_routes)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("💰 Average Fare", f"₹{avg_price:,.0f}")

    with col5:
        st.metric("💸 Maximum Fare", f"₹{max_price:,.0f}")

    with col6:
        st.metric("⏱️ Average Duration", f"{avg_duration:.2f} hrs")

    cities, frequency = db.fetch_flights_by_source_city()

    fig = px.bar(
        x=cities,
        y=frequency,
        labels={
            "x": "Source City",
            "y": "Number of Flights"
        },
        title="Flights by Source City"
    )

    st.plotly_chart(fig, use_container_width=True)

elif user_option == 'Key Insights':

    st.title("💡 Key Insights")

    st.write("""
    This section summarizes important findings from the flight dataset
    and answers key analytical questions using SQL-based analysis.
    """)

    # Basic insights
    highest_fare_airline = db.fetch_highest_avg_fare_airline()
    busiest_city = db.fetch_busiest_source_city()
    expensive_route = db.fetch_most_expensive_route()
    most_routes_airline = db.fetch_airline_most_routes()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Highest Average Fare")

        airline, avg_fare = highest_fare_airline

        st.metric(
            "Airline",
            airline
        )

        st.write(
            f"The highest average fare among the airlines is "
            f"₹{avg_fare:,.0f}."
        )

    with col2:

        st.subheader("Busiest Source City")

        city, flight_count = busiest_city

        st.metric(
            "City",
            city
        )

        st.write(
            f"{city} has the highest number of flights originating "
            f"from a source city with {flight_count:,} flights."
        )

    # Route insights
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Most Expensive Route")

        source, destination, avg_price = expensive_route

        st.metric(
            "Route",
            f"{source} → {destination}"
        )

        st.write(
            f"The average fare for this route is "
            f"₹{avg_price:,.0f}."
        )

    with col2:

        st.subheader("Widest Route Coverage")

        airline, route_count = most_routes_airline

        st.metric(
            "Airline",
            airline
        )

        st.write(
            f"{airline} operates across {route_count} distinct "
            f"source-destination routes in the dataset."
        )

    st.divider()

    # Class analysis
    st.subheader("Does Travel Class Affect Ticket Price?")

    class_data = db.fetch_class_avg_fare()

    df_class = pd.DataFrame(
        class_data,
        columns=[
            "class",
            "avg_price"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            df_class,
            x="class",
            y="avg_price",
            labels={
                "class": "Travel Class",
                "avg_price": "Average Fare"
            },
            title="Average Fare by Travel Class"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        highest_class = df_class.iloc[0]

    st.write(
        f"**{highest_class['class']}** has the highest average fare "
        f"at approximately **₹{highest_class['avg_price']:,.0f}**."
    )

    st.write(
        "This indicates that travel class is an important factor "
        "associated with ticket price in the dataset."
    )

    # Stops analysis
    st.subheader("Does the Number of Stops Affect Ticket Price?")

    stops_data = db.fetch_stops_avg_fare()

    df_stops = pd.DataFrame(
        stops_data,
        columns=[
            "stops",
            "avg_price"
        ]
    )

    fig = px.bar(
        df_stops,
        x="stops",
        y="avg_price",
        labels={
            "stops": "Number of Stops",
            "avg_price": "Average Fare"
        },
        title="Average Fare by Number of Stops"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    cheapest_stop = df_stops.loc[
        df_stops["avg_price"].idxmin()
    ]

    expensive_stop = df_stops.loc[
        df_stops["avg_price"].idxmax()
    ]

    st.markdown("### Answer")

    st.write(
        f"The lowest average fare is associated with **{cheapest_stop['stops']}** "
        f"at approximately **₹{cheapest_stop['avg_price']:,.0f}**, while "
        f"**{expensive_stop['stops']}** has the highest average fare at "
        f"approximately **₹{expensive_stop['avg_price']:,.0f}**."
    )

    # Booking lead analysis
    st.subheader("Does Booking Lead Time Affect Ticket Price?")

    booking_data = db.fetch_booking_lead_fare()

    df_booking = pd.DataFrame(
        booking_data,
        columns=[
            "days_left",
            "avg_price"
        ]
    )

    fig = px.line(
        df_booking,
        x="days_left",
        y="avg_price",
        markers=True,
        labels={
            "days_left": "Days Before Departure",
            "avg_price": "Average Fare"
        },
        title="Average Fare vs Days Left"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    lowest_booking = df_booking.loc[
        df_booking["avg_price"].idxmin()
    ]

    highest_booking = df_booking.loc[
        df_booking["avg_price"].idxmax()
    ]

    st.write(
        f"The average fare varies with booking lead time. "
        f"The lowest observed average fare is approximately "
        f"₹{lowest_booking['avg_price']:,.0f} when {int(lowest_booking['days_left'])} "
        f"days are left, while the highest is approximately "
        f"₹{highest_booking['avg_price']:,.0f} when "
        f"{int(highest_booking['days_left'])} days are left."
    )

    st.caption(
        "This describes the relationship observed in the dataset and does "
        "not establish that booking lead time alone causes the price change."
    )

elif user_option == "Flights Data":

    st.title("Flights Data")

    st.write(
        "Explore flights between different source and destination cities."
    )

    cities = db.fetch_city_names()

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox(
            "Source",
            sorted(cities)
        )

    with col2:
        destination = st.selectbox(
            "Destination",
            sorted(cities)
        )

    if st.button("Search Flights"):

        result = db.fetch_flights(
            source,
            destination
        )

        if result:

            df = pd.DataFrame(
                result,
                columns=[
                    "airline",
                    "flight",
                    "departure_Ttme",
                    "duration(in hrs)",
                    "price"
                ]
            )

            st.subheader(
                f"Flights from {source} → {destination}"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Departure analysis
            st.subheader("Departure Time Analysis")

            departure_time, frequency = (
                db.fetch_departure_time_frequency(
                    source,
                    destination
                )
            )

            time_order = [
                "Early_Morning",
                "Morning",
                "Afternoon",
                "Evening",
                "Night",
                "Late_Night"
            ]

            time_data = dict(
                zip(departure_time, frequency)
            )

            ordered_frequency = [
                time_data.get(time, 0)
                for time in time_order
            ]

            col1, col2 = st.columns(2)

            with col1:

                fig = px.line(
                    x=time_order,
                    y=ordered_frequency,
                    markers=True,
                    labels={
                        "x": "Departure Time",
                        "y": "Number of Flights"
                    },
                    title="Flights by Departure Time"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with col2:

                departure_time, avg_price = (
                    db.fetch_avg_price_by_departure_time(
                        source,
                        destination
                    )
                )

                time_data = dict(
                    zip(departure_time, avg_price)
                )

                ordered_price = [
                    time_data.get(time, 0)
                    for time in time_order
                ]

                fig = px.bar(
                    x=time_order,
                    y=ordered_price,
                    labels={
                        "x": "Departure Time",
                        "y": "Average Fare"
                    },
                    title="Average Fare by Departure Time"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # Stops analysis
            st.subheader("Stops Analysis")

            col1, col2 = st.columns(2)

            with col1:

                stops, frequency = db.fetch_stop_frequency(
                    source,
                    destination
                )

                fig = px.bar(
                    x=stops,
                    y=frequency,
                    labels={
                        "x": "Stops",
                        "y": "Number of Flights"
                    },
                    title="Flights by Number of Stops"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with col2:

                stops, avg_price = db.fetch_avg_price_by_stops(
                    source,
                    destination
                )

                fig = px.bar(
                    x=stops,
                    y=avg_price,
                    labels={
                        "x": "Stops",
                        "y": "Average Fare"
                    },
                    title="Average Fare by Stops"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # Class analysis
            classes, frequency = db.fetch_class_frequency(
                source,
                destination
            )

            fig = px.pie(
                names=classes,
                values=frequency,
                title="Flight Distribution by Class"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
    else:
        st.warning("No flights found for this route.")
elif user_option == "Airlines Data":

    st.title("Airlines Data")

    st.write(
        "Explore airline distribution, pricing, duration and route coverage."
    )

    airlines = db.fetch_airlines()

    # Airline distribution
    airline_names, frequency = db.fetch_airline_frequency()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            names=airline_names,
            values=frequency,
            title="Airline Flight Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        airline_names, avg_price = (
            db.fetch_avg_price_by_airline_all()
        )

        fig = px.bar(
            x=airline_names,
            y=avg_price,
            labels={
                "x": "Airline",
                "y": "Average Fare"
            },
            title="Average Fare by Airline"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Airline performance
    col1, col2 = st.columns(2)

    with col1:

        airline_names, avg_duration = (
            db.fetch_avg_duration_by_airline_all()
        )

        fig = px.bar(
            x=airline_names,
            y=avg_duration,
            labels={
                "x": "Airline",
                "y": "Average Duration"
            },
            title="Average Flight Duration by Airline"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        airline_names, routes = (
            db.fetch_airline_route_coverage()
        )

        fig = px.bar(
            x=airline_names,
            y=routes,
            labels={
                "x": "Airline",
                "y": "Number of Routes"
            },
            title="Airline Route Coverage"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Airline stops
    st.subheader("Airline vs Number of Stops")

    data = db.fetch_airline_stop_frequency()

    df_airline_stops = pd.DataFrame(
        data,
        columns=[
            "airline",
            "stops",
            "frequency"
        ]
    )

    fig = px.bar(
        df_airline_stops,
        x="airline",
        y="frequency",
        color="stops",
        barmode="stack",
        labels={
            "airline": "Airline",
            "frequency": "Number of Flights",
            "stops": "Stops"
        },
        title="Flight Stops by Airline"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Airline and class pricing
    st.subheader("Airline vs Class Average Fare")

    data = db.fetch_airline_class_avg_price()

    df_airline_class = pd.DataFrame(
        data,
        columns=[
            "airline",
            "class",
            "avg_price"
        ]
    )

    fig = px.bar(
        df_airline_class,
        x="airline",
        y="avg_price",
        color="class",
        barmode="group",
        labels={
            "airline": "Airline",
            "avg_price": "Average Fare",
            "class": "Class"
        },
        title="Average Fare by Airline and Class"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Airline selection
    st.subheader("Explore Airline Flights")

    selected_airline = st.selectbox(
        "Select an Airline",
        airlines
    )

    flights = db.fetch_flights(
        airline=selected_airline
    )

    df = pd.DataFrame(
        flights,
        columns=[
            "airline",
            "flight",
            "departure_Ttme",
            "duration(in hrs)",
            "price"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    ) 
elif user_option == "Airport_Data":

    st.title("🛫 Airport Data")

    st.write(
        "Analyze airport traffic, connectivity and fare patterns."
    )

    airport, airport_code = db.fetch_airport()

    selected_airport = st.selectbox(
        "Select Airport",
        sorted(airport)
    )

    # Airport reference
    st.markdown("""
    ### ✈️ Airport Codes

    | Airport Code | Airport |
    |---|---|
    | DEL | Indira Gandhi International Airport |
    | BOM | Chhatrapati Shivaji Maharaj International Airport |
    | BLR | Kempegowda International Airport |
    | CCU | Netaji Subhas Chandra Bose International Airport |
    | HYD | Rajiv Gandhi International Airport |
    | MAA | Chennai International Airport |
    """)


    flights = db.fetch_flights(
        airport=selected_airport
    )

    df = pd.DataFrame(
        flights,
        columns=[
            "airline",
            "flight",
            "departure_Ttme",
            "duration(in hrs)",
            "price"
        ]
    )

    st.subheader(
        f"Flights from {selected_airport}"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Airport analysis
    col1, col2 = st.columns(2)

    with col1:

        destinations, frequency = (
            db.fetch_airport_destinations(
                selected_airport
            )
        )

        fig = px.bar(
            x=destinations,
            y=frequency,
            labels={
                "x": "Destination",
                "y": "Number of Flights"
            },
            title="Flights by Destination"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        airport_codes, avg_price = (
            db.fetch_avg_price_by_airport()
        )

        fig = px.bar(
            x=airport_codes,
            y=avg_price,
            labels={
                "x": "Airport Code",
                "y": "Average Fare"
            },
            title="Average Fare by Airport"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

elif user_option == "Flight Routes And Price Data":

    st.title("Flight Routes And Price Data")

    st.write(
        "Analyze ticket prices across routes, airlines, classes and flight characteristics."
    )

    cities = db.fetch_city_names()

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox(
            "Source",
            sorted(cities)
        )

    with col2:
        destination = st.selectbox(
            "Destination",
            sorted(cities)
        )

    flights = db.fetch_flights(
        source,
        destination
    )

    df = pd.DataFrame(
        flights,
        columns=[
            "airline",
            "flight",
            "departure_Ttme",
            "duration(in hrs)",
            "price"
        ]
    )

    if df.empty:

        st.warning(
            "No flights found for this route."
        )

    else:

        # Route KPI
        avg_route_price = df["price"].mean()

        st.metric(
            f"Average Fare — {source} → {destination}",
            f"₹{avg_route_price:,.0f}"
        )

        # Class and airline
        col1, col2 = st.columns(2)

        with col1:

            classes, avg_price = (
                db.fetch_avg_price_by_class(
                    source,
                    destination
                )
            )

            fig = px.bar(
                x=classes,
                y=avg_price,
                labels={
                    "x": "Class",
                    "y": "Average Fare"
                },
                title="Average Fare by Class"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            airlines, avg_price = (
                db.fetch_avg_price_by_airline(
                    source,
                    destination
                )
            )

            fig = px.bar(
                x=airlines,
                y=avg_price,
                labels={
                    "x": "Airline",
                    "y": "Average Fare"
                },
                title="Average Fare by Airline"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # Price distribution
        st.subheader("Fare Distribution")

        prices = db.fetch_route_prices(
            source,
            destination
        )

        fig = px.histogram(
            x=prices,
            nbins=30,
            labels={
                "x": "Fare",
                "y": "Number of Flights"
            },
            title="Fare Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Days left and duration
        col1, col2 = st.columns(2)

        with col1:

            days_left, avg_price = (
                db.fetch_avg_price_by_days_left(
                    source,
                    destination
                )
            )

            fig = px.line(
                x=days_left,
                y=avg_price,
                markers=True,
                labels={
                    "x": "Days Left",
                    "y": "Average Fare"
                },
                title="Average Fare vs Days Left"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            data = db.fetch_price_duration(
                source,
                destination
            )

            df_price_duration = pd.DataFrame(
                data,
                columns=[
                    "duration",
                    "price"
                ]
            )

            fig = px.scatter(
                df_price_duration,
                x="duration",
                y="price",
                labels={
                    "duration": "Flight Duration",
                    "price": "Fare"
                },
                title="Fare vs Flight Duration"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # All routes
        st.subheader("Average Fare by Route")

        routes, avg_price = (
            db.fetch_avg_price_by_route()
        )

        fig = px.bar(
            x=avg_price,
            y=routes,
            orientation="h",
            labels={
                "x": "Average Fare",
                "y": "Route"
            },
            title="Average Fare Across Routes"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )