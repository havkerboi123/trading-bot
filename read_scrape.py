import requests
import time

# Replace this with your actual ngrok or local URL
FLASK_ENDPOINT = "http://localhost:5000/status"  # or "https://xyz.ngrok.io/status"

def poll_status():
    while True:
        try:
            response = requests.get(FLASK_ENDPOINT)
            if response.status_code == 200:
                data = response.json()
                status = data.get("email_status", "NO")

                if status == "YES":
                    print("✅ YES → Execute Trade")
                elif status == "NO":
                    print("❌ NO → Skip Trade")
                else:
                    print(f"⚠️ Unexpected status: {status}")
            else:
                print(f"🔴 Error: Received {response.status_code}")

        except Exception as e:
            print(f"🛑 Exception occurred: {e}")

        time.sleep(60)

if __name__ == "__main__":
    print("📡 Trading Decision Bot Started. Polling every 60 seconds.\n")
    poll_status()
