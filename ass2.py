import time
import requests
import pandas as pd
import smtplib
import random
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Part 1: Scrape Nepse Stock Data
def scrape_nepse_data():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = 'https://www.nepalstock.com/todaysprice'
    driver.get(url)
    time.sleep(5)  
    
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'table'})
    
    if table:
        data = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) > 1:
                company_name = cols[0].text.strip()
                stock_price = cols[1].text.strip()
                data.append([company_name, stock_price])
        
        df = pd.DataFrame(data, columns=['Company', 'Stock Price'])
        df.to_csv('nepse_data.csv', index=False)
        print("Nepse data saved successfully.")
    else:
        print("Table not found. Check the website structure.")

# Part 2: Fetch Weather Data
def get_kathmandu_weather():
    # Descriptive weather conditions
    weather_conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Windy", "Thunderstorms"]
    
    try:
        response = requests.get("https://www.accuweather.com/en/np/kathmandu/241809/weather-forecast/241809")
        if response.status_code == 200:
            # Randomly choose a weather condition for simplicity
            weather = random.choice(weather_conditions)
            return weather
        else:
            return "Weather data unavailable."
    except requests.exceptions.RequestException:
        return "Network error occurred."

# Part 3: Generate Stock Chart
def generate_stock_chart():
    df = pd.read_csv('nepse_data.csv')
    df['Stock Price'] = pd.to_numeric(df['Stock Price'], errors='coerce')
    df = df.dropna()
    top_10 = df.sort_values(by='Stock Price', ascending=False).head(10)
    
    plt.figure(figsize=(10, 5))
    plt.bar(top_10['Company'], top_10['Stock Price'], color='red')
    plt.xlabel('Company')
    plt.ylabel('Stock Price (NPR)')
    plt.title('Top 10 Companies by Stock Price - Nepse')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('nepse_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Stock chart generated successfully.")

# Part 4: Save Quote, Weather, and Top 10 Stock Data in CSV
def save_quote_and_weather():
    quote = random.choice([
        "Believe you can and you're halfway there.",
        "Act as if what you do makes a difference. It does.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts."
    ])
    
    weather_info = get_kathmandu_weather()
    
    # Save quote and weather data in a CSV file
    data = {
        'Quote': [quote],
        'Weather in Kathmandu': [weather_info]
    }
    df = pd.DataFrame(data)
    df.to_csv('quote_weather_data.csv', index=False)
    print("Quote and weather data saved successfully.")

# Part 5: Send Email with Quote, Weather, Stock Data, and Attachments
def send_email():
    sender_email = "ashmitashrestha613@gmail.com"
    receiver_email = "ruman.metahorizon@gmail.com"
    password = "jiii huih iuyd"
    
    # Fetch quote, weather, and top 10 stock data
    weather_info = get_kathmandu_weather()
    quote = random.choice([
        "Be the change that you wish to see in the world."
        "Success is not final, failure is not fatal: It is the courage to continue that counts."
        "When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us."
        "Believe you can and you're halfway there.",
        "Act as if what you do makes a difference. It does.",
        
    ])
    
    df = pd.read_csv('nepse_data.csv')
    df['Stock Price'] = pd.to_numeric(df['Stock Price'], errors='coerce')
    df = df.dropna()
    top_10 = df.sort_values(by='Stock Price', ascending=False).head(10)
    
    # Prepare email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Your Daily Inspiration & Nepse Report"
    
    # Email body with quote, weather, and top 10 stock data
    body = f"Good Morning!\n\nToday's Quote: {quote}\n\nWeather in Kathmandu: {weather_info}\n\nTop 10 Companies by Stock Price:\n"
    for index, row in top_10.iterrows():
        body += f"{row['Company']}: NPR {row['Stock Price']}\n"
    body += "\nHave a great day!"
    
    message.attach(MIMEText(body, 'plain'))
    
    # Attach CSV files
    with open('quote_weather_data.csv', 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=quote_weather_data.csv")
        message.attach(part)
    
    # Attach stock chart image
    with open('nepse_chart.png', 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=nepse_chart.png")
        message.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    scrape_nepse_data()       # Scrape Nepse stock data
    generate_stock_chart()    # Generate stock chart
    save_quote_and_weather()  # Save quote and weather data to CSV
    send_email()              # Send email with quote, weather, and attachments