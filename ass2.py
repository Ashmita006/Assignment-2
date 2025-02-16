import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import random
import os

url = "https://www.nepalstock.com/todays_price"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

data = []
table = soup.find('table', {'class': 'table table-bordered table-hover table-striped table-condensed'})


for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    if len(cells) > 0:
        company_name = cells[0].text.strip()
        stock_price = cells[2].text.strip()
        import_value = cells[5].text.strip() 
        data.append([company_name, stock_price, import_value])

df = pd.DataFrame(data, columns=['Company', 'Stock Price', 'Import Value'])
df.to_csv('nepse_data.csv', index=False)
print("Nepse data saved to nepse_data.csv")

api_key = "6c4c45640aa457fffe1b345d98f233f"
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q=Kathmandu&appid={api_key}&units=metric"
weather_response = requests.get(weather_url)
weather_data = weather_response.json()

temperature = weather_data['main']['temp']
humidity = weather_data['main']['humidity']
weather_condition = weather_data['weather'][0]['description']

print(f"Temperature: {temperature}°C")
print(f"Humidity: {humidity}%")
print(f"Weather condition: {weather_condition}")


df = pd.read_csv('nepse_data.csv')

df['Stock Price'] = pd.to_numeric(df['Stock Price'], errors='coerce')

top_10_companies = df.sort_values(by='Stock Price', ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_10_companies['Company'], top_10_companies['Stock Price'], color='skyblue')
plt.xlabel('Stock Price (NPR)')
plt.title('Top 10 Nepse Companies by Stock Price')
plt.gca().invert_yaxis()  
plt.tight_layout()

plt.savefig('nepse_chart.png')
print("Stock chart saved as nepse_chart.png")


quote_url = "https://zenquotes.io/api/random"
quote_response = requests.get(quote_url)
quote_data = quote_response.json()
quote_text = quote_data[0]['q']

sender_email = "ashmitashrestha613@gmail.com"
receiver_email = "ruman.metahorizon@gmail.com"
email_password = "iwya aaoz tpho ekti"
smtp_server = "smtp.gmail.com"
smtp_port = 587

subject = "Your Daily Inspiration & Nepse Report"
body = f"""Hello, here is your daily dose of inspiration:
    
"{quote_text}"
    
Also, the weather in Kathmandu today:
Temperature: {temperature}°C
Humidity: {humidity}%
Condition: {weather_condition}

Best regards,
Your Daily Report"""


msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))


with open('nepse_chart.png', 'rb') as file:
    img = MIMEImage(file.read())
    img.add_header('Content-Disposition', 'attachment', filename='nepse_chart.png')
    msg.attach(img)


try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls() 
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")