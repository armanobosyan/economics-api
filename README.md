
# Economic Data API Microservice (ED-API)

A production-ready **REST API** that delivers structured **macroeconomic data per country**, covering hundreds of real-time and historical indicators such as GDP, inflation, unemployment, interest rates, housing, trade, and more. All data is from public sources like Trading Economics and exposed through clean, **filterable JSON APIs**.

---

## Features

**Granular Economic Data** – 500+ economic indicators per country
**Topic & Filter Support** – Easily access sub-categories via `?Related=...`
**Structured API** – Clean, consistent endpoint architecture
**Live Economic Calendar** via TradingView
**OpenAPI-compatible schema** for documentation integration
**Real-time Data** No database required
**Zero API keys**, zero auth – public data, stateless design

---

## Example Endpoints

```http
GET /v1/economics/countries-overview
GET /v1/economics/United States/overview?Related=Inflation Rate
GET /v1/economics/Germany/GDP?Related=GDP Annual Growth Rate
GET /v1/economics/Japan/labour?Related=Unemployment Rate
GET /v1/economics/China/prices?Related=Consumer Price Index CPI
GET /v1/economics/France/government?Related=Government Debt to GDP
GET /v1/economics/Brazil/housing?Related=Housing Starts
GET /v1/economic-calendar
GET /v1/economics/schema
```

All endpoints return data in JSON format and support dynamic `Related=` filtering.

---

## Categories Covered

- `overview`
- `GDP`
- `labour`
- `prices`
- `health`
- `money`
- `trade`
- `government`
- `business`
- `consumer`
- `housing`

Each supports `?Related=...` filters to query specific metrics like:

- GDP Growth Rate
- Unemployment Rate
- Inflation Rate
- Consumer Confidence
- Trade Balance
- Retail Sales
- PCE Index
- Mortgage Rate
- ...and many more.

---

## Azure-Ready Deployment

This API is fully optimized for deployment on:

- **Azure App Service (Linux)**
- Using **Gunicorn** as the production WSGI server

### CI/CD Compatibility

- Supports **GitHub Actions**, **Azure DevOps**, or manual deployment
- Minimal footprint and fast cold-start (no DB, no queueing)

---

## Tech Stack

| Component        | Description                   |
|------------------|-------------------------------|
| Python 3.12      | Runtime                       |
| Flask            | Web framework                 |
| Gunicorn         | Production WSGI server        |
| BeautifulSoup    | HTML parser                   |
| Requests         | HTTP client for scraping      |
| Flask-Caching    | Optional server-side caching  |

---

