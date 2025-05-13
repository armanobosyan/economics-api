#########################################
### ED-API (Economics Data API 1.1.0  ###
#########################################


### BEGING # Library and Moduled import ###
# BEGIN # Standard library imports
import json
import os
import requests
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_caching import Cache            # optional
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
### END # Library and Moduled import ###


### BEGIN # Flask Parameters ###
# Initialize Flask application
app = Flask(__name__)
### END # Flask Parameters ###


### BEGIN # Dataframe # Define Utility Functions ###
def dataframe_to_json(df, date_col=None):
    """
    Converts a pandas DataFrame into a JSON string.
        Parameters:
    df (pd.DataFrame): DataFrame to be converted.
    date_col (str, optional): Column name in DataFrame to format as a date.
        Returns:
    str: JSON string representation of the DataFrame.
    """
    try:
        if isinstance(df, pd.DataFrame) and not df.empty:
            if date_col and date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col]).dt.strftime('%Y-%m-%d %H:%M:%S')
            return df.to_json(orient='records', date_format='iso', indent=4)
        else:
            return json.dumps({"message": "No data available"}, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)
# (Include any other utility functions here as needed)
### END # Dataframe # Define Utility Functions ###

### BEGIN # ECONOMICS Endpoints ###
### BEGIN # /economics/countries-overview ###
# Return the folowing information:
# Country, Current Account, Debt/GDP, GDP, GDP Growth, Gov. Budget, Inflation Rate, Interest Rate, Jobless Rate, Population
# For the folowing countries:
# United States, China, Euro Area, Japan, Germany, India, United Kingdom, France, Russia, Canada, Italy,
# Brazil, Australia, South Korea, Mexico, Spain, Indonesia, Saudi Arabia, Netherlands, Turkey, Switzerland, Taiwan, Poland
# The data is scraped from tradingeconomics.com

import requests
from bs4 import BeautifulSoup
import json

@app.route('/v1/economics/countries-overview', methods=['GET'])
def get_matrix():
    # URL of the page to scrape
    url = 'https://tradingeconomics.com/matrix?g=top'
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    # Initialize an empty list to hold dictionaries of row data
    data_dicts = []
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the table by class name
        table = soup.find('table', class_='table-heatmap')
        # Check if the table was found
        if table:
            # Extract headers
            headers = [header.text.strip() for header in table.find_all('th')]
            
            # Iterate over each row in the table
            for row in table.find_all('tr')[1:]:  # [1:] skips the header row
                # Extract text from each cell in the row
                row_data = [cell.text.strip() for cell in row.find_all('td')]
                # Create a dictionary for the current row
                row_dict = dict(zip(headers, row_data))
                # Append the dictionary to the list
                data_dicts.append(row_dict)
    else:
        return jsonify({"error": "Failed to retrieve the webpage"}), 500

    # Filter data based on query parameters
    filtered_data = []
    for item in data_dicts:
        if all(item.get(key, None) == request.args.get(key) for key in request.args):
            filtered_data.append(item)

    # Return all data if no filter is applied
    return jsonify(filtered_data if filtered_data else data_dicts)

#Usage /v1/economics/countries-overview?Country=China or any other Country # By default it will return all the data #
### END # /economics/countries-overview ###


