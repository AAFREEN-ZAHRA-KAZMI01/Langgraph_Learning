import os
from dotenv import load_dotenv
from twilio.rest import Client
from langchain.schema import HumanMessage
from email_utils import get_llm

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")  # e.g. "whatsapp:+14155238886"

llm = get_llm()


def send_whatsapp_message(body, to_number):
    """Send a WhatsApp message via Twilio. `to_number` like 'whatsapp:+91XXXXXXXXXX'."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=body, from_=TWILIO_WHATSAPP_FROM, to=to_number)
        print(f"✅ WhatsApp message sent (sid={message.sid})")
        return True
    except Exception as e:
        print("❌ Failed to send WhatsApp message:", str(e))
        return False


def main():
    print("🤖 Welcome to the Groq-Powered WhatsApp Chatbot!")
    print("Type your message. Type 'exit' to quit.\n")

    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        response = llm([HumanMessage(content=user_input)])
        print("🤖 Bot:", response.content)

        send_choice = input("📱 Send this reply via WhatsApp? (y/n): ").strip().lower()
        if send_choice == "y":
            to_number = input("📞 Enter recipient's WhatsApp number (e.g. whatsapp:+91XXXXXXXXXX): ").strip()
            send_whatsapp_message(response.content, to_number)


if __name__ == "__main__":
    main()