## All Endpoints
All endpoints return data in JSON format and support dynamic `Related=` filtering.
---
```http

**Countries Overview**
/v1/economics/countries-overview
/v1/economics/countries-overview?Country=China
/v1/economics/<country>/overview
/v1/economics/<country>/overview?Related=Currency
/v1/economics/<country>/overview?Related=Stock Market
/v1/economics/<country>/overview?Related=GDP Growth Rate
/v1/economics/<country>/overview?Related=GDP Annual Growth Rate
/v1/economics/<country>/overview?Related=Unemployment Rate
/v1/economics/<country>/overview?Related=Non Farm Payrolls
/v1/economics/<country>/overview?Related=Inflation Rate
/v1/economics/<country>/overview?Related=Inflation Rate MoM
/v1/economics/<country>/overview?Related=Interest Rate
/v1/economics/<country>/overview?Related=Balance of Trade
/v1/economics/<country>/overview?Related=Current Account to GDP
/v1/economics/<country>/overview?Related=Government Debt to GDP
/v1/economics/<country>/overview?Related=Government Budget
/v1/economics/<country>/overview?Related=Business Confidence
/v1/economics/<country>/overview?Related=Manufacturing PMI
/v1/economics/<country>/overview?Related=Services PMI
/v1/economics/<country>/overview?Related=Consumer Confidence
/v1/economics/<country>/overview?Related=Retail Sales MoM
/v1/economics/<country>/overview?Related=Building Permits
/v1/economics/<country>/overview?Related=Personal Income Tax Rate

/v1/
/v1/economics/<country>/GDP
/v1/economics/<country>/GDP?Related=GDP Growth Rate
/v1/economics/<country>/GDP?Related=GDP Annual Growth Rate
/v1/economics/<country>/GDP?Related=GDP
/v1/economics/<country>/GDP?Related=Gross National Product
/v1/economics/<country>/GDP?Related=Gross Fixed Capital Formation
/v1/economics/<country>/GDP?Related=GDP per Capita
/v1/economics/<country>/GDP?Related=GDP per Capita PPP
/v1/economics/<country>/GDP?Related=Full Year GDP Growth
/v1/economics/<country>/GDP?Related=GDP Sales QoQ
/v1/economics/<country>/GDP?Related=Real Consumer Spending
/v1/economics/<country>/GDP?Related=Weekly Economic Index
/v1/economics/<country>/GDP?Related=GDP from Agriculture
/v1/economics/<country>/GDP?Related=GDP from Construction
/v1/economics/<country>/GDP?Related=GDP from Manufacturing
/v1/economics/<country>/GDP?Related=GDP from Mining
/v1/economics/<country>/GDP?Related=GDP from Public Administration
/v1/economics/<country>/GDP?Related=GDP from Services
/v1/economics/<country>/GDP?Related=GDP from Transport
/v1/economics/<country>/GDP?Related=GDP from Utilities

/v1/
/v1/economics/<country>/labour
/v1/economics/<country>/labour?Related=Unemployment Rate
/v1/economics/<country>/labour?Related=Non Farm Payrolls
/v1/economics/<country>/labour?Related=Government Payrolls
/v1/economics/<country>/labour?Related=Nonfarm Payrolls Private
/v1/economics/<country>/labour?Related=Manufacturing Payrolls
/v1/economics/<country>/labour?Related=Initial Jobless Claims
/v1/economics/<country>/labour?Related=Continuing Jobless Claims
/v1/economics/<country>/labour?Related=ADP Employment Change
/v1/economics/<country>/labour?Related=Employed Persons
/v1/economics/<country>/labour?Related=Average Hourly Earnings
/v1/economics/<country>/labour?Related=Average Weekly Hours
/v1/economics/<country>/labour?Related=Labor Force Participation Rate
/v1/economics/<country>/labour?Related=Long Term Unemployment Rate
/v1/economics/<country>/labour?Related=Youth Unemployment Rate
/v1/economics/<country>/labour?Related=Labour Costs
/v1/economics/<country>/labour?Related=Productivity
/v1/economics/<country>/labour?Related=Job Vacancies
/v1/economics/<country>/labour?Related=Challenger Job Cuts
/v1/economics/<country>/labour?Related=Wages
/v1/economics/<country>/labour?Related=Minimum Wages
/v1/economics/<country>/labour?Related=Wage Growth
/v1/economics/<country>/labour?Related=Wages in Manufacturing
/v1/economics/<country>/labour?Related=Employment Cost Index
/v1/economics/<country>/labour?Related=Population
/v1/economics/<country>/labour?Related=Retirement Age Women
/v1/economics/<country>/labour?Related=Retirement Age Men
/v1/economics/<country>/labour?Related=Average Hourly Earnings YoY
/v1/economics/<country>/labour?Related=Employment Cost Index Benefits
/v1/economics/<country>/labour?Related=Employment Cost Index Wages
/v1/economics/<country>/labour?Related=Hiring Plans Announcements
/v1/economics/<country>/labour?Related=Job Layoffs and Discharges
/v1/economics/<country>/labour?Related=Job Quits
/v1/economics/<country>/labour?Related=Job Quits Rate
/v1/economics/<country>/labour?Related=Nonfarm Productivity QoQ
/v1/economics/<country>/labour?Related=U6 Unemployment Rate
/v1/economics/<country>/labour?Related=Unit Labour Costs QoQ
/v1/economics/<country>/labour?Related=Employment Rate
/v1/economics/<country>/labour?Related=Full Time Employment
/v1/economics/<country>/labour?Related=Jobless Claims 4-week Average
/v1/economics/<country>/labour?Related=Part Time Employment

**Prices**
/v1/economics/<country>/prices
/v1/economics/<country>/prices?Related=Inflation Rate
/v1/economics/<country>/prices?Related=Inflation Rate MoM
/v1/economics/<country>/prices?Related=Consumer Price Index CPI
/v1/economics/<country>/prices?Related=Core Consumer Prices
/v1/economics/<country>/prices?Related=Core Inflation Rate
/v1/economics/<country>/prices?Related=GDP Deflator
/v1/economics/<country>/prices?Related=Producer Prices
/v1/economics/<country>/prices?Related=Producer Prices Change
/v1/economics/<country>/prices?Related=Export Prices
/v1/economics/<country>/prices?Related=Import Prices
/v1/economics/<country>/prices?Related=Food Inflation
/v1/economics/<country>/prices?Related=Core Inflation Rate MoM
/v1/economics/<country>/prices?Related=Core PCE Price Index Annual Change
/v1/economics/<country>/prices?Related=Core PCE Price Index MoM
/v1/economics/<country>/prices?Related=Core PCE Prices QoQ
/v1/economics/<country>/prices?Related=Core Producer Prices MoM
/v1/economics/<country>/prices?Related=Core Producer Prices YoY
/v1/economics/<country>/prices?Related=CPI seasonally adjusted
/v1/economics/<country>/prices?Related=Energy Inflation
/v1/economics/<country>/prices?Related=Export Prices MoM
/v1/economics/<country>/prices?Related=Export Prices YoY
/v1/economics/<country>/prices?Related=Import Prices MoM
/v1/economics/<country>/prices?Related=Import Prices YoY
/v1/economics/<country>/prices?Related=Michigan 5 Year Inflation Expectations
/v1/economics/<country>/prices?Related=Michigan Inflation Expectations
/v1/economics/<country>/prices?Related=PCE Price Index Annual Change
/v1/economics/<country>/prices?Related=PCE Price Index Monthly Change
/v1/economics/<country>/prices?Related=PCE Prices QoQ
/v1/economics/<country>/prices?Related=PPI Ex Food Energy and Trade Services MoM
/v1/economics/<country>/prices?Related=PPI Ex Food Energy and Trade Services YoY
/v1/economics/<country>/prices?Related=Producer Price Inflation MoM
/v1/economics/<country>/prices?Related=Rent Inflation
/v1/economics/<country>/prices?Related=Services Inflation
/v1/economics/<country>/prices?Related=Core PCE Price Index
/v1/economics/<country>/prices?Related=Core Producer Prices
/v1/economics/<country>/prices?Related=CPI Core Core
/v1/economics/<country>/prices?Related=CPI Housing Utilities
/v1/economics/<country>/prices?Related=CPI Median
/v1/economics/<country>/prices?Related=CPI Transportation
/v1/economics/<country>/prices?Related=CPI Trimmed-Mean
/v1/economics/<country>/prices?Related=Inflation Expectations
/v1/economics/<country>/prices?Related=PCE Price Index

**Health**
/v1/economics/<country>/health
/v1/economics/<country>/health?Related=Coronavirus Vaccination Rate
/v1/economics/<country>/health?Related=Coronavirus Vaccination Total
/v1/economics/<country>/health?Related=Coronavirus Cases
/v1/economics/<country>/health?Related=Coronavirus Deaths
/v1/economics/<country>/health?Related=Hospital Beds
/v1/economics/<country>/health?Related=Hospitals
/v1/economics/<country>/health?Related=Medical Doctors
/v1/economics/<country>/health?Related=Nurses

**Money**
/v1/economics/<country>/money
/v1/economics/<country>/money?Related=Interest Rate
/v1/economics/<country>/money?Related=Interbank Rate
/v1/economics/<country>/money?Related=Money Supply M0
/v1/economics/<country>/money?Related=Money Supply M1
/v1/economics/<country>/money?Related=Money Supply M2
/v1/economics/<country>/money?Related=Banks Balance Sheet
/v1/economics/<country>/money?Related=Central Bank Balance Sheet
/v1/economics/<country>/money?Related=Foreign Exchange Reserves
/v1/economics/<country>/money?Related=Loans to Private Sector
/v1/economics/<country>/money?Related=Effective Federal Funds Rate
/v1/economics/<country>/money?Related=Fed Capital Account Surplus
/v1/economics/<country>/money?Related=Proxy Funds Rate
/v1/economics/<country>/money?Related=Secured Overnight Financing Rate
/v1/economics/<country>/money?Related=Foreign Bond Investment
/v1/economics/<country>/money?Related=Private Debt to GDP
/v1/economics/<country>/money?Related=Repo Rate

**Trade**
/v1/economics/<country>/trade
/v1/economics/<country>/trade?Related=Balance of Trade
/v1/economics/<country>/trade?Related=Current Account
/v1/economics/<country>/trade?Related=Current Account to GDP
/v1/economics/<country>/trade?Related=Exports
/v1/economics/<country>/trade?Related=Imports
/v1/economics/<country>/trade?Related=External Debt
/v1/economics/<country>/trade?Related=Terms of Trade
/v1/economics/<country>/trade?Related=Capital Flows
/v1/economics/<country>/trade?Related=Foreign Direct Investment
/v1/economics/<country>/trade?Related=Net Long-term TIC Flows
/v1/economics/<country>/trade?Related=Gold Reserves
/v1/economics/<country>/trade?Related=Crude Oil Production
/v1/economics/<country>/trade?Related=Auto Exports
/v1/economics/<country>/trade?Related=Weekly Crude Oil Production
/v1/economics/<country>/trade?Related=Goods Trade Balance
/v1/economics/<country>/trade?Related=Oil Exports
/v1/economics/<country>/trade?Related=Terrorism Index
/v1/economics/<country>/trade?Related=Tourism Revenues
/v1/economics/<country>/trade?Related=Tourist Arrivals
/v1/economics/<country>/trade?Related=Weapons Sales

Government
/v1/economics/<country>/government
/v1/economics/<country>/government?Related=Government Debt to GDP
/v1/economics/<country>/government?Related=Government Budget
/v1/economics/<country>/government?Related=Government Budget Value
/v1/economics/<country>/government?Related=Government Spending
/v1/economics/<country>/government?Related=Government Revenues
/v1/economics/<country>/government?Related=Government Debt
/v1/economics/<country>/government?Related=Fiscal Expenditure
/v1/economics/<country>/government?Related=Asylum Applications
/v1/economics/<country>/government?Related=Government Spending to GDP
/v1/economics/<country>/government?Related=Military Expenditure
/v1/economics/<country>/government?Related=Corporate Tax Rate
/v1/economics/<country>/government?Related=Personal Income Tax Rate
/v1/economics/<country>/government?Related=Sales Tax Rate
/v1/economics/<country>/government?Related=Social Security Rate
/v1/economics/<country>/government?Related=Social Security Rate For Companies
/v1/economics/<country>/government?Related=Social Security Rate For Employees
/v1/economics/<country>/government?Related=Withholding Tax Rate

**Business**
/v1/economics/<country>/business
/v1/economics/<country>/business?Related=Business Confidence
/v1/economics/<country>/business?Related=Manufacturing PMI
/v1/economics/<country>/business?Related=Non Manufacturing PMI
/v1/economics/<country>/business?Related=Services PMI
/v1/economics/<country>/business?Related=Composite PMI
/v1/economics/<country>/business?Related=Industrial Production
/v1/economics/<country>/business?Related=Industrial Production Mom
/v1/economics/<country>/business?Related=Manufacturing Production
/v1/economics/<country>/business?Related=Capacity Utilization
/v1/economics/<country>/business?Related=Durable Goods Orders
/v1/economics/<country>/business?Related=Durable Goods Orders Ex Defense
/v1/economics/<country>/business?Related=Durable Goods Orders Ex Transportation
/v1/economics/<country>/business?Related=Factory Orders Ex Transportation
/v1/economics/<country>/business?Related=Factory Orders
/v1/economics/<country>/business?Related=New Orders
/v1/economics/<country>/business?Related=Business Inventories
/v1/economics/<country>/business?Related=Changes in Inventories
/v1/economics/<country>/business?Related=Wholesale Inventories
/v1/economics/<country>/business?Related=Bankruptcies
/v1/economics/<country>/business?Related=Corporate Profits
/v1/economics/<country>/business?Related=NFIB Business Optimism Index
/v1/economics/<country>/business?Related=Chicago Fed National Activity Index
/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Index
/v1/economics/<country>/business?Related=NY Empire State Manufacturing Index
/v1/economics/<country>/business?Related=Philadelphia Fed Manufacturing Index
/v1/economics/<country>/business?Related=Richmond Fed Manufacturing Index
/v1/economics/<country>/business?Related=Chicago PMI
/v1/economics/<country>/business?Related=Car Production
/v1/economics/<country>/business?Related=Car Registrations
/v1/economics/<country>/business?Related=Total Vehicle Sales
/v1/economics/<country>/business?Related=Crude Oil Stocks Change
/v1/economics/<country>/business?Related=Gasoline Stocks Change
/v1/economics/<country>/business?Related=Natural Gas Stocks Change
/v1/economics/<country>/business?Related=Leading Economic Index
/v1/economics/<country>/business?Related=API Crude Oil Stock Change
/v1/economics/<country>/business?Related=CFNAI Employment Index
/v1/economics/<country>/business?Related=CFNAI Personal Consumption and Housing Index
/v1/economics/<country>/business?Related=CFNAI Production Index
/v1/economics/<country>/business?Related=CFNAI Sales Orders and Inventories Index
/v1/economics/<country>/business?Related=Coincident Index
/v1/economics/<country>/business?Related=Composite Leading Indicator
/v1/economics/<country>/business?Related=Crude Oil Rigs
/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Employment Index
/v1/economics/<country>/business?Related=Dallas Fed Manufacturing New Orders Index
/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Prices Paid Index
/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Production Index
/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Shipments Index
/v1/economics/<country>/business?Related=Dallas Fed Services Index
/v1/economics/<country>/business?Related=Dallas Fed Services Revenues Index
/v1/economics/<country>/business?Related=ISM Manufacturing Employment
/v1/economics/<country>/business?Related=ISM Manufacturing New Orders
/v1/economics/<country>/business?Related=ISM Manufacturing Prices
/v1/economics/<country>/business?Related=ISM Non Manufacturing Business Activity
/v1/economics/<country>/business?Related=ISM Non Manufacturing Employment
/v1/economics/<country>/business?Related=ISM Non Manufacturing New Orders
/v1/economics/<country>/business?Related=ISM Non Manufacturing Prices
/v1/economics/<country>/business?Related=Kansas Fed Composite Index
/v1/economics/<country>/business?Related=Kansas Fed Employment Index
/v1/economics/<country>/business?Related=Kansas Fed New Orders Index
/v1/economics/<country>/business?Related=Kansas Fed Prices Paid Index
/v1/economics/<country>/business?Related=Kansas Fed Shipments Index
/v1/economics/<country>/business?Related=Manufacturing Production MoM
/v1/economics/<country>/business?Related=Non Defense Capital Goods Orders Ex Aircraft
/v1/economics/<country>/business?Related=NY Empire State Employment Index
/v1/economics/<country>/business?Related=NY Empire State New Orders Index
/v1/economics/<country>/business?Related=NY Empire State Prices Paid Index
/v1/economics/<country>/business?Related=NY Empire State Shipments Index
/v1/economics/<country>/business?Related=Philly Fed Business Conditions
/v1/economics/<country>/business?Related=Philly Fed CAPEX Index
/v1/economics/<country>/business?Related=Philly Fed Employment
/v1/economics/<country>/business?Related=Philly Fed New Orders
/v1/economics/<country>/business?Related=Philly Fed Prices Paid
/v1/economics/<country>/business?Related=Retail Inventories Ex Autos
/v1/economics/<country>/business?Related=Richmond Fed Manufacturing Shipments
/v1/economics/<country>/business?Related=Richmond Fed Services Index
/v1/economics/<country>/business?Related=Strategic Petroleum Reserve Crude Oil Stocks
/v1/economics/<country>/business?Related=Total Rigs
/v1/economics/<country>/business?Related=API Crude Imports
/v1/economics/<country>/business?Related=API Crude Runs
/v1/economics/<country>/business?Related=API Cushing Number
/v1/economics/<country>/business?Related=API Distillate Stocks
/v1/economics/<country>/business?Related=API Gasoline Stocks
/v1/economics/<country>/business?Related=API Heating Oil
/v1/economics/<country>/business?Related=API Product Imports
/v1/economics/<country>/business?Related=Corruption Index
/v1/economics/<country>/business?Related=Corruption Rank
/v1/economics/<country>/business?Related=Crude Oil Imports
/v1/economics/<country>/business?Related=Cushing Crude Oil Stocks
/v1/economics/<country>/business?Related=Distillate Fuel Production
/v1/economics/<country>/business?Related=Distillate Stocks
/v1/economics/<country>/business?Related=Gasoline Production
/v1/economics/<country>/business?Related=Grain Stocks Corn
/v1/economics/<country>/business?Related=Grain Stocks Soy
/v1/economics/<country>/business?Related=Grain Stocks Wheat
/v1/economics/<country>/business?Related=Heating Oil Stocks
/v1/economics/<country>/business?Related=Kansas Fed Manufacturing Index
/v1/economics/<country>/business?Related=Lmi Inventory Costs
/v1/economics/<country>/business?Related=Lmi Logistics Managers Index Current
/v1/economics/<country>/business?Related=Lmi Logistics Managers Index Future
/v1/economics/<country>/business?Related=Lmi Transportation Prices
/v1/economics/<country>/business?Related=Lmi Warehouse Prices
/v1/economics/<country>/business?Related=Mining Production
/v1/economics/<country>/business?Related=Refinery Crude Runs
/v1/economics/<country>/business?Related=Steel Production

**Consumer**
/v1/economics/<country>/consumer
/v1/economics/<country>/consumer?Related=Consumer Confidence
/v1/economics/<country>/consumer?Related=Retail Sales MoM
/v1/economics/<country>/consumer?Related=Retail Sales Ex Autos
/v1/economics/<country>/consumer?Related=Retail Sales YoY
/v1/economics/<country>/consumer?Related=Consumer Spending
/v1/economics/<country>/consumer?Related=Disposable Personal Income
/v1/economics/<country>/consumer?Related=Personal Spending
/v1/economics/<country>/consumer?Related=Personal Income
/v1/economics/<country>/consumer?Related=Personal Savings
/v1/economics/<country>/consumer?Related=Consumer Credit
/v1/economics/<country>/consumer?Related=Private Sector Credit
/v1/economics/<country>/consumer?Related=Bank Lending Rate
/v1/economics/<country>/consumer?Related=Economic Optimism Index
/v1/economics/<country>/consumer?Related=Redbook Index
/v1/economics/<country>/consumer?Related=Credit Card Accounts
/v1/economics/<country>/consumer?Related=Debt Balance Auto Loans
/v1/economics/<country>/consumer?Related=Debt Balance Credit Cards
/v1/economics/<country>/consumer?Related=Debt Balance Mortgages
/v1/economics/<country>/consumer?Related=Debt Balance Student Loans
/v1/economics/<country>/consumer?Related=Debt Balance Total
/v1/economics/<country>/consumer?Related=Michigan Consumer Expectations
/v1/economics/<country>/consumer?Related=Michigan Current Economic Conditions
/v1/economics/<country>/consumer?Related=Retail Sales Ex Gas and Autos MoM
/v1/economics/<country>/consumer?Related=Used Car Prices MoM
/v1/economics/<country>/consumer?Related=Used Car Prices YoY
/v1/economics/<country>/consumer?Related=Chain Store Sales
/v1/economics/<country>/consumer?Related=Gasoline Prices
/v1/economics/<country>/consumer?Related=Households Debt to GDP

**Housing**
/v1/economics/<country>/housing
/v1/economics/<country>/housing?Related=Building Permits
/v1/economics/<country>/housing?Related=Housing Starts
/v1/economics/<country>/housing?Related=New Home Sales
/v1/economics/<country>/housing?Related=Pending Home Sales
/v1/economics/<country>/housing?Related=Existing Home Sales
/v1/economics/<country>/housing?Related=Construction Spending
/v1/economics/<country>/housing?Related=Housing Index
/v1/economics/<country>/housing?Related=Nahb Housing Market Index
/v1/economics/<country>/housing?Related=Mortgage Rate
/v1/economics/<country>/housing?Related=Mortgage Applications
/v1/economics/<country>/housing?Related=15 Year Mortgage Rate
/v1/economics/<country>/housing?Related=30 Year Mortgage Rate
/v1/economics/<country>/housing?Related=Average House Prices
/v1/economics/<country>/housing?Related=Average Mortgage Size
/v1/economics/<country>/housing?Related=Building Permits MoM
/v1/economics/<country>/housing?Related=Case Shiller Home Price Index MoM
/v1/economics/<country>/housing?Related=Case Shiller Home Price Index YoY
/v1/economics/<country>/housing?Related=Existing Home Sales MoM
/v1/economics/<country>/housing?Related=House Price Index MoM
/v1/economics/<country>/housing?Related=House Price Index YoY
/v1/economics/<country>/housing?Related=Housing Starts MoM
/v1/economics/<country>/housing?Related=Housing Starts Multi Family
/v1/economics/<country>/housing?Related=Housing Starts Single Family
/v1/economics/<country>/housing?Related=MBA Mortgage Market Index
/v1/economics/<country>/housing?Related=MBA Mortgage Refinance Index
/v1/economics/<country>/housing?Related=MBA Purchase Index
/v1/economics/<country>/housing?Related=Mortgage Originations
/v1/economics/<country>/housing?Related=National Home Price Index
/v1/economics/<country>/housing?Related=New Home Sales MoM
/v1/economics/<country>/housing?Related=Pending Home Sales MoM
/v1/economics/<country>/housing?Related=Total Housing Inventory
/v1/economics/<country>/housing?Related=Case Shiller Home Price Index
/v1/economics/<country>/housing?Related=Home Ownership Rate
/v1/economics/<country>/housing?Related=Single Family Home Prices
/v1/economics/<country>/housing?Related=Price to Rent Ratio
/v1/economics/<country>/housing?Related=Residential Property Prices
```
---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/armanobosyan/economics-api.git
cd economics-api.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
python app.py
```

Or using Gunicorn (recommended for production):

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## Health Check

Verify API is live:

```bash
curl http://localhost:8000/v1/economics/United States/GDP?Related=GDP Growth Rate
```

---

## License

MIT License. Use freely with attribution. Data remains the property of original sources (e.g., TradingEconomics).

---

## Contributing

Pull requests and issue reports welcome. Please open an issue to discuss major changes before submitting.

