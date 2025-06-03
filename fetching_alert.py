import imapclient
import pyzmail
import getpass
import time

EMAIL = "tradingbotgik@gmail.com"
PASSWORD = "qwgu dojn mtrh fslv"

# Keep track of already seen UIDs to avoid duplicates
seen_uids = set()

def fetch_emails():
    with imapclient.IMAPClient('imap.gmail.com', ssl=True) as imap:
        imap.login(EMAIL, PASSWORD)
        imap.select_folder('INBOX', readonly=True)

        UIDs = imap.search(['UNSEEN'])  # Fetch only unread emails

        new_emails = [uid for uid in UIDs if uid not in seen_uids]
        for uid in new_emails:
            raw_message = imap.fetch([uid], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])

            subject = message.get_subject()
            from_email = message.get_addresses('from')[0][1]

            if message.text_part:
                body = message.text_part.get_payload().decode(message.text_part.charset)
            elif message.html_part:
                body = message.html_part.get_payload().decode(message.html_part.charset)
            else:
                body = "No text content"

            print(f"\nFrom: {from_email}")
            print(f"Subject: {subject}")
            
           

            seen_uids.add(uid)

if __name__ == "__main__":
    print("📬 Gmail Scraper started... Fetching emails every 60 seconds.\n")
    while True:
        try:
            fetch_emails()
        except Exception as e:
            print(f"❌ Error occurred: {e}")
        time.sleep(60)
