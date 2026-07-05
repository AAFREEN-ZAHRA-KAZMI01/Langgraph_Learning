import os
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.header import decode_header
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# 🔐 Load .env credentials
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🤖 Init LLM
llm = ChatGroq(
    temperature=0.3,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
)

# 📥 Inbox Summary
def fetch_email_summary():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        total_emails = int(input("📩 How many recent emails to summarize (e.g., 5, 10): "))
        if total_emails <= 0:
            return "❗ Invalid number entered."

        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()[-total_emails:]

        summary = ""
        for num in reversed(mail_ids):
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            subject = subject.decode(encoding or "utf-8", errors="ignore") if isinstance(subject, bytes) else subject
            from_ = msg.get("From")

            summary += f"From: {from_}\nSubject: {subject}\n" + "-" * 30 + "\n"

        mail.logout()
        return summary

    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🔍 Search emails by keyword
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
            subject = subject.decode(encoding or "utf-8", errors="ignore") if isinstance(subject, bytes) else subject
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
        return "\n\n".join(matched_emails) if matched_emails else f"❗ No email found for keyword: {keyword}"

    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🤖 Auto-reply to unread important inbox emails
def auto_reply_to_unread():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        mail_ids = messages[0].split()
        if not mail_ids:
            return "✅ No unread emails found."

        smtp = smtplib.SMTP(os.getenv("SMTP_SERVER", "smtp.gmail.com"), int(os.getenv("SMTP_PORT", 587)))
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        replies = []
        skip_keywords = ["noreply", "no-reply", "mailer", "support", "newsletter", "update", "notifications", "donotreply"]

        for num in mail_ids:
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            subject = subject.decode(encoding or "utf-8", errors="ignore") if isinstance(subject, bytes) else subject
            from_ = msg.get("From")
            sender_email = email.utils.parseaddr(from_)[1]

            if EMAIL_ADDRESS.lower() in sender_email.lower() or any(x in sender_email.lower() for x in skip_keywords):
                continue

            content = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        if body:
                            content = body.decode(errors="ignore")
                            break
            else:
                content = msg.get_payload(decode=True).decode(errors="ignore")

            # 🧠 Ask LLM if reply is needed
            judgment_prompt = f"""You're a smart assistant. Read this email and answer only: yes or no.
Does this email seem like it's from a real person and needs a reply?

Subject: {subject}
From: {sender_email}
Message:
{content}
"""
            decision = llm([HumanMessage(content=judgment_prompt)]).content.strip().lower()
            if "yes" not in decision:
                continue

            # ✍️ Generate reply
            reply_prompt = f"Write a short, polite, professional reply to this email:\n\nSubject: {subject}\n\n{content}"
            reply_text = llm([HumanMessage(content=reply_prompt)]).content

            reply_msg = MIMEText(reply_text)
            reply_msg["Subject"] = "Re: " + subject
            reply_msg["From"] = EMAIL_ADDRESS
            reply_msg["To"] = sender_email

            smtp.sendmail(EMAIL_ADDRESS, sender_email, reply_msg.as_string())
            replies.append(f"✅ Replied to: {sender_email} | Subject: {subject}")

        smtp.quit()
        mail.logout()
        return "\n".join(replies) if replies else "✅ No suitable unread emails to reply."

    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🧠 Chat Assistant
def smart_email_bot():
    print("🤖 Groq Smart Email Assistant\n-----------------------------")

    while True:
        print("\nChoose an action:")
        print("1️⃣ Inbox Summary")
        print("2️⃣ Search Email by Keyword")
        print("3️⃣ Auto-Reply to Important Emails")
        print("❌ Exit")

        choice = input("🧑 Your choice (summary / keyword / auto / exit): ").strip().lower()

        if choice == "exit":
            print("👋 Goodbye!")
            break

        elif choice == "summary":
            summary = fetch_email_summary()
            print("\n📬 Summary:\n", summary)
            if input("❓ Ask anything about it? (y/n): ").lower() == "y":
                q = input("💬 Your question: ")
                prompt = f"Summary:\n{summary}\n\nQuestion:\n{q}"
                answer = llm([HumanMessage(content=prompt)]).content
                print("\n🤖 Answer:\n", answer)

        elif choice == "keyword":
            keyword = input("🔍 Keyword to search: ")
            results = fetch_specific_email(keyword)
            print("\n📨 Matches:\n", results)
            if input("❓ Ask anything about it? (y/n): ").lower() == "y":
                q = input("💬 Your question: ")
                prompt = f"Emails:\n{results}\n\nQuestion:\n{q}"
                answer = llm([HumanMessage(content=prompt)]).content
                print("\n🤖 Answer:\n", answer)

        elif choice == "auto":
            print("🤖 Auto-replying to important unread emails...")
            result = auto_reply_to_unread()
            print("\n📨 Result:\n", result)

        else:
            print("⚠️ Invalid input. Try again.")

# 🚀 Run
if __name__ == "__main__":
    smart_email_bot()
