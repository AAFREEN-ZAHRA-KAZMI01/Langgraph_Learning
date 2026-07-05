"""Shared helpers for the Gmail-based tool scripts in this folder.

fetch_email_tool.py, send_email_tool.py, and send_email_with_langsmith.py
all talk to the same Gmail account and the same Groq LLM — this module
centralizes that setup so each script only contains its own logic.
"""
import os
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.header import decode_header
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def get_llm(model_name="llama-3.1-8b-instant", temperature=0.3):
    return ChatGroq(temperature=temperature, groq_api_key=GROQ_API_KEY, model_name=model_name)


def setup_langsmith_tracing(default_project="default"):
    """Enable LangSmith tracing if LANGCHAIN_API_KEY is set. No-op otherwise."""
    api_key = os.getenv("LANGCHAIN_API_KEY")
    if not api_key:
        return
    os.environ["LANGCHAIN_API_KEY"] = api_key
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", default_project)
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")


def decode_email_subject(msg):
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        return subject.decode(encoding or "utf-8", errors="ignore")
    return subject


def get_email_body(msg):
    """Extract the first text/plain body from a (possibly multipart) email message."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                if body:
                    return body.decode(errors="ignore")
        return ""
    payload = msg.get_payload(decode=True)
    return payload.decode(errors="ignore") if payload else ""


def imap_connect():
    """Log in to Gmail over IMAP and select the inbox."""
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select("inbox")
    return mail


def smtp_connect():
    """Log in to Gmail over SMTP using STARTTLS (for scripts that send multiple emails)."""
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    return smtp


def send_email(subject, body, to_email, from_email=None):
    """Send a single email over SMTP_SSL. Returns True on success, False on failure."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email or EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print("✅ Email sent successfully.")
        return True
    except Exception as e:
        print("❌ Failed to send email:", str(e))
        return False
