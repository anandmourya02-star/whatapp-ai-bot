from flask import Flask, request
import requests
import time

app = Flask(__name__)

VERIFY_TOKEN = "12345"
WHATSAPP_TOKEN = "take your own token"
PHONE_ID = "your phone id "

def send_message(phone, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=data)

def human_reply(text):
    text = text.lower()

    if "menu" in text:
        return "Hi 😊 hamara menu hai: Pizza 🍕, Burger 🍔, Pasta 🍝\nKya order karna chahoge?"
    
    elif "table" in text:
        return "Sure sir 🙌 kitne log ke liye table chahiye?"
    
    elif "hello" in text or "hi" in text:
        return "Hello 👋 Welcome to Mourya Restaurant!\nKaise help kar sakta hoon?"
    
    else:
        return "Ji 😊 thoda clear bataoge kya chahiye? Main help kar deta hoon 👍"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Error"

    data = request.json
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        phone = msg["from"]
        text = msg["text"]["body"]

        time.sleep(2)  # typing feel 😎
        reply = human_reply(text)
        send_message(phone, reply)

    except:
        pass

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)
