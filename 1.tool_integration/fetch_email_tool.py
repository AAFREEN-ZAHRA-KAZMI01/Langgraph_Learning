import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Load credentials
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    temperature=0.3,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
)

# 📥 Fetch email summary
def fetch_email_summary():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        total_emails = int(input("📩 How many recent emails do you want to summarize? (e.g., 5, 10): "))
        if total_emails <= 0:
            return "❗ Invalid number entered."

        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()
        latest_n = mail_ids[-total_emails:]

        summary = ""
        for num in reversed(latest_n):
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_ = msg.get("From")
            summary += f"From: {from_}\nSubject: {subject}\n" + "-" * 30 + "\n"

        mail.logout()
        return summary

    except Exception as e:
        return f"❌ Error: {str(e)}"

# 📌 Fetch all matching emails based on keyword
def fetch_specific_email(keyword):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()
        mail_ids.reverse()

        matched_emails = []

        for num in mail_ids:
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_ = msg.get("From")
            full_content = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        if body:
                            full_content = body.decode(errors="ignore")
                            break
            else:
                full_content = msg.get_payload(decode=True).decode(errors="ignore")

            if keyword.lower() in subject.lower() or keyword.lower() in from_.lower():
                matched_emails.append(
                    f"📧 From: {from_}\n📌 Subject: {subject}\n\n📄 Content:\n{full_content[:800]}...\n{'-'*50}"
                )

        mail.logout()

        if matched_emails:
            return "\n\n".join(matched_emails)
        else:
            return f"❗ No email found matching the keyword: {keyword}"

    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🤖 Smart Email Bot
def smart_email_bot():
    print("🤖 Groq Smart Email Assistant")
    print("-----------------------------")

    while True:
        print("\nLLM: What would you like to do?")
        print("1️⃣ View inbox summary")
        print("2️⃣ Search for a specific email (by keyword)")
        print("❌ Exit the assistant")

        user_intent = input("🧑 Your choice (summary / keyword / exit): ").strip().lower()

        if user_intent == "exit":
            print("👋 Goodbye! The assistant has exited.")
            break

        elif user_intent == "summary":
            summary = fetch_email_summary()
            print("\n📬 Inbox Summary:\n", summary)

            follow_up = input("\n🧑 Would you like to ask something about this summary? (y/n): ").strip()
            if follow_up.lower() == "y":
                question = input("❓ Your question (English or any language): ")
                prompt = f"Inbox summary:\n{summary}\n\nQuestion:\n{question}"
                response = llm([HumanMessage(content=prompt)]).content
                print("\n🤖 LLM Response:\n", response)

        elif user_intent == "keyword":
            keyword = input("🔍 Enter a keyword (e.g., YouTube, job, Google) to search for emails: ")
            specific_data = fetch_specific_email(keyword)
            print("\n📨 Matching Emails:\n", specific_data)

            ask_llm = input("\n❓ Would you like to ask something about these emails? (y/n): ").strip()
            if ask_llm.lower() == "y":
                q = input("🧑 Your question (English or any language): ")
                prompt = f"Here are the emails:\n{specific_data}\n\nNow answer this question:\n{q}"
                response = llm([HumanMessage(content=prompt)]).content
                print("\n🤖 LLM Response:\n", response)

        else:
            print("⚠️ Invalid input. Please type only 'summary', 'keyword', or 'exit'.")

# 🚀 Run
if __name__ == "__main__":
    smart_email_bot()
