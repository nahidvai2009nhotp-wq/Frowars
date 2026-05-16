import os
import time
import requests

# আপনার দেওয়া প্যানেল ও টেলিগ্রাম কনফিগারেশন
BASE_URL = "http://185.190.142.81/api/v1/"
API_KEY = "nxa_a0c78ce02c9a7cee35d9886f72d4c42935a63863"
GROUP_ID = "-1003735393669"
TELEGRAM_BOT_TOKEN = "8255693337:AAEOHh2xoiOwoR-K3ndLGtui8dmbGcgVlJ0"

# ডুপ্লিকেট মেসেজ আটকানোর জন্য সেট
sent_messages = set()

def get_panel_messages():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    try:
        # প্যানেলের এন্ডপয়েন্ট (প্রয়োজনে /messages পরিবর্তন করতে পারেন)
        response = requests.get(f"{BASE_URL}messages", headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Panel API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching data from panel: {e}")
        return []

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": GROUP_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code != 200:
            print(f"Telegram Error: {response.text}")
    except Exception as e:
        print(f"Telegram Connection Error: {e}")

def main():
    print("Bot is running and monitoring OTPs...")
    while True:
        messages = get_panel_messages()
        
        # যদি API থেকে লিস্ট আকারে ডেটা আসে
        if isinstance(messages, list):
            for msg in messages:
                msg_id = msg.get("id") or msg.get("_id") # প্যানেলের আইডি ফরম্যাট অনুযায়ী
                msg_text = msg.get("otp_message") or msg.get("message") or msg.get("otp")
                
                if msg_id and msg_text and msg_id not in sent_messages:
                    formatted_text = f"📩 *New OTP Received:*\n\n{msg_text}"
                    send_to_telegram(formatted_text)
                    sent_messages.add(msg_id)
                    
        # মেমোরি ক্লিয়ার রাখার জন্য
        if len(sent_messages) > 1000:
            sent_messages.clear()
            
        time.sleep(5) # প্রতি ৫ সেকেন্ড পর পর নতুন ওটিপি চেক করবে

if __name__ == "__main__":
    main()
  
