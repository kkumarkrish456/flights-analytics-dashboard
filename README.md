# ✈️ Flights Analytics Dashboard

An interactive **Flights Analytics Dashboard** built with **Python, PostgreSQL, SQL, Streamlit, Pandas, and Plotly**.

This project analyzes a large Indian domestic flight dataset and presents flight, airline, airport, route, pricing, and booking-related insights through an interactive web dashboard.

The project follows an end-to-end Data Analytics workflow:

**Raw Data → Data Wrangling → PostgreSQL → SQL Analysis → Python DB Layer → Streamlit Dashboard → Interactive Visualizations**

---

## 📌 Project Overview

Airfare data contains several factors that can be explored to understand how flight prices and operations vary across airlines, routes, travel classes, stops, booking lead time, and airports.

The goal of this project is to build a practical analytics dashboard that converts raw flight data into useful, interactive insights using SQL and Python.

The dashboard allows users to explore the underlying flight data as well as analytical summaries generated directly from PostgreSQL.

---

## 📊 Dataset

The project uses the **Flight Price Prediction** dataset containing approximately **300,000 flight records** from the Indian domestic aviation market.

### Dataset Coverage

- **Cities:** Delhi, Mumbai, Bangalore, Kolkata, Hyderabad, Chennai
- **Airlines:** SpiceJet, AirAsia, Vistara, GO_FIRST, Indigo, Air India
- **Flight information:** Flight number, source, destination, departure time, arrival time
- **Pricing:** Ticket price
- **Travel details:** Class, stops, duration
- **Booking information:** Days left before departure
- **Airport information:** Airport name and airport code derived from source city

The dataset is used for analytical purposes and is not intended to represent real-time airline pricing.

---

## 🎯 Business Questions

The dashboard explores questions such as:

### Flight & Airport Analysis
- How many flights operate from each source city?
- Which airports serve the different source cities?
- How are destinations distributed across airports?
- Which airports have broader connectivity?

### Airline Analysis
- How frequently does each airline appear in the dataset?
- How does average fare vary across airlines?
- How does average flight duration vary across airlines?
- How do airlines differ in route coverage?
- How are airline prices distributed across travel classes?

### Route & Pricing Analysis
- Which routes have higher average fares?
- How does fare vary between different routes?
- How does average price vary with flight duration?
- How does fare vary according to the number of stops?
- How does booking lead time relate to average fare?

### Travel Class Analysis
- How is average fare distributed across travel classes?
- How does the distribution of classes vary across flights?

---

## 📈 Dashboard Sections

### 1. Project Overview

Provides an introduction to the project, dataset, technologies used, and project information.

### 2. Dashboard Overview

Provides high-level KPIs and an overview of flight distribution across source cities.

### 3. Key Insights

Contains analytical queries designed to answer important business questions, including:

- Highest average fare airline
- Busiest source city
- Most expensive route by average fare
- Airline with the largest route coverage
- Average fare by travel class
- Average fare by number of stops
- Average fare by booking lead time

### 4. Flights Data

Allows users to explore flight-level data using filters such as:

- Source city
- Destination city
- Airline
- Airport

### 5. Airlines Data

Provides airline-level analysis including frequency, average pricing, duration, route coverage, stops, and class-related pricing.

### 6. Airport Data

Provides airport-level information and connectivity analysis.

### 7. Flight Routes & Price Data

Provides route-specific analysis covering:

- Route prices
- Average price by route
- Price vs. duration
- Price vs. booking lead time
- Route-level flight information

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Data processing and application logic |
| **Pandas** | Data handling and analysis |
| **PostgreSQL** | Database storage and SQL analysis |
| **Psycopg2** | PostgreSQL connection from Python |
| **SQL** | Data retrieval and analytical queries |
| **Streamlit** | Interactive dashboard |
| **Plotly** | Interactive charts and visualizations |
| **python-dotenv** | Secure local environment-variable management |
| **Supabase** | Hosted PostgreSQL database |

---

## 🗄️ Database & SQL

The flight data is stored in a PostgreSQL database hosted on **Supabase**.

The Python application communicates with PostgreSQL through a dedicated `DB` class in `dbhelper.py`.

Analytical operations are performed using SQL queries such as:

