import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def check_availability(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the availability status
    
    availability_div = soup.find('div', class_='availability')

    if availability_div:
        availability = availability_div.text.strip()
    else:
        availability = "Availability information not found"

    return availability

def send_email(sender_email, sender_password, receiver_email, product_name, product_url):
    # Set up SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()

    smtp_server.login(sender_email, sender_password)

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f'Product Available: {product_name}'

    body = f"The product {product_name} is now available.\nYou can purchase it here: {product_url}"
    message.attach(MIMEText(body, 'plain'))

    smtp_server.send_message(message)

    smtp_server.quit()

def main():
    product_url = "https://www.canadacomputers.com/product_info.php?cPath=22_700_1429&item_id=251147&language=en"
    sender_email = "temp"  # Your email
    sender_password = "temp"      # Your email password
    receiver_email = "temp"  # Receiver's email
    product_name = "Monitor"      # Name of the product

    while True:
        availability = check_availability(product_url)

        if "In Stock" in availability:
            send_email(sender_email, sender_password, receiver_email, product_name, product_url)
            print("Email notification sent!")
            break
        else:
            print("Product is still out of stock. Retrying in 1 hour...")
            time.sleep(3600)  # Retry after 1 hour

if __name__ == "__main__":
    main()
