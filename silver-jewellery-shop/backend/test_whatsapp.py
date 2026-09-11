"""
Local test for the WhatsApp order notification.

CallMeBot status: The free WhatsApp bot is currently FULL — no new API keys
can be issued until slots open up.  This script:

  1. Checks if a CALLMEBOT_API_KEY is already in .env and tests it.
  2. If not, opens a pre-filled WhatsApp deep-link so you can manually
     send yourself a test message (no API needed).
  3. Offers instructions for Twilio WhatsApp Sandbox as a free alternative
     that works immediately.

Usage:
  python test_whatsapp.py               # auto-detect and run best option
  python test_whatsapp.py test <key>    # force-test a specific CallMeBot key
  python test_whatsapp.py link          # open WhatsApp deep-link (manual send)
  python test_whatsapp.py twilio        # show Twilio sandbox setup instructions
"""

import sys
import urllib.request
import urllib.parse
import os

OWNER_PHONE = '918072000599'    # 91 + 10-digit number (no +)
OWNER_PHONE_DISPLAY = '+91 80720 00599'

# ──────────────────────────────────────────────────────────────────────────────
# Option A: CallMeBot (if you already have a key)
# ──────────────────────────────────────────────────────────────────────────────

def test_callmebot(api_key: str):
    """Send a fake order notification via CallMeBot (requires a valid API key)."""
    print("\n=== Testing CallMeBot WhatsApp notification ===\n")

    message = (
        "🛍 *New Order — Kasavelli* [TEST]\n"
        "Order ID: order_TEST12345\n"
        f"Customer: Test User (+91 9876543210)\n"
        "\n"
        "*Items Ordered:*\n"
        "• Vanki Silver Ring x1 — ₹1,299\n"
        "• Silver Jhumka Earrings x2 — ₹1,598\n"
        "\n"
        "*Total Paid: ₹2,897*\n"
        "Ship to: 4B, Anna Nagar, Chennai, Tamil Nadu - 600040\n"
        "Contact: 9876543210"
    )

    params = urllib.parse.urlencode({
        'phone':  OWNER_PHONE,
        'text':   message,
        'apikey': api_key,
    })
    url = f'https://api.callmebot.com/whatsapp.php?{params}'

    print(f"Sending to : {OWNER_PHONE_DISPLAY}")
    print(f"API key    : {api_key}")
    print(f"URL        : {url[:90]}...\n")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Kasavelli/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode('utf-8', errors='ignore')
            print(f"HTTP status : {resp.status}")
            print(f"Response    : {body[:300]}\n")

            if 'success' in body.lower():
                print("✅  WhatsApp message sent successfully!")
                print(f"\nAdd to .env:          CALLMEBOT_API_KEY={api_key}")
                print(f"Add to Render dashboard → Environment:")
                print(f"  Key: CALLMEBOT_API_KEY   Value: {api_key}")
            elif 'full' in body.lower() or 'slot' in body.lower():
                print("⚠️  CallMeBot is currently full — no new registrations.")
                print("   Use the WhatsApp deep-link or Twilio approach instead.")
                print("   Run:  python test_whatsapp.py link")
            else:
                print("⚠️  Request completed — check response above for details.")
                print("   If 'not registered': the bot is full, try alternative below.")
                print("   Run:  python test_whatsapp.py link")

    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        print(f"❌  HTTP {e.code}: {body[:300]}")
    except urllib.error.URLError as e:
        print(f"❌  Network error: {e.reason}")
    except Exception as e:
        print(f"❌  Unexpected error: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# Option B: WhatsApp deep-link (no API, manual send from browser)
# ──────────────────────────────────────────────────────────────────────────────

def open_whatsapp_link():
    """Open a WhatsApp deep-link with a pre-filled test order message."""
    print("\n=== WhatsApp Deep-Link Test (no API key needed) ===\n")

    message = (
        "🛍 *New Order — Kasavelli* [TEST]\n"
        "Order ID: order_TEST12345\n"
        "Customer: Test User\n\n"
        "*Items:*\n"
        "• Vanki Ring x1 — ₹1,299\n"
        "• Jhumka Earrings x2 — ₹1,598\n\n"
        "*Total Paid: ₹2,897*\n"
        "Ship to: 4B Anna Nagar, Chennai 600040\n"
        "Contact: 9876543210"
    )

    encoded = urllib.parse.quote(message)
    # wa.me link opens WhatsApp Web / app with the number + message pre-filled
    wa_url = f"https://wa.me/{OWNER_PHONE}?text={encoded}"

    print(f"Opening WhatsApp to send test message to {OWNER_PHONE_DISPLAY}")
    print(f"URL: {wa_url[:80]}...\n")
    print("This opens WhatsApp Web — just click SEND in the browser.\n")

    try:
        import webbrowser
        webbrowser.open(wa_url)
        print("✅  WhatsApp Web opened in your browser.")
        print("   Click 'Send' to deliver the test order message to yourself.")
    except Exception:
        print("Could not open browser automatically.")
        print(f"Copy and open this URL manually:\n{wa_url}")


# ──────────────────────────────────────────────────────────────────────────────
# Option C: Twilio WhatsApp Sandbox instructions
# ──────────────────────────────────────────────────────────────────────────────

def show_twilio_instructions():
    print("""
=== Twilio WhatsApp Sandbox (free, works immediately) ===

1. Sign up free at https://www.twilio.com/try-twilio
2. In the Twilio console → Messaging → Try it out → Send a WhatsApp message
3. You'll see a sandbox number like: +1 415 523 8886
4. Send  join <your-sandbox-word>  from +91 8072000599 to that number on WhatsApp
5. Once joined, run a quick test:

   pip install twilio
   python test_whatsapp.py twilio-test <account_sid> <auth_token> <sandbox_number>

6. Add to .env:
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

Note: The sandbox works for 72 hours per session. For production you'll need
      a Twilio approved WhatsApp sender (~$0.005/message).
""")


def test_twilio(account_sid, auth_token, from_number):
    """Send a test WhatsApp via Twilio."""
    try:
        from twilio.rest import Client
    except ImportError:
        print("❌  Twilio not installed. Run:  pip install twilio")
        return

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=(
            "🛍 *New Order — Kasavelli* [TEST]\n"
            "Order: TEST12345 | Total: ₹2,897\n"
            "Customer: Test User | Ship to: Chennai 600040"
        ),
        from_=f'whatsapp:{from_number}',
        to=f'whatsapp:+{OWNER_PHONE}'
    )
    print(f"✅  Twilio message sent! SID: {message.sid}")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if args and args[0] == 'test' and len(args) >= 2:
        test_callmebot(args[1])

    elif args and args[0] == 'link':
        open_whatsapp_link()

    elif args and args[0] == 'twilio':
        show_twilio_instructions()

    elif args and args[0] == 'twilio-test' and len(args) >= 4:
        test_twilio(args[1], args[2], args[3])

    else:
        # Auto: check if CALLMEBOT_API_KEY is already in env / .env
        api_key = os.environ.get('CALLMEBOT_API_KEY', '')
        if not api_key:
            # Try reading from .env manually
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            if os.path.exists(env_path):
                for line in open(env_path):
                    line = line.strip()
                    if line.startswith('CALLMEBOT_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break

        if api_key:
            print(f"✓ Found CALLMEBOT_API_KEY in .env — testing CallMeBot...")
            test_callmebot(api_key)
        else:
            print("⚠️  No CALLMEBOT_API_KEY found in .env\n")
            print("CallMeBot Status: Bot is currently FULL — no new registrations.")
            print("Using WhatsApp deep-link instead (manual send, no API key needed).\n")
            open_whatsapp_link()
            print("\n─────────────────────────────────────────────────────")
            print("Other options:")
            print("  python test_whatsapp.py test <key>   → test a CallMeBot key")
            print("  python test_whatsapp.py twilio       → Twilio setup instructions")
            print("─────────────────────────────────────────────────────")


if __name__ == '__main__':
    main()

# Made with Bob