### BEGIN # /economics/<country>/overview ###
@app.route('/v1/economics/<country>/overview', methods=['GET'])
def get_country_indicators(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table table-hover')
        
        data = []
        if table:
            rows = table.find_all('tr')[1:]  # Skipping the header row

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    related_text = cells[0].find('a').text.strip() if cells[0].find('a') else 'N/A'
                    data_dict = {
                        'Related': related_text,
                        'Last': cells[1].text.strip(),
                        'Previous': cells[2].text.strip(),
                        'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                        'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                        'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                        'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                    }
                    data.append(data_dict)

        # Check if a query parameter for 'Related' is provided
        related_query = request.args.get('Related')
        if related_query:
            # Filter the data based on the 'Related' query parameter
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500


#/v1/economics/<country>/overview
#/v1/economics/<country>/overview?Related=Currency
#/v1/economics/<country>/overview?Related=Stock Market
#/v1/economics/<country>/overview?Related=GDP Growth Rate
#/v1/economics/<country>/overview?Related=GDP Annual Growth Rate
#/v1/economics/<country>/overview?Related=Unemployment Rate
#/v1/economics/<country>/overview?Related=Non Farm Payrolls
#/v1/economics/<country>/overview?Related=Inflation Rate
#/v1/economics/<country>/overview?Related=Inflation Rate MoM
#/v1/economics/<country>/overview?Related=Interest Rate
#/v1/economics/<country>/overview?Related=Balance of Trade
#/v1/economics/<country>/overview?Related=Current Account to GDP
#/v1/economics/<country>/overview?Related=Government Debt to GDP
#/v1/economics/<country>/overview?Related=Government Budget
#/v1/economics/<country>/overview?Related=Business Confidence
#/v1/economics/<country>/overview?Related=Manufacturing PMI
#/v1/economics/<country>/overview?Related=Services PMI
#/v1/economics/<country>/overview?Related=Consumer Confidence
#/v1/economics/<country>/overview?Related=Retail Sales MoM
#/v1/economics/<country>/overview?Related=Building Permits
#/v1/economics/<country>/overview?Related=Personal Income Tax Rate
    
## END # /economics/<country>/overview ###


### BEGIN # /economics/<country>/gdp ###
@app.route('/v1/economics/<country>/gdp', methods=['GET'])
def get_gdp_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Assuming 'gdp' is a consistent section id across different country pages on the website
        gdp_section = soup.find('div', id='gdp')
        table = gdp_section.find('table', class_='table table-hover') if gdp_section else None

        data = []
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    related_link = cells[0].find('a')
                    related_text = related_link.text.strip() if related_link else 'N/A'
                    data_dict = {
                        'Related': related_text,
                        'Last': cells[1].text.strip(),
                        'Previous': cells[2].text.strip(),
                        'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                        'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                        'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                        'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                    }
                    data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/GDP
#/v1/economics/<country>/GDP?Related=GDP Growth Rate
#/v1/economics/<country>/GDP?Related=GDP Annual Growth Rate
#/v1/economics/<country>/GDP?Related=GDP
#/v1/economics/<country>/GDP?Related=Gross National Product
#/v1/economics/<country>/GDP?Related=Gross Fixed Capital Formation
#/v1/economics/<country>/GDP?Related=GDP per Capita
#/v1/economics/<country>/GDP?Related=GDP per Capita PPP
#/v1/economics/<country>/GDP?Related=Full Year GDP Growth
#/v1/economics/<country>/GDP?Related=GDP Sales QoQ
#/v1/economics/<country>/GDP?Related=Real Consumer Spending
#/v1/economics/<country>/GDP?Related=Weekly Economic Index
#/v1/economics/<country>/GDP?Related=GDP from Agriculture
#/v1/economics/<country>/GDP?Related=GDP from Construction
#/v1/economics/<country>/GDP?Related=GDP from Manufacturing
#/v1/economics/<country>/GDP?Related=GDP from Mining
#/v1/economics/<country>/GDP?Related=GDP from Public Administration
#/v1/economics/<country>/GDP?Related=GDP from Services
#/v1/economics/<country>/GDP?Related=GDP from Transport
#/v1/economics/<country>/GDP?Related=GDP from Utilities
    
## END # /economics/<country>/GDP ###
    

### BEGIN # /economics/<country>/labour ###   
@app.route('/v1/economics/<country>/labour', methods=['GET'])
def get_labour_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        labour_section = soup.find('div', id='labour')
        table = labour_section.find('table', class_='table table-hover') if labour_section else None

        data = []
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    related_link = cells[0].find('a')
                    related_text = related_link.text.strip() if related_link else 'N/A'
                    data_dict = {
                        'Related': related_text,
                        'Last': cells[1].text.strip(),
                        'Previous': cells[2].text.strip(),
                        'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                        'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                        'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                        'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                    }
                    data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/labour
#/v1/economics/<country>/labour?Related=Unemployment Rate
#/v1/economics/<country>/labour?Related=Non Farm Payrolls
#/v1/economics/<country>/labour?Related=Government Payrolls
#/v1/economics/<country>/labour?Related=Nonfarm Payrolls Private
#/v1/economics/<country>/labour?Related=Manufacturing Payrolls
#/v1/economics/<country>/labour?Related=Initial Jobless Claims
#/v1/economics/<country>/labour?Related=Continuing Jobless Claims
#/v1/economics/<country>/labour?Related=ADP Employment Change
#/v1/economics/<country>/labour?Related=Employed Persons
#/v1/economics/<country>/labour?Related=Average Hourly Earnings
#/v1/economics/<country>/labour?Related=Average Weekly Hours
#/v1/economics/<country>/labour?Related=Labor Force Participation Rate
#/v1/economics/<country>/labour?Related=Long Term Unemployment Rate
#/v1/economics/<country>/labour?Related=Youth Unemployment Rate
#/v1/economics/<country>/labour?Related=Labour Costs
#/v1/economics/<country>/labour?Related=Productivity
#/v1/economics/<country>/labour?Related=Job Vacancies
#/v1/economics/<country>/labour?Related=Challenger Job Cuts
#/v1/economics/<country>/labour?Related=Wages
#/v1/economics/<country>/labour?Related=Minimum Wages
#/v1/economics/<country>/labour?Related=Wage Growth
#/v1/economics/<country>/labour?Related=Wages in Manufacturing
#/v1/economics/<country>/labour?Related=Employment Cost Index
#/v1/economics/<country>/labour?Related=Population
#/v1/economics/<country>/labour?Related=Retirement Age Women
#/v1/economics/<country>/labour?Related=Retirement Age Men
#/v1/economics/<country>/labour?Related=Average Hourly Earnings YoY
#/v1/economics/<country>/labour?Related=Employment Cost Index Benefits
#/v1/economics/<country>/labour?Related=Employment Cost Index Wages
#/v1/economics/<country>/labour?Related=Hiring Plans Announcements
#/v1/economics/<country>/labour?Related=Job Layoffs and Discharges
#/v1/economics/<country>/labour?Related=Job Quits
#/v1/economics/<country>/labour?Related=Job Quits Rate
#/v1/economics/<country>/labour?Related=Nonfarm Productivity QoQ
#/v1/economics/<country>/labour?Related=U6 Unemployment Rate
#/v1/economics/<country>/labour?Related=Unit Labour Costs QoQ
#/v1/economics/<country>/labour?Related=Employment Rate
#/v1/economics/<country>/labour?Related=Full Time Employment
#/v1/economics/<country>/labour?Related=Jobless Claims 4-week Average
#/v1/economics/<country>/labour?Related=Part Time Employment
    
### END # /economics/<country>/labour ###


### BEGIN # /economics/<country>/prices ###
@app.route('/v1/economics/<country>/prices', methods=['GET'])
def get_prices_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        prices_section = soup.find('div', id='prices')
        table = prices_section.find('table', class_='table table-hover') if prices_section else None

        data = []
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    related_link = cells[0].find('a')
                    related_text = related_link.text.strip() if related_link else 'N/A'
                    data_dict = {
                        'Related': related_text,
                        'Last': cells[1].text.strip(),
                        'Previous': cells[2].text.strip(),
                        'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                        'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                        'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                        'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                    }
                    data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/prices
#/v1/economics/<country>/prices?Related=Inflation Rate
#/v1/economics/<country>/prices?Related=Inflation Rate MoM
#/v1/economics/<country>/prices?Related=Consumer Price Index CPI
#/v1/economics/<country>/prices?Related=Core Consumer Prices
#/v1/economics/<country>/prices?Related=Core Inflation Rate
#/v1/economics/<country>/prices?Related=GDP Deflator
#/v1/economics/<country>/prices?Related=Producer Prices
#/v1/economics/<country>/prices?Related=Producer Prices Change
#/v1/economics/<country>/prices?Related=Export Prices
#/v1/economics/<country>/prices?Related=Import Prices
#/v1/economics/<country>/prices?Related=Food Inflation
#/v1/economics/<country>/prices?Related=Core Inflation Rate MoM
#/v1/economics/<country>/prices?Related=Core PCE Price Index Annual Change
#/v1/economics/<country>/prices?Related=Core PCE Price Index MoM
#/v1/economics/<country>/prices?Related=Core PCE Prices QoQ
#/v1/economics/<country>/prices?Related=Core Producer Prices MoM
#/v1/economics/<country>/prices?Related=Core Producer Prices YoY
#/v1/economics/<country>/prices?Related=CPI seasonally adjusted
#/v1/economics/<country>/prices?Related=Energy Inflation
#/v1/economics/<country>/prices?Related=Export Prices MoM
#/v1/economics/<country>/prices?Related=Export Prices YoY
#/v1/economics/<country>/prices?Related=Import Prices MoM
#/v1/economics/<country>/prices?Related=Import Prices YoY
#/v1/economics/<country>/prices?Related=Michigan 5 Year Inflation Expectations
#/v1/economics/<country>/prices?Related=Michigan Inflation Expectations
#/v1/economics/<country>/prices?Related=PCE Price Index Annual Change
#/v1/economics/<country>/prices?Related=PCE Price Index Monthly Change
#/v1/economics/<country>/prices?Related=PCE Prices QoQ
#/v1/economics/<country>/prices?Related=PPI Ex Food Energy and Trade Services MoM
#/v1/economics/<country>/prices?Related=PPI Ex Food Energy and Trade Services YoY
#/v1/economics/<country>/prices?Related=Producer Price Inflation MoM
#/v1/economics/<country>/prices?Related=Rent Inflation
#/v1/economics/<country>/prices?Related=Services Inflation
#/v1/economics/<country>/prices?Related=Core PCE Price Index
#/v1/economics/<country>/prices?Related=Core Producer Prices
#/v1/economics/<country>/prices?Related=CPI Core Core
#/v1/economics/<country>/prices?Related=CPI Housing Utilities
#/v1/economics/<country>/prices?Related=CPI Median
#/v1/economics/<country>/prices?Related=CPI Transportation
#/v1/economics/<country>/prices?Related=CPI Trimmed-Mean
#/v1/economics/<country>/prices?Related=Inflation Expectations
#/v1/economics/<country>/prices?Related=PCE Price Index

### END # /economics/<country>/prices ###
    

### BEGIN # /economics/<country>/health ###
@app.route('/v1/economics/<country>/health', methods=['GET'])
def get_health_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        health_section = soup.find('div', id='health')
        table = health_section.find('table', class_='table table-hover') if health_section else None

        data = []
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    related_link = cells[0].find('a')
                    related_text = related_link.text.strip() if related_link else 'N/A'
                    data_dict = {
                        'Related': related_text,
                        'Last': cells[1].text.strip(),
                        'Previous': cells[2].text.strip(),
                        'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                        'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                        'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                        'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                    }
                    data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/health
#/v1/economics/<country>/health?Related=Coronavirus Vaccination Rate
#/v1/economics/<country>/health?Related=Coronavirus Vaccination Total
#/v1/economics/<country>/health?Related=Coronavirus Cases
#/v1/economics/<country>/health?Related=Coronavirus Deaths
#/v1/economics/<country>/health?Related=Hospital Beds
#/v1/economics/<country>/health?Related=Hospitals
#/v1/economics/<country>/health?Related=Medical Doctors
#/v1/economics/<country>/health?Related=Nurses

### END # /economics/<country>/health ###
    

### BEGIN # /economics/<country>/money ###
@app.route('/v1/economics/<country>/money', methods=['GET'])
def get_money_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        money_section = soup.find('div', id='money')
        table = money_section.find('table', class_='table table-hover') if money_section else None

        data = []
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    related_link = cells[0].find('a')
                    related_text = related_link.text.strip() if related_link else 'N/A'
                    data_dict = {
                        'Related': related_text,
                        'Last': cells[1].text.strip(),
                        'Previous': cells[2].text.strip(),
                        'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                        'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                        'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                        'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                    }
                    data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/money
#/v1/economics/<country>/money?Related=Interest Rate
#/v1/economics/<country>/money?Related=Interbank Rate
#/v1/economics/<country>/money?Related=Money Supply M0
#/v1/economics/<country>/money?Related=Money Supply M1
#/v1/economics/<country>/money?Related=Money Supply M2
#/v1/economics/<country>/money?Related=Banks Balance Sheet
#/v1/economics/<country>/money?Related=Central Bank Balance Sheet
#/v1/economics/<country>/money?Related=Foreign Exchange Reserves
#/v1/economics/<country>/money?Related=Loans to Private Sector
#/v1/economics/<country>/money?Related=Effective Federal Funds Rate
#/v1/economics/<country>/money?Related=Fed Capital Account Surplus
#/v1/economics/<country>/money?Related=Proxy Funds Rate
#/v1/economics/<country>/money?Related=Secured Overnight Financing Rate
#/v1/economics/<country>/money?Related=Foreign Bond Investment
#/v1/economics/<country>/money?Related=Private Debt to GDP
#/v1/economics/<country>/money?Related=Repo Rate
    
### END # /economics/<country>/money ###
    

### BEGIN # /economics/<country>/trade ###
@app.route('/v1/economics/<country>/trade', methods=['GET'])
def get_trade_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        trade_section = soup.find('div', id='trade')
        table = trade_section.find('table', class_='table table-hover') if trade_section else None

        data = []
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    related_link = cells[0].find('a')
                    related_text = related_link.text.strip() if related_link else 'N/A'
                    data_dict = {
                        'Related': related_text,
                        'Last': cells[1].text.strip(),
                        'Previous': cells[2].text.strip(),
                        'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                        'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                        'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                        'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                    }
                    data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/trade
#/v1/economics/<country>/trade?Related=Balance of Trade
#/v1/economics/<country>/trade?Related=Current Account
#/v1/economics/<country>/trade?Related=Current Account to GDP
#/v1/economics/<country>/trade?Related=Exports
#/v1/economics/<country>/trade?Related=Imports
#/v1/economics/<country>/trade?Related=External Debt
#/v1/economics/<country>/trade?Related=Terms of Trade
#/v1/economics/<country>/trade?Related=Capital Flows
#/v1/economics/<country>/trade?Related=Foreign Direct Investment
#/v1/economics/<country>/trade?Related=Net Long-term TIC Flows
#/v1/economics/<country>/trade?Related=Gold Reserves
#/v1/economics/<country>/trade?Related=Crude Oil Production
#/v1/economics/<country>/trade?Related=Auto Exports
#/v1/economics/<country>/trade?Related=Weekly Crude Oil Production
#/v1/economics/<country>/trade?Related=Goods Trade Balance
#/v1/economics/<country>/trade?Related=Oil Exports
#/v1/economics/<country>/trade?Related=Terrorism Index
#/v1/economics/<country>/trade?Related=Tourism Revenues
#/v1/economics/<country>/trade?Related=Tourist Arrivals
#/v1/economics/<country>/trade?Related=Weapons Sales
    
### END # /economics/<country>/trade ###
    

### BEGIN # /economics/<country>/government ###
@app.route('/v1/economics/<country>/government', methods=['GET'])
def get_government_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        government_section = soup.find('div', id='government')
        tables = government_section.find_all('table', class_='table table-hover') if government_section else None

        data = []
        if tables:
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip the header row
                for row in rows:
                    cells = row.find_all('td')
                    if cells:
                        related_link = cells[0].find('a')
                        related_text = related_link.text.strip() if related_link else 'N/A'
                        data_dict = {
                            'Related': related_text,
                            'Last': cells[1].text.strip(),
                            'Previous': cells[2].text.strip(),
                            'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                            'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                            'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                            'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                        }
                        data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/government
#/v1/economics/<country>/government?Related=Government Debt to GDP
#/v1/economics/<country>/government?Related=Government Budget
#/v1/economics/<country>/government?Related=Government Budget Value
#/v1/economics/<country>/government?Related=Government Spending
#/v1/economics/<country>/government?Related=Government Revenues
#/v1/economics/<country>/government?Related=Government Debt
#/v1/economics/<country>/government?Related=Fiscal Expenditure
#/v1/economics/<country>/government?Related=Asylum Applications
#/v1/economics/<country>/government?Related=Government Spending to GDP
#/v1/economics/<country>/government?Related=Military Expenditure
#/v1/economics/<country>/government?Related=Corporate Tax Rate
#/v1/economics/<country>/government?Related=Personal Income Tax Rate
#/v1/economics/<country>/government?Related=Sales Tax Rate
#/v1/economics/<country>/government?Related=Social Security Rate
#/v1/economics/<country>/government?Related=Social Security Rate For Companies
#/v1/economics/<country>/government?Related=Social Security Rate For Employees
#/v1/economics/<country>/government?Related=Withholding Tax Rate
    
### END # /economics/<country>/government ###


### BEGIN # /economics/<country>/business ###
@app.route('/v1/economics/<country>/business', methods=['GET'])
def get_business_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        business_section = soup.find('div', id='business')  # Assuming 'business' is the ID for the business section
        tables = business_section.find_all('table', class_='table table-hover') if business_section else None

        data = []
        if tables:
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip the header row
                for row in rows:
                    cells = row.find_all('td')
                    if cells:
                        related_link = cells[0].find('a')
                        related_text = related_link.text.strip() if related_link else 'N/A'
                        data_dict = {
                            'Related': related_text,
                            'Last': cells[1].text.strip(),
                            'Previous': cells[2].text.strip(),
                            'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                            'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                            'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                            'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                        }
                        data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/business
#/v1/economics/<country>/business?Related=Business Confidence
#/v1/economics/<country>/business?Related=Manufacturing PMI
#/v1/economics/<country>/business?Related=Non Manufacturing PMI
#/v1/economics/<country>/business?Related=Services PMI
#/v1/economics/<country>/business?Related=Composite PMI
#/v1/economics/<country>/business?Related=Industrial Production
#/v1/economics/<country>/business?Related=Industrial Production Mom
#/v1/economics/<country>/business?Related=Manufacturing Production
#/v1/economics/<country>/business?Related=Capacity Utilization
#/v1/economics/<country>/business?Related=Durable Goods Orders
#/v1/economics/<country>/business?Related=Durable Goods Orders Ex Defense
#/v1/economics/<country>/business?Related=Durable Goods Orders Ex Transportation
#/v1/economics/<country>/business?Related=Factory Orders Ex Transportation
#/v1/economics/<country>/business?Related=Factory Orders
#/v1/economics/<country>/business?Related=New Orders
#/v1/economics/<country>/business?Related=Business Inventories
#/v1/economics/<country>/business?Related=Changes in Inventories
#/v1/economics/<country>/business?Related=Wholesale Inventories
#/v1/economics/<country>/business?Related=Bankruptcies
#/v1/economics/<country>/business?Related=Corporate Profits
#/v1/economics/<country>/business?Related=NFIB Business Optimism Index
#/v1/economics/<country>/business?Related=Chicago Fed National Activity Index
#/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Index
#/v1/economics/<country>/business?Related=NY Empire State Manufacturing Index
#/v1/economics/<country>/business?Related=Philadelphia Fed Manufacturing Index
#/v1/economics/<country>/business?Related=Richmond Fed Manufacturing Index
#/v1/economics/<country>/business?Related=Chicago PMI
#/v1/economics/<country>/business?Related=Car Production
#/v1/economics/<country>/business?Related=Car Registrations
#/v1/economics/<country>/business?Related=Total Vehicle Sales
#/v1/economics/<country>/business?Related=Crude Oil Stocks Change
#/v1/economics/<country>/business?Related=Gasoline Stocks Change
#/v1/economics/<country>/business?Related=Natural Gas Stocks Change
#/v1/economics/<country>/business?Related=Leading Economic Index
#/v1/economics/<country>/business?Related=API Crude Oil Stock Change
#/v1/economics/<country>/business?Related=CFNAI Employment Index
#/v1/economics/<country>/business?Related=CFNAI Personal Consumption and Housing Index
#/v1/economics/<country>/business?Related=CFNAI Production Index
#/v1/economics/<country>/business?Related=CFNAI Sales Orders and Inventories Index
#/v1/economics/<country>/business?Related=Coincident Index
#/v1/economics/<country>/business?Related=Composite Leading Indicator
#/v1/economics/<country>/business?Related=Crude Oil Rigs
#/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Employment Index
#/v1/economics/<country>/business?Related=Dallas Fed Manufacturing New Orders Index
#/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Prices Paid Index
#/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Production Index
#/v1/economics/<country>/business?Related=Dallas Fed Manufacturing Shipments Index
#/v1/economics/<country>/business?Related=Dallas Fed Services Index
#/v1/economics/<country>/business?Related=Dallas Fed Services Revenues Index
#/v1/economics/<country>/business?Related=ISM Manufacturing Employment
#/v1/economics/<country>/business?Related=ISM Manufacturing New Orders
#/v1/economics/<country>/business?Related=ISM Manufacturing Prices
#/v1/economics/<country>/business?Related=ISM Non Manufacturing Business Activity
#/v1/economics/<country>/business?Related=ISM Non Manufacturing Employment
#/v1/economics/<country>/business?Related=ISM Non Manufacturing New Orders
#/v1/economics/<country>/business?Related=ISM Non Manufacturing Prices
#/v1/economics/<country>/business?Related=Kansas Fed Composite Index
#/v1/economics/<country>/business?Related=Kansas Fed Employment Index
#/v1/economics/<country>/business?Related=Kansas Fed New Orders Index
#/v1/economics/<country>/business?Related=Kansas Fed Prices Paid Index
#/v1/economics/<country>/business?Related=Kansas Fed Shipments Index
#/v1/economics/<country>/business?Related=Manufacturing Production MoM
#/v1/economics/<country>/business?Related=Non Defense Capital Goods Orders Ex Aircraft
#/v1/economics/<country>/business?Related=NY Empire State Employment Index
#/v1/economics/<country>/business?Related=NY Empire State New Orders Index
#/v1/economics/<country>/business?Related=NY Empire State Prices Paid Index
#/v1/economics/<country>/business?Related=NY Empire State Shipments Index
#/v1/economics/<country>/business?Related=Philly Fed Business Conditions
#/v1/economics/<country>/business?Related=Philly Fed CAPEX Index
#/v1/economics/<country>/business?Related=Philly Fed Employment
#/v1/economics/<country>/business?Related=Philly Fed New Orders
#/v1/economics/<country>/business?Related=Philly Fed Prices Paid
#/v1/economics/<country>/business?Related=Retail Inventories Ex Autos
#/v1/economics/<country>/business?Related=Richmond Fed Manufacturing Shipments
#/v1/economics/<country>/business?Related=Richmond Fed Services Index
#/v1/economics/<country>/business?Related=Strategic Petroleum Reserve Crude Oil Stocks
#/v1/economics/<country>/business?Related=Total Rigs
#/v1/economics/<country>/business?Related=API Crude Imports
#/v1/economics/<country>/business?Related=API Crude Runs
#/v1/economics/<country>/business?Related=API Cushing Number
#/v1/economics/<country>/business?Related=API Distillate Stocks
#/v1/economics/<country>/business?Related=API Gasoline Stocks
#/v1/economics/<country>/business?Related=API Heating Oil
#/v1/economics/<country>/business?Related=API Product Imports
#/v1/economics/<country>/business?Related=Corruption Index
#/v1/economics/<country>/business?Related=Corruption Rank
#/v1/economics/<country>/business?Related=Crude Oil Imports
#/v1/economics/<country>/business?Related=Cushing Crude Oil Stocks
#/v1/economics/<country>/business?Related=Distillate Fuel Production
#/v1/economics/<country>/business?Related=Distillate Stocks
#/v1/economics/<country>/business?Related=Gasoline Production
#/v1/economics/<country>/business?Related=Grain Stocks Corn
#/v1/economics/<country>/business?Related=Grain Stocks Soy
#/v1/economics/<country>/business?Related=Grain Stocks Wheat
#/v1/economics/<country>/business?Related=Heating Oil Stocks
#/v1/economics/<country>/business?Related=Kansas Fed Manufacturing Index
#/v1/economics/<country>/business?Related=Lmi Inventory Costs
#/v1/economics/<country>/business?Related=Lmi Logistics Managers Index Current
#/v1/economics/<country>/business?Related=Lmi Logistics Managers Index Future
#/v1/economics/<country>/business?Related=Lmi Transportation Prices
#/v1/economics/<country>/business?Related=Lmi Warehouse Prices
#/v1/economics/<country>/business?Related=Mining Production
#/v1/economics/<country>/business?Related=Refinery Crude Runs
#/v1/economics/<country>/business?Related=Steel Production
    
### END # /economics/<country>/business ###


### BEGIN # /economics/<country>/consumer ###
@app.route('/v1/economics/<country>/consumer', methods=['GET'])
def get_consumer_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        consumer_section = soup.find('div', id='consumer')
        tables = consumer_section.find_all('table', class_='table table-hover') if consumer_section else None

        data = []
        if tables:
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip the header row
                for row in rows:
                    cells = row.find_all('td')
                    if cells:
                        related_link = cells[0].find('a')
                        related_text = related_link.text.strip() if related_link else 'N/A'
                        data_dict = {
                            'Related': related_text,
                            'Last': cells[1].text.strip(),
                            'Previous': cells[2].text.strip(),
                            'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                            'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                            'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                            'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                        }
                        data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/consumer
#/v1/economics/<country>/consumer?Related=Consumer Confidence
#/v1/economics/<country>/consumer?Related=Retail Sales MoM
#/v1/economics/<country>/consumer?Related=Retail Sales Ex Autos
#/v1/economics/<country>/consumer?Related=Retail Sales YoY
#/v1/economics/<country>/consumer?Related=Consumer Spending
#/v1/economics/<country>/consumer?Related=Disposable Personal Income
#/v1/economics/<country>/consumer?Related=Personal Spending
#/v1/economics/<country>/consumer?Related=Personal Income
#/v1/economics/<country>/consumer?Related=Personal Savings
#/v1/economics/<country>/consumer?Related=Consumer Credit
#/v1/economics/<country>/consumer?Related=Private Sector Credit
#/v1/economics/<country>/consumer?Related=Bank Lending Rate
#/v1/economics/<country>/consumer?Related=Economic Optimism Index
#/v1/economics/<country>/consumer?Related=Redbook Index
#/v1/economics/<country>/consumer?Related=Credit Card Accounts
#/v1/economics/<country>/consumer?Related=Debt Balance Auto Loans
#/v1/economics/<country>/consumer?Related=Debt Balance Credit Cards
#/v1/economics/<country>/consumer?Related=Debt Balance Mortgages
#/v1/economics/<country>/consumer?Related=Debt Balance Student Loans
#/v1/economics/<country>/consumer?Related=Debt Balance Total
#/v1/economics/<country>/consumer?Related=Michigan Consumer Expectations
#/v1/economics/<country>/consumer?Related=Michigan Current Economic Conditions
#/v1/economics/<country>/consumer?Related=Retail Sales Ex Gas and Autos MoM
#/v1/economics/<country>/consumer?Related=Used Car Prices MoM
#/v1/economics/<country>/consumer?Related=Used Car Prices YoY
#/v1/economics/<country>/consumer?Related=Chain Store Sales
#/v1/economics/<country>/consumer?Related=Gasoline Prices
#/v1/economics/<country>/consumer?Related=Households Debt to GDP

### END # /economics/<country>/consumer ###


### BEGIN # /economics/<country>/housing ###
@app.route('/v1/economics/<country>/housing', methods=['GET'])
def get_housing_related(country):
    formatted_country = country.replace(" ", "-").lower()
    #url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    url = f"https://tradingeconomics.com/{formatted_country}/indicators"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        housing_section = soup.find('div', id='housing')
        tables = housing_section.find_all('table', class_='table table-hover') if housing_section else None

        data = []
        if tables:
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip the header row
                for row in rows:
                    cells = row.find_all('td')
                    if cells:
                        related_link = cells[0].find('a')
                        related_text = related_link.text.strip() if related_link else 'N/A'
                        data_dict = {
                            'Related': related_text,
                            'Last': cells[1].text.strip(),
                            'Previous': cells[2].text.strip(),
                            'Highest': cells[3].text.strip() if len(cells) > 3 else 'N/A',
                            'Lowest': cells[4].text.strip() if len(cells) > 4 else 'N/A',
                            'Unit': cells[5].text.strip() if len(cells) > 5 else 'N/A',
                            'Reference': cells[6].text.strip() if len(cells) > 6 else 'N/A',
                        }
                        data.append(data_dict)

        # Filter by 'Related' if query param is given
        related_query = request.args.get('Related')
        if related_query:
            data = [item for item in data if item['Related'].lower() == related_query.lower()]

        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#/v1/economics/<country>/housing
#/v1/economics/<country>/housing?Related=Building Permits
#/v1/economics/<country>/housing?Related=Housing Starts
#/v1/economics/<country>/housing?Related=New Home Sales
#/v1/economics/<country>/housing?Related=Pending Home Sales
#/v1/economics/<country>/housing?Related=Existing Home Sales
#/v1/economics/<country>/housing?Related=Construction Spending
#/v1/economics/<country>/housing?Related=Housing Index
#/v1/economics/<country>/housing?Related=Nahb Housing Market Index
#/v1/economics/<country>/housing?Related=Mortgage Rate
#/v1/economics/<country>/housing?Related=Mortgage Applications
#/v1/economics/<country>/housing?Related=15 Year Mortgage Rate
#/v1/economics/<country>/housing?Related=30 Year Mortgage Rate
#/v1/economics/<country>/housing?Related=Average House Prices
#/v1/economics/<country>/housing?Related=Average Mortgage Size
#/v1/economics/<country>/housing?Related=Building Permits MoM
#/v1/economics/<country>/housing?Related=Case Shiller Home Price Index MoM
#/v1/economics/<country>/housing?Related=Case Shiller Home Price Index YoY
#/v1/economics/<country>/housing?Related=Existing Home Sales MoM
#/v1/economics/<country>/housing?Related=House Price Index MoM
#/v1/economics/<country>/housing?Related=House Price Index YoY
#/v1/economics/<country>/housing?Related=Housing Starts MoM
#/v1/economics/<country>/housing?Related=Housing Starts Multi Family
#/v1/economics/<country>/housing?Related=Housing Starts Single Family
#/v1/economics/<country>/housing?Related=MBA Mortgage Market Index
#/v1/economics/<country>/housing?Related=MBA Mortgage Refinance Index
#/v1/economics/<country>/housing?Related=MBA Purchase Index
#/v1/economics/<country>/housing?Related=Mortgage Originations
#/v1/economics/<country>/housing?Related=National Home Price Index
#/v1/economics/<country>/housing?Related=New Home Sales MoM
#/v1/economics/<country>/housing?Related=Pending Home Sales MoM
#/v1/economics/<country>/housing?Related=Total Housing Inventory
#/v1/economics/<country>/housing?Related=Case Shiller Home Price Index
#/v1/economics/<country>/housing?Related=Home Ownership Rate
#/v1/economics/<country>/housing?Related=Single Family Home Prices
#/v1/economics/<country>/housing?Related=Price to Rent Ratio
#/v1/economics/<country>/housing?Related=Residential Property Prices

### END # /economics/<country>/housing ###
### END # ECONOMICS Endpoints ###


# ### BEGIN # Economic Calendar ### 
@app.route('/v1/economic-calendar', methods=['GET'])
@app.route('/v1/economic-calendar/', methods=['GET'])
def economic_calendar():
    try:
        # Correctly pass the variable to the template using a keyword argument
        return render_template('economic-calendar.html')
    except Exception as e:
        # Consider logging the error for debugging purposes
        return f"An error occurred: {str(e)}", 500
# ### END # Economic Calendar ###


### BEGIN # SCHEMA Economics # Publish schema-economics.json ###
@app.route('/v1/schema-economics.json')
def serve_schema_economics_file():
    return send_from_directory('static', 'schema-economics.json')
### END # SCHEMA Economics # Publish schema-economics.json ###

### END # ENDPOINTS ###


### BEGIN # Flask Run Debug # Run the Flask Application #
if __name__ == '__main__':
    app.run(debug=True)
### END # Flask Run Debug # Run the Flask Application #


#########################################
### ED-API (Economics Data API 1.1.0  ###
#########################################
### End of code ###
