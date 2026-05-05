import requests
import json
import time

# ================== CONFIG ==================
BOT_TOKEN = "8694702193:AAGqpwL1gz0vhB4pCBezSzMVcS9_qPRTDJQ"  # <-- PUT YOUR TELEGRAM BOT TOKEN HERE
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

EXTERNAL_API_URL = "5f829fb665db72e1fe34ea83ef3a2a9d"  # <-- PUT YOUR EXTERNAL HTTPS API HERE (dummy placeholder)

# ================== KEYBOARD ==================
def get_main_keyboard():
    keyboard = {
        "keyboard": [
            [{"text": "📱 Phone Lookup"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    return json.dumps(keyboard)

# ================== SEND MESSAGE ==================
def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    url = API_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Send message error:", e)

# ================== GET UPDATES ==================
def get_updates(offset):
    url = API_URL + "getUpdates"
    params = {
        "timeout": 30,
        "offset": offset
    }

    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print("Get updates error:", e)
        return {}

# ================== PHONE VALIDATION ==================
def is_valid_phone(number):
    return number.isdigit() and len(number) == 10

# ================== EXTERNAL API CALL ==================
def call_external_api(phone):
    try:
        # Dummy HTTPS API call (replace with real endpoint)
        response = requests.get(EXTERNAL_API_URL, params={"phone": phone}, timeout=10)

        # Convert to JSON safely
        try:
            data = response.json()
        except:
            data = {"error": "Invalid JSON response from API"}

        return data

    except Exception as e:
        return {"error": str(e)}

# ================== MAIN LOOP ==================
def main():
    offset = 0

    print("Bot is running...")

    while True:
        updates = get_updates(offset)

        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" not in update:
                    continue

                message = update["message"]
                chat_id = message["chat"]["id"]

                if "text" not in message:
                    continue

                text = message["text"].strip()

                # ================== COMMAND: /start ==================
                if text == "/start":
                    send_message(
                        chat_id,
                        "👋 Welcome!\n\nUse the button below to lookup a phone number.",
                        reply_markup=get_main_keyboard()
                    )

                # ================== BUTTON CLICK ==================
                elif text == "📱 Phone Lookup":
                    send_message(chat_id, "📞 Send 10 digit mobile number:")

                # ================== PHONE INPUT ==================
                elif is_valid_phone(text):
                    send_message(chat_id, "⏳ Checking number...")

                    api_response = call_external_api(text)

                    formatted = json.dumps(api_response, indent=4)

                    send_message(
                        chat_id,
                        f"<pre>{formatted}</pre>",
                        parse_mode="HTML"
                    )

                # ================== INVALID INPUT ==================
                else:
                    send_message(
                        chat_id,
                        "❌ Invalid input.\n\nPlease send a valid 10-digit mobile number or use the button.",
                        reply_markup=get_main_keyboard()
                    )

        time.sleep(1)

# ================== RUN ==================
if __name__ == "__main__":
    main()
