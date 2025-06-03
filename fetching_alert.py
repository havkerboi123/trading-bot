from flask import Flask, jsonify
import threading
import imapclient
import pyzmail
import time
import os
import json

app = Flask(__name__)

EMAIL = "tradingbotgik@gmail.com"
PASSWORD = "qwgu dojn mtrh fslv"
UID_FILE = "seen_uids.json"
seen_uids = set()
last_email_status = "NO"  # Default state

# Load seen UIDs from file
if os.path.exists(UID_FILE):
    with open(UID_FILE, "r") as f:
        seen_uids = set(json.load(f))

def save_seen_uids():
    with open(UID_FILE, "w") as f:
        json.dump(list(seen_uids), f)

def fetch_emails_loop():
    global seen_uids, last_email_status
    print("📬 Gmail TradingBot Trigger started... Checking every 60 seconds.\n")
    while True:
        try:
            with imapclient.IMAPClient('imap.gmail.com', ssl=True) as imap:
                imap.login(EMAIL, PASSWORD)
                imap.select_folder('INBOX', readonly=True)

                UIDs = imap.search(['UNSEEN'])
                new_emails = [uid for uid in UIDs if uid not in seen_uids]

                if new_emails:
                    last_email_status = "YES"
                    for uid in new_emails:
                        raw_message = imap.fetch([uid], ['BODY[]', 'FLAGS'])
                        message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])
                        subject = message.get_subject()
                        from_email = message.get_addresses('from')[0][1]
                        print(f"From: {from_email}")
                        print(f"Subject: {subject}")
                        seen_uids.add(uid)
                    save_seen_uids()
                else:
                    last_email_status = "NO"

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            last_email_status = "ERROR"
        time.sleep(60)

# Flask endpoint
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"email_status": last_email_status})

# Run background thread before Flask starts
def start_background():
    thread = threading.Thread(target=fetch_emails_loop)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    start_background()
    app.run(port=5000, debug=False)