- `GROUP BY`
- `ORDER BY`
- `COUNT`
- `AVG`
- `COUNT(DISTINCT ...)`
- `CASE`
- filtering and aggregation
- route-level analysis

This keeps the analytical workload close to the database while Streamlit is responsible for presenting the results.

---

## 🔄 Data Wrangling

The `data_wrangling.py` script handles database-side preparation of airport information.

It maintains a mapping between source cities and their corresponding airports and IATA codes:

| Source City | Airport | Code |
|---|---|---|
| Delhi | Indira Gandhi International Airport | DEL |
| Mumbai | Chhatrapati Shivaji Maharaj International Airport | BOM |
| Bangalore | Kempegowda International Airport | BLR |
| Kolkata | Netaji Subhas Chandra Bose International Airport | CCU |
| Hyderabad | Rajiv Gandhi International Airport | HYD |
| Chennai | Chennai International Airport | MAA |

The script uses `ADD COLUMN IF NOT EXISTS`, allowing it to be run without failing when the columns are already present.

---

## 📁 Project Structure

```text
Flights-Analytics-Dashboard/
│
├── app.py
├── dbhelper.py
├── data_wrangling.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml        # Local/deployment secrets - NOT committed
```

### `app.py`

Main Streamlit application containing the dashboard interface, filters, layouts, and visualizations.

### `dbhelper.py`

Contains the PostgreSQL connection and database helper methods used by the dashboard.

### `data_wrangling.py`

Handles database-side data preparation and airport mapping.

### `requirements.txt`

Contains the Python dependencies required to run the application.

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/flights-analytics-dashboard.git
cd flights-analytics-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure database credentials

Create a `.env` file in the project root:

```env
DB_HOST=your_supabase_host
DB_NAME=postgres
DB_USER=your_supabase_user
DB_PASSWORD=your_supabase_password
DB_PORT=5432
```

Do **not** commit `.env` to GitHub.

The repository's `.gitignore` should contain:

```gitignore
.env
```

### 5. Run the data-wrangling script

```bash
python data_wrangling.py
```

This prepares the airport-related columns in the PostgreSQL table.

### 6. Run the Streamlit dashboard

```bash
streamlit run app.py
```

The dashboard will then open in your browser.

---

## 🔐 Security

Database credentials are intentionally kept outside the source code.

For local development:

```text
.env
```

is used for database credentials.

For deployment on Streamlit Community Cloud, the database credentials should be stored using **Streamlit Secrets** rather than committing them to the repository.

**Never commit passwords, API keys, database URLs, or other credentials to GitHub.**

---

## ☁️ Deployment

The intended deployment architecture is:

```text
GitHub
   ↓
Streamlit Community Cloud
   ↓
Supabase PostgreSQL
   ↓
airlines_flights_data
```

The application source code is hosted on GitHub, Streamlit handles the dashboard deployment, and Supabase hosts the PostgreSQL database.

---

## 🚀 Future Improvements

Possible future additions include:

- More advanced SQL analysis
- Additional route-level KPIs
- Better data-quality checks
- Interactive date/time analysis
- More advanced dashboard filtering
- Additional business-oriented insights
- Dashboard performance optimization
- Automated data refresh
- Deployment improvements
- More detailed documentation and screenshots

---

## 📷 Dashboard Preview

Screenshots of the dashboard can be added here after deployment.

Example:

```text
[Dashboard Screenshot]
```

---

## 📌 Key Learning Outcomes

This project demonstrates an end-to-end Data Analytics workflow involving:

- Data wrangling
- Relational database design
- PostgreSQL
- SQL aggregation and analysis
- Python database connectivity
- Pandas
- Interactive data visualization
- Streamlit dashboard development
- Business-question-driven analysis
- Environment-variable based credential management
- Cloud database integration

---

## 👨‍💻 Author

**Krish Kumar**

Data Analytics / AI & ML Student

### Connect

- **GitHub:** https://github.com/YOUR_USERNAME
- **LinkedIn:** Add your LinkedIn profile here
- **Portfolio:** Add your portfolio here

---

## ⭐ Project

If you find this project useful or interesting, consider giving the repository a star.

**Built with Python, SQL, PostgreSQL, Streamlit & Plotly.**
