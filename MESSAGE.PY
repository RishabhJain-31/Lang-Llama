from twilio.rest import Client
import os
from dotenv import load_dotenv

def send_lead(name,phone_number):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
    from_="whatsapp:+14155238886",  # Twilio sandbox number
    to="whatsapp:+917428817537",  # Your verified number
    body=f"New Lead\n👤 Name: {name}\n📞 Phone: {phone_number}"
)
    
    formatted_lead = f"👤 Name: {name} | 📞 Phone: {phone_number}"
    try:
        with open("leads.txt", "r", encoding="utf-8") as f:
            existing_leads = f.read().splitlines()
    except FileNotFoundError:
        existing_leads = []

    if not any(phone_number in lead for lead in existing_leads):
        with open("leads.txt", "a", encoding="utf-8") as f:
            f.write(formatted_lead + "\n")

    return message.sid
